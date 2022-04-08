from jajucha.planning import BasePlanning
from jajucha.graphics import Graphics
from jajucha.control import mtx
import cv2
import numpy as np
import time




class Planning(BasePlanning):
    def __init__(self, graphics):
        super().__init__(graphics)
        # --------------------------- #
        self.vars.redCnt = 0  # 변수 설정
        self.vars.greenCnt = 0  # 변수 설정
        self.vars.stop = True
        self.vars.steer = 0
        self.vars.velocity = 0
        

    def process(self, t, frontImage, rearImage, frontLidar, rearLidar):
        
        
        # 자주차의 센서 정보를 바탕으로 조향과 속도를 결정하는 함수
        # t: 주행 시점으로부터의 시간 (초)
		# frontImage: 전면 카메라 이미지
		# rearImage: 후면 카메라 이미지
		# frontLidar: 전면 거리 센서 (mm), 0은 오류를 의미함
		# rearLidar: 후면 거리 센서 (mm), 0은 오류를 의미함
        

        # [1] 라이다 처리

        # canny 이미지 보기
        canny = self.canny(frontImage)
        self.imshow('canny', canny)

        # lines, (reds, greens) = self.processFront(frontImage)
        # 차선 정보 파악
        V, L, R = self.gridFront(frontImage, cols=41, rows=21)
        # V, L, R = self.gridFront(frontImage, cols=7, rows=3) : 전방 이미지 행선, 열선 그리기
        # rearV, rearL, rearR = self.gridRear(rearImage, cols=4, rows=6) : 후방 이미지도 가능
        # rows : 행선값  cols : 열선값 (row, column) ex) rows=3 : 행선이 3개이고, 총 4개의 행 칸이 생성
        # L[0], L[1], L[2], R[0], R[1], R[2], V[0]~v[6]

        # 각 변수의 최댓값
        if V[3] == 255:  # V[i]가 잡히지 않은 경우
            ...
        if L[2] == 320:  # L[i]가 잡히지 않은 경우  (중앙 픽셀이 324라서 왼쪽으로 최대 324)
            ...
        if R[2] == 320:  # R[i]가 잡히지 않은 경우  (중앙 픽셀이 324라서 오른쪽으로 최대 315)
            ...

        # [2] 주행 처리

        standard_steer = 5
        steer = standard_steer  #기본 조향       
        velocity = 50
        total_1 = 0
        ignore = 0
           
        # 1. 중앙보정 
        for i in range (20+1):
            if R[i]==316: R[i] = "없음"
            if L[i] ==325: L[i] = "없음"

            if R[i] == "없음" or L[i] == "없음" :
                ignore += 1
            else:
                center = L[i] - R[i]
                if center == 0:
                    total_1 +=0 #standard_steer   #Keep going
                
                elif center < 0:
                    total_1 += -center #+standard_steer
                
                elif center > 0:
                    total_1 += -center #+standard_steer
        
            if ignore == 21: 
                steer = standard_steer
        
            else: 
                average = total_1 // (21-ignore)
                steer = average // 5 +standard_steer
        
        # 4. 커브 코드
        #(1) 리스트 나누기 (왼쪽, 오른쪽)
        list_left = V[0:19]
        list_right= V[40:21:-1]
        R_remove = R
        num1 =R_remove.count("없음")
        for delete1 in range(num1):
            R_remove.remove("없음")
        L_remove = L
        num2 =L_remove.count("없음")
        for delete2 in range(num2):
            L_remove.remove("없음")

        #(2) 기준점 정하기
        minLeft = min(list_left)
        minRight = min(list_right)
        Idx_L = list_left.index(minLeft)
        Idx_R = list_right.index(minRight)
        Idx_shift_L =  Idx_L
        Idx_shift_R = Idx_R
        L_left_min = min(L_remove)
        R_right_min = min(R_remove)
        L_index = L.index(L_left_min)
        R_index = R.index(R_right_min)
        angle_L = "미감지"
        angle_R = "미감지"
        slope_L = "미감지"
        slope_R = "미감지"
        

        #(3) 변화하는 곳 찾아서 돌기
        if V[20] < 200: 
        #우회전
            velocity = 40
            while  V[Idx_shift_L] > V[Idx_L] + 11 * (Idx_shift_L - Idx_L) -30 and Idx_shift_L < 19:
                Idx_shift_L += 1
            if L.count("없음") < R.count("없음") and V[Idx_shift_L] > V[Idx_L]:
                slope_L = (V[Idx_shift_L + 3] -V[Idx_shift_L]) / 3
                angle_L= np.arctan(slope_L/6)*180//3.14
                steer = int (90-angle_L) +standard_steer #+10 
                if V[10] < 70: steer = 100 +standard_steer

        #좌회전
            while  V[40-Idx_shift_R] > V[40-Idx_R] + 11 * (Idx_shift_R - Idx_R) -30 and Idx_shift_R < 19:
                Idx_shift_R += 1
            if L.count("없음") > R.count("없음") and V[40-Idx_shift_R] > V[40-Idx_R]:
                slope_R = (V[37-Idx_shift_R] - V[40-Idx_shift_R]) / 3
                angle_R = np.arctan(slope_R/6)*180//3.14
                steer =  int (angle_R - 90) +standard_steer #- 10
                if V[35] < 60 : steer = -100 +standard_steer

       # 5. 삼거리 회전
            if L.count("없음") >= 10: #and V.count(255) >= 3 :
                velocity = 70
                bunmo= V[20] // 10
                if V.count(255) >= 4 and L.count("없음") <= 16: steer =  -50 - 600 // bunmo + standard_steer
                elif Idx_L >= 15: steer = -70 - 600 // bunmo + standard_steer
                elif Idx_L >= 3 and V[20] < 200: steer = -70 - 600 //bunmo +standard_steer

       # 6. 속도 조정 코드
        if -20 + standard_steer < steer < 20 + standard_steer :
            velocity = 50

        # 7. 방향타 고장 방지
        if steer > 100 + standard_steer :
            steer = 100 + standard_steer
        if steer < -100 + standard_steer :
            steer = -100 + standard_steer

        # 8. 보행자 인식 후 멈춤
        if 0< frontLidar < 100 :
            velocity = 0
        velocity = 0

        print('[steer=', steer, end="]  ")
        print('[velocity=', velocity, "]")
        print()

        self.vars.steer = steer
        self.vars.velocity = velocity

        # self.vars.redCnt = redCnt  # 변수 설정
        # self.vars.greenCnt = greenCnt  # 변수 설정
        # self.vars.stop = stop
        return self.vars.steer, self.vars.velocity #self.vars.redCnt, self.vars.greenCnt, self.vars.stop



if __name__ == "__main__":
    g = Graphics(Planning)  # 자주차 컨트롤러 실행
    g.root.mainloop()  # 클릭 이벤트 처리
    g.exit()  # 자주차 컨트롤러 종료