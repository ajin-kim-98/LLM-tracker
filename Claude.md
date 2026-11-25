# 윈터딜

겨울옷 할인 소식(뽐뿌 핫딜 + Google 뉴스)을 15분마다 모아 최신순으로 보여주는 정적 사이트.

## 먼저 읽을 문서
- [docs/PRD.md](docs/PRD.md): 무엇을 만드는지, 제외할 것, 완료 기준. 기능을 추가하거나 바꾸기 전에 확인한다.
- [docs/DESIGN.md](docs/DESIGN.md): 색, 글자 크기, 레이아웃 규칙. 화면을 고칠 때는 이 문서의 토큰만 쓴다.

## 구조
- `config.json`: 추적 키워드, 뉴스 필수 단어(할인/세일/특가), 보관 기간, 최대 개수
- `scripts/collect.py`: RSS 수집 → 필터 → `site/deals.json` 저장 (표준 라이브러리만 사용)
- `site/index.html`: `deals.json`을 읽어 그리는 단일 페이지 (빌드 없음, CSS/JS 인라인)
- `tests/test_collect.py`: PRD 완료 기준 테스트
- `.github/workflows/collect.yml`: 15분 cron → 테스트 → 수집 → deals.json 커밋 → GitHub Pages 배포

## 명령
- 테스트: `python -m unittest discover -s tests -v`
- 수집: `python scripts/collect.py`
- 로컬 미리보기: `python -m http.server 8000 -d site` 후 http://localhost:8000
  (`file://`로 열면 fetch가 막혀서 데이터가 안 보인다)

## 규칙
- 가격은 글 제목에 적힌 값만 쓴다. 없으면 `null`로 두고 화면에는 "가격 정보 없음"으로 표시한다. 추정하거나 지어내지 않는다.
- PRD의 제외 요소(로그인, 댓글, 공유, 쇼핑몰 가격 추적, 최저가 비교, 알림)는 만들지 않는다.
- 외부 패키지를 추가하지 않는다. 의존성이 꼭 필요하면 먼저 물어본다.
- 화면 글자는 `textContent`로 넣는다(`innerHTML` 금지). 링크는 http/https만 허용한다.
- DESIGN.md에 없는 색, 그림자, 그라디언트, 이모지는 쓰지 않는다.
- 필터 로직을 바꾸면 테스트도 함께 고치고 통과를 확인한다.
