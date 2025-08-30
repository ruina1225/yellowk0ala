# OOP? : 실생활묘사
# OOD(Desing)
#   1) 실제로 비만도검사 센터에 가서 검사받는 상활을 생각
#       손님이 비만도검사 센터에 간다
#       손님이 의사에게 이름, 키, 몸무게를 말한다
#       의사가 측정한다
#   2) 등장인물: 프로그램에 필요한 것만 남긴다
#   3) 속성 : 프로그램에 필요한 것만 남긴다
#   4) 상황 진행 -> 액션
#   5) ㄱㄱ (최대한 실생활스럽게)

# *************
# 멤버변수 : 의사가 자기소개할때 할만한 얘기
# 지역변수 : 메소드 진행중에만 쓰고 버릴
# 파라메터
# 리턴

# 의사
class Doctor:
    def start(self):
        guest = self.callGuest() # -> 손님은 업무중에만 필요한거니까 지역변수
        self.ask(guest)
        self.calculate(guest)
        self.tellResult(guest)

    def callGuest(self): # -> 의사입장에서 손님을 부르면 뭐가 남나?
        return Guest()  # -> 손님이 들어옴
    
    def ask(self, guest):
        guest.tell()

    def calculate(self, guest):
        h = guest.height / 100
        guest.bmi = guest.weight / (h * h)
        
        if guest.bmi >= 39:
            guest.result = "고도 비만"
        elif guest.bmi >= 32:
            guest.result = "중도 비만"
            
    def tellResult(self, guest):
        print("BMI : %.1f" % guest.bmi)
        print("%s씨는 %s" % (guest.name, guest.result))

# 손님
class Guest:
    def tell(self):
        self.name = input("이름: ")
        self.height = float(input("키: "))
        self.weight = float(input("몸무게: "))

    # 21번줄을 만들어보니 아래 내용을 쓸수 없어
    # def __init__(self, name, height, weight):
    #     self.name = name
    #     self.height = height
    #     self.weight = weight
########################################
d = Doctor() # 의사 출근
d.start()

# 다시 풀어 보세요 
