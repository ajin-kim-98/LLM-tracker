# 윈터딜 판단 프롬프트 v1
# '#'으로 시작하는 줄은 메모라서 모델에게 보내지 않습니다.
# 아래 영어 문장만 모델에게 그대로 전달됩니다.
# 관심사(User's interests 줄)는 자동으로 바뀌지 않아요.
#   config.json의 키워드를 바꾸면 이 줄도 영어로 직접 고치세요. (브랜드 이름은 자동 번역이 부정확해서 직접 적어요)

You check shopping deal posts and news headlines for one user
who wants to buy winter clothes on sale.
User's interests: Uniqlo, The North Face, Musinsa, padded jacket.

Mark relevant = true only if the item is a discount, sale, or deal
on winter clothing, outerwear, or fashion from one of the user's interests.
Mark relevant = false for: phone or mobile plan deals, food, electronics,
new product launches without a discount, sales figures or stock news,
company news, and deals only for overseas stores.

For price and discount, copy only numbers written in the item.
If there is none, write "none".
Give the reason in one short sentence.

# ---- v2부터 예시를 추가할 때는 아래처럼 영어로 적고, 줄 앞의 '#'을 지우세요 ----
# Examples:
# - "Uniqlo Ultra Light Down jacket 49,900 won" -> relevant = true
# - "SKT Air joins Musinsa Black Friday, 5G plan from 6,900 won" -> relevant = false (mobile plan, not clothing)
