#트킨터 import
from tkinter import *
import random
import tkinter.font as tkFont
# 프로그램 창 만들기
root = Tk()
root.title("자리 배치 프로그램")

root.geometry("2560x1600+0+0")

# 반 이름 리스트 선언(여자, 남자)
list1_1_w = [
'1. 강지선',
'2. 김민서',
'3. 김서윤',
'4. 김성은',
'5. 김은재',
'6. 김하원',
'7. 박시아',
'8. 성수연',
'9. 양수빈',
'10. 이단주',
'11. 이서하',
'12. 이채민',
'13. 조서현',
'14. 최유진',
'15. 최은서',
'16. 한지연']
list1_1_m =[
'17. 강현구',
'18. 김동환',
'19. 김우진',
'20. 김은수',
'21. 김현',
'22. 문상서',
'23. 박승민',
'24. 서현성',
'25. 신현우',
'26. 유태민',
'27. 윤영각',
'28. 임주환',
'29. 최동주']

# 전체 좌석수 지정 (6열 5행)
global row_range
row_range = range(0,5)
global column_range
column_range = range(0,6)

class RandomSeats:
    
    def __init__(self, list_w,list_m):

        # 남자 리스트, 여자 리스트 필수로 불러오기
        self.list_m = list_m
        self.list_w = list_w

        # text 하나하나 좌표마다 지정하기 위한 반복문
        for repeat_row in row_range:

            for repeat_col in column_range:
                globals()['text{},{}'.format(repeat_row, repeat_col)] = StringVar()

        # 라벨 하나하나 지정
        for repeat_row in row_range:

            for repeat_col in column_range:
                globals()['lab{},{}'.format(repeat_row,repeat_col)] = \
                Label(root, textvariable= globals()['text{},{}'.format(repeat_row,repeat_col)],font = tkFont.Font(size = 20, weight = "bold"))\
                .grid(row = repeat_row, column = repeat_col, padx = 70, pady = 50)

    def changeText(self):

        # 리스트 각각 섞기
        random.shuffle(self.list_m)
        random.shuffle(self.list_w)
        
        # 반복할 때 카운트 (man, woman)
        m = 0
        w = 0

        #왼쪽 좌석과 오른쪽 좌석 배치
        left = [0,2,4]
        right = [1,3,5]
   
        # try구문을 이용하여 사람 수가 적어 indexing 오류가 발생해도 무시
        try:

            # 나머지 자리 추가(여 to 남)
            leftover_seats(self.list_w, self.list_m)

            for repeat_row in row_range:

                for repeat_col in left:
                    globals()['text{},{}'.format(repeat_row, repeat_col)].set(self.list_w[w])
                    w += 1

            
                
        except:
            pass

        try:

            # 나머지 자리 추가
            leftover_seats(self.list_m, self.list_w)

            for repeat_row in row_range:

                for repeat_col in right:

                    globals()['text{},{}'.format(repeat_row, repeat_col)].set(self.list_m[m])
                    m += 1

        except:
            pass

def leftover_seats(l_1, l_2):
        # l_1을 기준으로 넘으면 l_2로 옮김
        while len(l_1) > 15:

                l_2.append(l_1[-1])
                del l_1[-1]

# 클래스 선언
class_101 = RandomSeats(list1_1_w,list1_1_m)

# 뽑기 버튼
btn = Button(root, padx = 10, pady = 5, text = "랜덤뽑기", command = class_101.changeText)
btn.place(x = 0, y = 0)
root.mainloop()