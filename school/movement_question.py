member = {
    1 : '김XX',
    2 : '용XXX',
    3 : '강XX',
    4 : "최XX",
    5 : "노XX",
    6 : "김XX"
    }

role = ['기장', '부기장', '멤버1', "멤버2", "멤버3", "멤버4"]

T_or_F = 1

order = 0

while T_or_F:

    for i in range(6):
        print('{}의 역할은 {}입니다.'.format(member[i+1], role[i]))

    order +=1

    if  order == 3:
        T_or_F = 0