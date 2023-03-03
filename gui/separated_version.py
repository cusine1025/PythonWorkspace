#트킨터 import
from audioop import lin2adpcm
from tkinter import *
from tkinter import messagebox
from random import shuffle
import tkinter.font as tkFont
# from winsound import Beep
from time import sleep
# 프로그램 창 만들기
root = Tk()
root.title("자리 배치 프로그램")

# 윈도우의 해상도 값 가져와 전체화면으로 열기
monitor_height = root.winfo_screenheight()
monitor_width = root.winfo_screenwidth()

root.geometry("{}x{}+0+0".format(monitor_width, monitor_height))

# 반 이름 리스트 선언(여자, 남자)
try:
    with open("/list.txt", "r") as file:
        contents = file.read()
    l1 = contents.split(sep = ',')
except:
    messagebox.showerror(title = "오류!",
    message = "list.txt가 같은 파일 안에 있는지 확인해주세요.")
    root.destroy()

class_list = l1
# 전체 좌석수 지정 (6열 5행)
global row_range
row_range = range(0,5)
global column_range
column_range = range(0,6)

class RandomSeats:
    
    def __init__(self, class_list):

        self.class_list = class_list
        # text 하나하나 좌표마다 지정하기 위한 반복문
        for repeat_row in row_range:

            for repeat_col in column_range:
                globals()['text{},{}'.format(repeat_row, repeat_col)] = StringVar()

        # 라벨 하나하나 지정
        for repeat_row in row_range:

            for repeat_col in column_range:
                globals()['lab{},{}'.format(repeat_row,repeat_col)] = \
                Label(root, textvariable= globals()['text{},{}'.format(repeat_row,repeat_col)],
                      font = tkFont.Font(size = 20, weight = "bold"))\
                    .grid(row = repeat_row, column = repeat_col,
                          padx = int(monitor_width//24), pady = int(monitor_height//20) )

    # 텍스트를 바꾸는 함수 지정
    def changeText(self):
        
        try:
            btn.place_forget()

            for repeat_row in row_range:
                for repeat_col in column_range:
                    globals()['text{},{}'.format(repeat_row, repeat_col)].set('')
            root.update()
        except:
            pass

        # 나머지 자리 추가
        # leftover_seats(self.list_m, self.list_w)

        # 리스트 각각 섞기
        
        shuffle(self.class_list)
        
        # 반복할 때 카운트 (man, woman)

        #왼쪽 좌석과 오른쪽 좌석 배치

        for count in [5,4,3,2,1]:

            time_counted = Label(root, text = count, font = tkFont.Font(size = 300, weight = "bold"))
            time_counted.place(relx= 0.4, rely=0.3)
            root.update()
            sleep(1.2)
            time_counted.place_forget()
            root.update()
        iterable = 0

        try:
        
            for repeat_row in row_range:

                for repeat_col in column_range:
                    globals()['text{},{}'.format(repeat_row, repeat_col)].set(self.class_list[iterable])
                    iterable += 1
            root.update()

    
                
        except:
            pass
        # btn.place(relx = 0.38, rely = 0.85)
        # btn.config(text = '다시뽑기')


# 클래스 선언
haneul = RandomSeats(class_list)

# copyright
copyright = Label(root, text = 'Made by 11기 김우진', font = tkFont.Font(size = 16, weight = 'bold', slant = 'italic'))
copyright.place(relx = 0.85, rely = 0.95)
# 뽑기 버튼
btn = Button(root, padx = 30, pady = 10, text = "랜덤뽑기", 
             font = tkFont.Font(size = 40, weight = 'bold'), command = haneul.changeText)
btn.place(relx = 0.38, rely = 0.85)
root.mainloop()