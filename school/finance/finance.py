from currency_converter import CurrencyConverter
c = CurrencyConverter()

a = input("기존 화폐의 종류 : ")
amount = int(input('화폐의 양 : '))
b = input("변환할 화폐의 종류 : ")

print('직접 재정환율을 계산하였을 때의 환율 : ')
first = c.convert(amount, a, 'USD')

print('기존 화폐 -> 미국 달러 : ' + str(first))
second = c.convert(first, 'USD', b)
print('미국 달러 -> 변환할 화폐 : ' + str(second))

print()
print('바로 환율을 계산하였을 때의 환율 : ')
direct = c.convert(amount, a, b)
print('기존 화폐 -> 변환할 화폐 : ' + str(direct))