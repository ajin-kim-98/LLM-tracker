"""윈터딜 수집기.

뽐뿌 핫딜 RSS와 Google 뉴스 RSS에서 새 글을 가져와
config.json의 키워드에 맞는 글만 site/deals.json에 저장한다.
표준 라이브러리만 사용한다.
"""

from __future__ import annotations

import json
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "config.json"
OUTPUT_PATH = ROOT / "site" / "deals.json"

PPOMPPU_URL = "https://www.ppomppu.co.kr/rss.php?id=ppomppu"
GOOGLE_NEWS_URL = "https://news.google.com/rss/search?{query}"
USER_AGENT = "Mozilla/5.0 (compatible; WinterDeal/1.0; personal feed reader)"

# "12,610원", "9900원", "9.9만원", "3만원" 같은 표기를 찾는다.
PRICE_RE = re.compile(r"(\d+(?:\.\d+)?\s*만\s*원|\d{1,3}(?:,\d{3})+\s*원|\d+\s*원)")


# ---------- 순수 함수 (테스트 대상) ----------

def extract_price(title: str) -> str | None:
    """제목에 적힌 가격 문자열을 그대로 돌려준다. 없으면 None (지어내지 않는다)."""
    match = PRICE_RE.search(title)
    if not match:
        return None
    return re.sub(r"\s+", "", match.group(1))


def parse_date(text: str | None) -> str | None:
    if not text:
        return None
    try:
        dt = parsedate_to_datetime(text.strip())
    except (TypeError, ValueError):
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat()


def parse_ppomppu(xml_text: str) -> list[dict]:
    root = ET.fromstring(xml_text)
    items = []
    for node in root.iter("item"):
        title = (node.findtext("title") or "").strip()
        link = (node.findtext("link") or "").strip()
        if not title or not link:
            continue
        shop = re.match(r"^\[([^\]]+)\]", title)
        items.append({
            "title": title,
            "link": link,
            "source": "뽐뿌 핫딜",
            "shop": shop.group(1).strip() if shop else None,
            "kind": "hotdeal",
            "published_at": parse_date(node.findtext("pubDate")),
        })
    return items


def parse_google_news(xml_text: str) -> list[dict]:
    root = ET.fromstring(xml_text)
    items = []
    for node in root.iter("item"):
        title = (node.findtext("title") or "").strip()
        link = (node.findtext("link") or "").strip()
        if not title or not link:
            continue
        publisher = (node.findtext("source") or "").strip()
        # Google 뉴스 제목 끝의 " - 언론사"를 떼어낸다.
        if publisher and title.endswith(f" - {publisher}"):
            title = title[: -len(f" - {publisher}")].strip()
        items.append({
            "title": title,
            "link": link,
            "source": f"Google 뉴스 · {publisher}" if publisher else "Google 뉴스",
            "shop": None,
            "kind": "news",
            "published_at": parse_date(node.findtext("pubDate")),
        })
    return items


def matches(item: dict, keywords: list[str], sale_words: list[str]) -> bool:
    title = item["title"].lower()
    if not any(k.lower() in title for k in keywords):
        return False
    if item["kind"] == "news":
        return any(w in title for w in sale_words)
    return True


def filter_items(items: list[dict], keywords: list[str], sale_words: list[str]) -> list[dict]:
    result = []
    for item in items:
        if matches(item, keywords, sale_words):
            item = dict(item)
            item["price"] = extract_price(item["title"])
            item["keywords"] = [k for k in keywords if k.lower() in item["title"].lower()]
            result.append(item)
    return sort_latest(result)


def sort_latest(items: list[dict]) -> list[dict]:
    return sorted(items, key=lambda i: i.get("published_at") or "", reverse=True)


def title_key(title: str) -> str:
    """중복 판단용 제목: 따옴표·말줄임표·공백 등 기호를 모두 빼고 소문자로 맞춘다."""
    return re.sub(r"[^0-9a-z가-힣]", "", title.lower())


def dedupe_by_title(items: list[dict]) -> list[dict]:
    """제목이 같은 글은 가장 최근 것 하나만 남긴다 (언론사만 다른 같은 기사 등)."""
    seen: set[str] = set()
    result = []
    for item in sort_latest(items):
        key = title_key(item["title"])
        if key in seen:
            continue
        seen.add(key)
        result.append(item)
    return result


def merge(old: list[dict], new: list[dict], keep_days: int, max_items: int,
          now: datetime | None = None) -> list[dict]:
    """이전 결과와 새 결과를 링크와 제목 기준으로 합치고 오래된 글을 지운다."""
    now = now or datetime.now(timezone.utc)
    cutoff = (now - timedelta(days=keep_days)).isoformat()
    by_link = {i["link"]: i for i in old}
    by_link.update({i["link"]: i for i in new})
    kept = [i for i in by_link.values() if (i.get("published_at") or "") >= cutoff]
    return dedupe_by_title(kept)[:max_items]


# ---------- 네트워크 ----------

def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read().decode("utf-8", errors="replace")


def google_news_url(keyword: str, sale_words: list[str]) -> str:
    q = f'"{keyword}" ({" OR ".join(sale_words)}) when:7d'
    return GOOGLE_NEWS_URL.format(query=urllib.parse.urlencode(
        {"q": q, "hl": "ko", "gl": "KR", "ceid": "KR:ko"}))


def collect(config: dict) -> tuple[list[dict], list[str]]:
    keywords, sale_words = config["keywords"], config["news_sale_words"]
    raw, errors = [], []
    try:
        raw += parse_ppomppu(fetch(PPOMPPU_URL))
    except Exception as e:  # 한 출처가 실패해도 나머지는 계속 모은다.
        errors.append(f"뽐뿌: {e}")
    for kw in keywords:
        try:
            raw += parse_google_news(fetch(google_news_url(kw, sale_words)))
        except Exception as e:
            errors.append(f"Google 뉴스({kw}): {e}")
    return filter_items(raw, keywords, sale_words), errors


def main() -> int:
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    old = []
    if OUTPUT_PATH.exists():
        old = json.loads(OUTPUT_PATH.read_text(encoding="utf-8")).get("items", [])

    new, errors = collect(config)
    for err in errors:
        print(f"[경고] {err}", file=sys.stderr)

    items = merge(old, new, config["keep_days"], config["max_items"])
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps({
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "keywords": config["keywords"],
        "items": items,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"새로 찾은 글 {len(new)}건, 저장된 글 {len(items)}건")
    # 모든 출처가 실패했을 때만 실패로 처리한다.
    return 1 if len(errors) == 1 + len(config["keywords"]) else 0


if __name__ == "__main__":
    sys.exit(main())
