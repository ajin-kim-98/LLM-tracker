# 윈터딜

뽐뿌 핫딜과 Google 뉴스에서 유니클로, 노스페이스, 무신사, 패딩 할인 소식을 15분마다 모아 최신순으로 보여주는 페이지.

- 기획: [docs/PRD.md](docs/PRD.md)
- 디자인: [docs/DESIGN.md](docs/DESIGN.md)

## 로컬에서 실행

```bash
python scripts/collect.py                 # site/deals.json 생성
python -m http.server 8000 -d site        # http://localhost:8000
python -m unittest discover -s tests -v   # 테스트
```

키워드는 `config.json`에서 바꾼다.

## 배포

GitHub Actions가 15분마다 수집한 뒤 GitHub Pages에 배포한다.
저장소 Settings → Pages → Source를 **GitHub Actions**로 설정해야 한다.
