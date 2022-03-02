mode = input('사용하실 사칙연산을 입력해주세요 : ')
input_first = int(input('첫번째 숫자를 입력해주세요 : '))
input_second = int(input('두번째 숫자를 입력해주세요 : '))


class FourCal:
    def __init__(self, first, second):
        self.first = first
        self.second = second
    def setdata(self, first, second):
        self.first = first
        self.second = second
    def add(self):
        result = self.first + self.second
        return result
    def mul(self):
         result = self.first * self.second
         return result
    def sub(self):
         result = self.first - self.second
         return result
    def div(self):
         result = self.first / self.second
         return result

a = FourCal(input_first, input_second)

if mode == '나누기' :
    print(a.div())
elif mode == '빼기':
    print(a.sub())
elif mode == '더하기':
    print(a.add())
elif mode == '곱하기' :
    print(a.mul())
else :
    print('잘못된 사칙연산입니다. 다시 시도해주세요.')