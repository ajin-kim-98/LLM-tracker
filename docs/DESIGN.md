---
version: alpha
name: 윈터딜
description: 겨울옷 할인 소식 tracker의 디자인 규칙. 무채색 바탕에 청록 강조색 하나, 최신 1건만 크게, 나머지는 구분선 목록.
colors:
  primary: "#287A74"
  primary-hover: "#1F625D"
  on-primary: "#ffffff"
  accent-line: "#55A9A0"
  highlight: "#AEEED3"
  badge: "#FFF8B0"
  background: "#ffffff"
  surface: "#f5f5f7"
  text: "#1d1d1f"
  text-secondary: "#6e6e73"
  border: "#d2d2d7"
typography:
  headline-featured:
    fontFamily: -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", "Malgun Gothic", "Helvetica Neue", Arial, sans-serif
    fontSize: 32px
    fontWeight: 700
    lineHeight: 1.25
    letterSpacing: 0em
  price-featured:
    fontFamily: -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", "Malgun Gothic", "Helvetica Neue", Arial, sans-serif
    fontSize: 28px
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: 0em
  title-section:
    fontFamily: -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", "Malgun Gothic", "Helvetica Neue", Arial, sans-serif
    fontSize: 21px
    fontWeight: 700
    lineHeight: 1.3
    letterSpacing: 0em
  title-item:
    fontFamily: -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", "Malgun Gothic", "Helvetica Neue", Arial, sans-serif
    fontSize: 17px
    fontWeight: 600
    lineHeight: 1.4
    letterSpacing: 0em
  price:
    fontFamily: -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", "Malgun Gothic", "Helvetica Neue", Arial, sans-serif
    fontSize: 17px
    fontWeight: 700
    lineHeight: 1.4
    letterSpacing: 0em
  body:
    fontFamily: -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", "Malgun Gothic", "Helvetica Neue", Arial, sans-serif
    fontSize: 17px
    fontWeight: 400
    lineHeight: 1.53
    letterSpacing: 0em
  meta:
    fontFamily: -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", "Malgun Gothic", "Helvetica Neue", Arial, sans-serif
    fontSize: 15px
    fontWeight: 400
    lineHeight: 1.4
    letterSpacing: 0em
rounded:
  sm: 8px
  md: 12px
  full: 980px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  xxl: 48px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.body}"
    rounded: "{rounded.full}"
    padding: 12px
  button-primary-hover:
    backgroundColor: "{colors.primary-hover}"
  featured:
    backgroundColor: "{colors.highlight}"
    textColor: "{colors.text}"
    typography: "{typography.headline-featured}"
    rounded: "{rounded.md}"
    padding: 32px
  list-item:
    backgroundColor: "{colors.background}"
    textColor: "{colors.text}"
    typography: "{typography.title-item}"
    padding: 16px
  link:
    textColor: "{colors.primary}"
    typography: "{typography.body}"
  badge:
    backgroundColor: "{colors.badge}"
    textColor: "{colors.text}"
    typography: "{typography.meta}"
    rounded: "{rounded.sm}"
    padding: 4px
  header:
    backgroundColor: "{colors.background}"
    textColor: "{colors.text}"
    typography: "{typography.title-section}"
    height: 56px
  footer:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text-secondary}"
    typography: "{typography.meta}"
---

# 윈터딜

## Overview

겨울옷 할인 소식을 최신순으로 훑어보는 페이지다. 바탕은 무채색이고 강조색은 청록 하나다. 가장 최근 소식 1건만 크게 보여주고, 나머지는 구분선으로 나눈 목록으로 보여준다. 카드, 그림자, 이모지 같은 장식은 쓰지 않고 글자 크기와 여백으로 위계를 만든다.

글자 크기와 여백 체계는 Apple Developer 디자인 페이지를 참고했다. light mode만 다룬다.

## Colors

기본은 무채색이고, 색은 버튼과 중요한 정보에만 쓴다.

**무채색 (화면의 대부분)**
- **background** `#ffffff`: 페이지 배경.
- **surface** `#f5f5f7`: footer 배경.
- **text** `#1d1d1f`: 제목과 본문.
- **text-secondary** `#6e6e73`: 출처, 게시 시각, "가격 정보 없음" 같은 보조 정보.
- **border** `#d2d2d7`: 목록의 1px 구분선.

**강조색 (하나)**
- **primary** `#287A74`: 버튼 배경, 링크, 가격. hover 시 `#1F625D`.

**보조 배경 (같은 청록 계열, 좁은 면적에만)**
- **highlight** `#AEEED3`: featured 블록 배경. 페이지에서 한 곳에만 쓴다.
- **badge** `#FFF8B0`: 뱃지 배경. 꼭 알려야 할 짧은 라벨에만 쓴다.
- **accent-line** `#55A9A0`: featured 블록 왼쪽의 4px 장식선. 글자색으로는 쓰지 않는다.

**허용하는 글자색과 배경 조합 (명암비 4.5:1 이상)**

| 글자 | 배경 | 명암비 |
| --- | --- | --- |
| text `#1d1d1f` | background `#ffffff` | 16.8:1 |
| text-secondary `#6e6e73` | background `#ffffff` | 5.1:1 |
| text-secondary `#6e6e73` | surface `#f5f5f7` | 4.7:1 |
| primary `#287A74` | background `#ffffff` | 5.1:1 |
| on-primary `#ffffff` | primary `#287A74` | 5.1:1 |
| text `#1d1d1f` | highlight `#AEEED3` | 12.8:1 |
| text `#1d1d1f` | badge `#FFF8B0` | 15.5:1 |

**금지하는 조합 (명암비 미달)**
- `#55A9A0` 글자를 흰 배경에 (2.8:1), 또는 흰 글자를 `#55A9A0` 배경에.
- primary `#287A74` 글자를 highlight `#AEEED3` 배경에 (3.9:1).
- text-secondary `#6e6e73` 글자를 highlight `#AEEED3` 배경에 (3.9:1).

따라서 featured 블록 안의 글자는 모두 text `#1d1d1f`로 쓰고, 이동은 텍스트 링크 대신 button-primary로 한다.

## Typography

- 서체는 system font stack이다. Apple 기기에서는 SF가, Windows에서는 맑은 고딕이 나온다.
- 본문은 17px이고, 가장 작은 글씨(meta)도 15px 아래로 내려가지 않는다.
- 모든 글자는 배경과 명암비 4.5:1 이상을 지킨다. 흐린 회색 글씨를 쓰지 않는다.
- 제목은 본문과 확실히 차이 나게 크고 굵게 쓴다.
  - featured 제목: 32px, 700
  - featured 가격: 28px, 700
  - 섹션 제목과 사이트 이름: 21px, 700
  - 목록의 글 제목: 17px, 600
  - 목록의 가격: 17px, 700, primary 색
  - 본문: 17px, 400
  - 출처와 게시 시각: 15px, 400, text-secondary 색
- 모든 글은 왼쪽 정렬한다.
- 한글은 letter-spacing을 0으로 둔다.
- 734px 이하 화면에서는 featured 제목을 26px, featured 가격을 24px로 줄인다.

## Layout

- **콘텐츠 폭**: 가운데 배치, 최대 980px. 1068px 이하에서는 692px, 734px 이하에서는 화면 폭의 87.5%.
- **페이지 구성 순서**:
  1. Header: 왼쪽에 사이트 이름, 그 옆이나 아래에 한 줄 설명.
  2. Featured: 가장 최근 소식 1건. 페이지에서 가장 큰 요소다.
  3. 목록: 섹션 제목 아래에 나머지 소식을 최신순으로 한 줄에 하나씩.
  4. Footer.
- **목록의 한 줄**: 왼쪽에 제목, 그 아래에 출처와 게시 시각. 오른쪽 끝에 가격. 734px 이하에서는 가격이 제목 아래로 내려간다.
- **구분**: 목록의 줄 사이는 1px 구분선(border)과 위아래 `{spacing.md}`(16px) 여백으로 나눈다. 줄마다 카드를 만들지 않는다.
- **여백**: header와 featured 사이 `{spacing.lg}`(24px), featured와 목록 사이 `{spacing.xxl}`(48px), 섹션 제목과 첫 줄 사이 `{spacing.md}`(16px), 제목과 meta 사이 `{spacing.xs}`(4px).
- 여백 값은 4px의 배수만 쓴다.
- 같은 모양의 섹션을 반복하지 않는다. 큰 요소는 featured 하나뿐이다.

## Elevation & Depth

그림자는 쓰지 않는다. 깊이는 featured 블록의 배경색 하나로만 표현한다.

## Shapes

- featured 블록: `{rounded.md}`(12px). 페이지에서 유일한 카드형 요소다.
- 버튼: `{rounded.full}`로 pill 모양.
- 뱃지: `{rounded.sm}`(8px).
- 목록의 줄: 모서리와 배경 없이 아래쪽 구분선만 둔다.

## Components

- **featured**: highlight 배경, 12px 모서리, 32px 안쪽 여백, 왼쪽에 4px accent-line. 구성은 출처와 게시 시각 → 제목 → 가격 → 버튼 순서. 글자는 모두 text 색.
- **list-item**: 배경 없음, 아래 1px 구분선, 위아래 16px 여백. 제목은 원문으로 가는 링크이고 text 색으로 쓰며 hover 시 밑줄을 긋는다. 가격은 primary 색.
- **button-primary**: primary 배경에 흰 글자, pill 모양, 위아래 12px 좌우 22px 여백. 페이지에 하나(featured 안)만 둔다.
- **link**: 본문 안의 링크는 primary 색, hover 시 밑줄.
- **badge**: badge 배경에 text 색 글자, 15px. 한 줄에 최대 하나.
- **header**: 높이 56px, 흰 배경, 아래 1px 구분선.
- **footer**: surface 배경, 15px, text-secondary 색.
- **빈 값**: 가격이 없으면 text-secondary 색으로 "가격 정보 없음"이라고 쓴다.

## Do's and Don'ts

**Do**
- 목록은 구분선과 여백으로 나눈다.
- 카드는 featured처럼 꼭 묶어야 할 때만 쓴다.
- 색은 버튼, 링크, 가격에만 쓴다.
- 가장 중요한 정보 하나만 크게 보여준다.
- 문구에는 숫자, 이름, 상황을 넣어 구체적으로 쓴다. 예: "뽐뿌 핫딜과 Google 뉴스에서 모은 유니클로, 노스페이스, 무신사, 패딩 할인 소식".
- 화면에 나오는 숫자와 가격은 수집한 실제 데이터만 쓴다.

**Don't**
- 모든 항목을 둥근 카드에 넣지 않는다.
- 그림자, 그라디언트, 이모지 아이콘을 쓰지 않는다.
- 파랑, 보라 등 팔레트에 없는 색을 추가하지 않는다. 다크 배경에 네온색도 쓰지 않는다.
- 15px보다 작은 글씨, 명암비 4.5:1 미만의 흐린 글씨를 쓰지 않는다.
- 가운데 제목 아래 카드 3개를 놓는 구성을 쓰지 않는다.
- "혁신", "스마트한 경험" 같은 추상적인 문구와 근거 없는 숫자를 쓰지 않는다.
