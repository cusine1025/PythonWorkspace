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
        
        """
        자주차의 센서 정보를 바탕으로 조향과 속도를 결정하는 함수
        t: 주행 시점으로부터의 시간 (초)
		frontImage: 전면 카메라 이미지
		rearImage: 후면 카메라 이미지
		frontLidar: 전면 거리 센서 (mm), 0은 오류를 의미함
		rearLidar: 후면 거리 센서 (mm), 0은 오류를 의미함
        """

        # [1] 라이다 처리
        # frontLines, frontObject = self.processFront(frontImage)
        # reds = frontObject[0]
        # canny 이미지 보기
        canny = self.canny(frontImage)
        self.imshow('canny', canny)

        # 차선 정보 파악
        V, L, R = self.gridFront(frontImage, cols=80, rows=40)
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
        
        steer =5
        
        if L[2] < 320 :
            steer = 30 + 5

        if R[2] < 321 :
            steer = -30 +5    


        if V[4] < 60:
            steer = -80 +5 #지금 곡선 커브를 돌고 있는 것은 다 직선보정 덕분, 이 알고리즘을 정말 사용하려면 코드의 개작 필수

        elif V[5] < 30: 
            steer = - (120 - V[5]) +5

        if V[2] < 60:
            steer = 80 +5

        elif V[1] < 30:
            steer = 120 - V[1] +5   
          
        if V[3] < 180 :
            if L[1] == 320 and R[1] == 321:
                steer = 5
            elif L[1] != 320 or R[1] !=321: 

                change = V[4] - V[3]
                if -1 <= change - (V[5] - V[4]) <= 1 :
                    
                    if R[1] == 321 :
                        steer = 100 + 5    #200 - V[3] +5
                    if L[1] == 320 :
                        steer = -100 +5    #- (200 - V[3]) +5  #차선 하나 안밟고 깔끔
                    if L[1] < 320 and R[1] < 321:
                        if change > 0 :
                            steer = 100 // change #change => 기울기
                        if change < 0 :
                            steer = -100 // change
                        
        # if not stop:
        #     if reds:
        #         redCnt += 1
        #     else:
        #         redCnt =0

        #     if redCnt >=1:
        #         greenCnt =0
        #         stop = True

        # if stop:
        #     if greenCnt >= [0]:
        #         redCnt =0

        # if 0 < redCnt < 500:
        #     stop=True

        # if 0 < greenCnt < 500:
        #     stop = False


        # if stop:
        #     print('Light stop!!!','Red Cnt',redCnt, 'Green Cnt=',greenCnt)
        #     return 0, 0
                
        
        velocity = 60

        if steer > 100 +5 :
            steer = 100 +5
        if steer < -100 +5 :
            steer = -100 +5

        if 0< frontLidar < 100 :
            velocity = 0
       

        print ('L[0]=', L[0], 'L[1]=', L[1], 'L[2]=', L[2], end="  //  ")
        print ('R[0]=', R[0], 'R[1]=', R[1], 'R[2]=', R[2])
        print ('V[0]=', V[0], 'V[1]=', V[1], 'V[2]=', V[2], 'V[3]=', V[3], 'V[4]=', V[4], 'V[5]=', V[5], 'V[6]=', V[6])
        print('frontLidar=', frontLidar, end="..//..")
        print('rearLidar=', rearLidar, end="       => => =>    ")
        #print('[e=', e,-+-+ end="]  ")
        print('[steer=', steer, end="]  ")
        print('[velocity=', velocity, "]")
        print()

        self.vars.steer = steer
        self.vars.velocity = velocity
        return self.vars.steer, self.vars.velocity



if __name__ == "__main__":
    g = Graphics(Planning)  # 자주차 컨트롤러 실행
    g.root.mainloop()  # 클릭 이벤트 처리
    g.exit()  # 자주차 컨트롤러 종료
