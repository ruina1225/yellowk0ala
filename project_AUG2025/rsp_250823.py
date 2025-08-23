# 가위바위보 게임

# 1) 가위
# 2) 바위
# 3) 보
# ----------------
# 뭐 : 3
# 나 : 보
# 컴 : 바위
# 승
# ----------------
# 뭐 : 3
# 나 : 보
# 컴 : 보
# 무
# ----------------
# ...
# ----------------
# 뭐 : 1
# 나 : 가위
# 컴: 바위
# 패
# 3연승

def printRule(handTable):
    for i in range(len(handTable)):
        if i !=0:
            print("%d) %s" % (i, handTable[i]))
    print("-----")

handTable = [None, "가위", "바위", "보"]

# printRule(handTable)

def userFire():
    userHand = int(input("뭐 : "))
    if 0 < userHand < 4: 
        return userHand
    return userFire()

userFire()