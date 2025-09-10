#25/03/24 
# 1) 의뢰인 : 초딩 내 동생 -> 뭘 그렇게 잘해줄 필요 있나
# 2) Python : OOP가 완전 필수는 아니고..
 
####################################
# x : 
# y : 
# ----------------
#
####################################
# exception 예제
# 수학에서 나누기 0은 없음
# 그걸 내 동생이 몰랐음 -> 나누기 0 시도하다가 실패
# -> 나한테 와서 성질을 냄
# exception Handling
#   성질 못내게 대비책을 마련해놓자
#   문제 생길만한거를 파악해서 대비책을 마련해놓자
#       Java : 처리를 안해놓으면 error 가 뜸
#       Python (자유의 언어) : 하든말든 

# try : 
#       일단 여기를 실행
# except 예외이름 as 별칭: 
#       별칭의 예외사의가
#       그 문제가 발생하면 여기가 실행
# except 예외이름: 
#       문제가 발생하면 여기가 실행
# ...
#  else:
#       아무 문제도 없었으면 여기가 실행
#  finally:
#       문제가 있었든 없었든 무조건 실행 + return 보다 먼저 실행





x = int(input("x : "))
y = int(input("y : "))
# a = x + y 
# b = x - y
# c = x * y

# try:
#     d = x / y
#     print("-------")
#     print(d)
    
#     e = [54, 123, 3]
#     print(e[y])

# except ZeroDivisionError:   
#     print("나누기 0은 없다")

# except IndexError:
#     print("리스트에 그거 없다")

try:
    d = x / y
    print("-------")
    print(d)
    e = [54, 123, 3]
    print(e[y])
except Exception as e:
    print(e) # 개발하는 동안..., 개발종료 때 지우고**
    print("어쨌든 잘못됨")
else:
    print("문제 없었음")
finally:
    print("문제발생여부 상관없이 어쨌든 실행???")


# Avengers 로 부터 상속받는 Ironman
#  Exception으로부터 상속받는 IndexError

#   polymorphism(다형성)
#       상위타입(Animal)변수에 하위타입(Dog)데이터 넣는게 가능

#   Python] 
#    Python은 다 객체
#    Python 모든 변수의 자료형 : object
#    상위타입(object) 변수에 하위타입(Dog, str, int, ...)
#       -> 다형성을 늘 써왔음

a = 10 
print(a, type(a))
a = 'ㅋ'
print(a, type(a))


# 다시 한번 공부하세요