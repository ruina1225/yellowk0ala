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
        guest = self.callGuest()
        self.ask(guest)
        self.calculate(guest)
        self.tellresult(guest)   # ✅ 오타 수정

    def callGuest(self):
        return Guest()
    
    def ask(self, guest):
        guest.tell()

    def calculate(self, guest):
        h = guest.height / 100
        guest.bmi = guest.weight / (h * h)
        if guest.bmi >= 39:
            guest.result = "고도비만"
        elif guest.bmi >= 32:
            guest.result = "중도비만"
        elif guest.bmi >= 25:
            guest.result = "과체중"
        elif guest.bmi >= 18.5:
            guest.result = "정상"
        else:
            guest.result = "저체중"

    def tellresult(self, guest):   # ✅ 이름 맞춤
        print("BMI : %.1f" % guest.bmi)
        print("%s씨는 %s" % (guest.name, guest.result))

# 손님
class Guest:
    def tell(self):
        self.name = input("이름 : ")
        self.height = float(input("키(cm) : "))      # ✅ 숫자 변환
        self.weight = float(input("몸무게(kg) : "))  # ✅ 숫자 변환
    
###############################
d = Doctor()
d.start()

# 왜 안되지 vscode????????????