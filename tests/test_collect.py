import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from collect import extract_price, filter_items, merge, parse_google_news, parse_ppomppu  # noqa: E402

KEYWORDS = ["유니클로", "노스페이스", "무신사", "패딩"]
SALE_WORDS = ["할인", "세일", "특가"]

PPOMPPU_XML = """<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0"><channel>
<item><title>[유니클로] 울트라라이트다운 패딩 (49,900원/무료)</title>
<link>http://www.ppomppu.co.kr/zboard/view.php?id=ppomppu&amp;no=1</link>
<pubDate>Wed, 25 Nov 2026 08:00:00 GMT</pubDate></item>
<item><title>[11번가] 오리온 고구마칩 56g 10개 (12,610원/무료)</title>
<link>http://www.ppomppu.co.kr/zboard/view.php?id=ppomppu&amp;no=2</link>
<pubDate>Wed, 25 Nov 2026 07:00:00 GMT</pubDate></item>
<item><title>[무신사] 겨울 아우터 기획전 쿠폰</title>
<link>http://www.ppomppu.co.kr/zboard/view.php?id=ppomppu&amp;no=3</link>
<pubDate>Wed, 25 Nov 2026 06:00:00 GMT</pubDate></item>
</channel></rss>"""

NEWS_XML = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel>
<item><title>노스페이스 눕시 최대 30% 할인 - 한국경제</title>
<link>https://news.google.com/rss/articles/a</link>
<pubDate>Wed, 25 Nov 2026 07:30:00 GMT</pubDate>
<source url="https://www.hankyung.com">한국경제</source></item>
<item><title>패딩 판매량 전년 대비 증가 - 연합뉴스</title>
<link>https://news.google.com/rss/articles/b</link>
<pubDate>Wed, 25 Nov 2026 05:00:00 GMT</pubDate>
<source url="https://www.yna.co.kr">연합뉴스</source></item>
</channel></rss>"""


class AcceptanceTest(unittest.TestCase):
    """PRD 완료 기준: 핫딜 3건 + 뉴스 2건 중 맞는 3건만 최신순으로."""

    def test_only_matching_three_in_latest_order(self):
        raw = parse_ppomppu(PPOMPPU_XML) + parse_google_news(NEWS_XML)
        self.assertEqual(len(raw), 5)
        result = filter_items(raw, KEYWORDS, SALE_WORDS)
        self.assertEqual([r["title"] for r in result], [
            "[유니클로] 울트라라이트다운 패딩 (49,900원/무료)",
            "노스페이스 눕시 최대 30% 할인",
            "[무신사] 겨울 아우터 기획전 쿠폰",
        ])
        for r in result:
            self.assertTrue(r["source"])
            self.assertTrue(r["link"].startswith("http"))

    def test_price_not_invented(self):
        result = filter_items(parse_ppomppu(PPOMPPU_XML) + parse_google_news(NEWS_XML),
                              KEYWORDS, SALE_WORDS)
        prices = {r["title"]: r["price"] for r in result}
        self.assertEqual(prices["[유니클로] 울트라라이트다운 패딩 (49,900원/무료)"], "49,900원")
        self.assertIsNone(prices["노스페이스 눕시 최대 30% 할인"])
        self.assertIsNone(prices["[무신사] 겨울 아우터 기획전 쿠폰"])


class PriceTest(unittest.TestCase):
    def test_formats(self):
        self.assertEqual(extract_price("패딩 (12,610원/무료)"), "12,610원")
        self.assertEqual(extract_price("패딩 9900원"), "9900원")
        self.assertEqual(extract_price("패딩 9.9만 원"), "9.9만원")
        self.assertIsNone(extract_price("패딩 최대 60% 할인"))


class MergeTest(unittest.TestCase):
    def test_dedupe_and_expire(self):
        now = datetime(2026, 11, 25, tzinfo=timezone.utc)
        old = [
            {"link": "a", "title": "old a", "published_at": "2026-11-24T00:00:00+00:00"},
            {"link": "x", "title": "expired", "published_at": "2026-10-01T00:00:00+00:00"},
        ]
        new = [{"link": "a", "title": "new a", "published_at": "2026-11-24T00:00:00+00:00"}]
        result = merge(old, new, keep_days=14, max_items=100, now=now)
        self.assertEqual([r["title"] for r in result], ["new a"])

    def test_same_title_different_link_keeps_latest(self):
        now = datetime(2026, 11, 25, tzinfo=timezone.utc)
        old = [{"link": "n1", "title": "'에어' 5G 특가…SKT, 무신사 블프 참여",
                "published_at": "2026-11-24T01:00:00+00:00"}]
        new = [
            {"link": "n2", "title": "‘에어’ 5G 특가...SKT, 무신사 블프 참여",
             "published_at": "2026-11-24T03:00:00+00:00"},
            {"link": "n3", "title": "유니클로 패딩 할인",
             "published_at": "2026-11-24T02:00:00+00:00"},
        ]
        result = merge(old, new, keep_days=14, max_items=100, now=now)
        self.assertEqual([r["link"] for r in result], ["n2", "n3"])


if __name__ == "__main__":
    unittest.main()
