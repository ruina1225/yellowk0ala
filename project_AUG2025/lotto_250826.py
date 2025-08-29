# 로또 게임을 설계해 보자
# lotto 번호 자동 생성기
# set 쓰지말고, list만 쓰기
# 첫번째 숫자 : 그냥 뽑

from random import randint

def pick(i, lotto):
    ball = randint(1, 6)
    for j in range(i):
        if ball == lotto[j]:
            return pick(i, lotto)
    return ball

lotto = []
for i in range(6):
    lotto.append(pick(i, lotto))
print(lotto)

# 재귀 대신 반복문 사용
# 지금은 같은 숫자가 나오면 pick을 재귀 호출하는데, 이 방식도 문제는 없지만 효율성 면에서 불필요하게 깊어질 수 있어요.
# → while 문으로 바꾸면 더 직관적이고 안전합니다.

from random import randint

def pick(lotto):
    while True:
        ball = randint(1, 45)
        if ball not in lotto:
            return ball

# 가장 간단하고 파이썬다운 방법은 아래처럼 random.sample을 사용하는 겁니다.
from random import sample

lotto = sorted(sample(range(1, 46), 6))
print(lotto)

