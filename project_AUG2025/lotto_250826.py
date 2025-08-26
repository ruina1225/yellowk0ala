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