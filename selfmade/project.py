word_list = {
    'apple' : ['사과', ],
    'banana' : ['바나나', ],
    'canada' : ['캐나다', ],
    'doctor' : ['의사', ]
    }
count = 0
for i in word_list:
    text = '{}의 뜻은?'.format(i)
    answer = input(text)
    if answer == word_list[i][0]:
        print('정답입니다')
        count += 1
        print('지금까지 맞춘 개수 :', count)
        reply = input('계속하기 - yes : ')

        if reply == 'yes':
            continue
        else:
            break
    else:
        print('오답입니다')
        enumerate