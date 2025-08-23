from random import randint

turn = 0 
def getUserAns():
    userAns = int(input("뭐 : "))
    if 0 < userAns < 10001:
        return userAns
    return getUserAns()

def pickGameAns():
    return randint(1, 10000)

def judge(userAns, gameAns):
    global turn
    turn += 1
    if userAns == gameAns:
        print("%d번만에 정답" % turn)
        return False
    elif userAns == gameAns:
        print("DOWN")
    else:
        print("up")
    return True

gameAns = pickGameAns()

while True:
    userAns = getUserAns()
    go = judge(userAns, gameAns)
    if not go:
        break
