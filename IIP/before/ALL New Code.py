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
        V, L, R = self.gridFront(frontImage, cols=640, rows=320)
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

        steer = 5  #기본 조향       
        velocity = 30
        # 1. 필요없는 점 무시하기 코드
        for i in range (0,21) :
            t = max(V) // 11.5 -1
            if t < 20-i :
                R[i] = "무시"
                L[i] = "무시"
        
        # 2. 중앙보정 21~40까지의 값을 평균내어 직선보정을 하는 방식, 정확성을 높일 수 있음
        total = 0
        ignore = 0
        
        for i in range (11,21):
            
            if R[i] == "무시" or L[i] == "무시" :
                ignore += 1
            
            else:
                center = L[i] - R[i]
                if center == 0:
                    steer = 5   #Keep going
                
                elif center < 0:
                    steer = -center
                
                elif center > 0:
                    steer = -center
            total += steer

        average = total // (10-ignore)
        
        if average != 0:
            steer = average //2 +5
        

        # 3. 커브 코드
        
        #(1) 리스트 나누기 (왼쪽, 오른쪽)
        list_left = V[0:19]
        list_right= V[40:21:-1]

        #(2) 기준점 정하기
        minLeft = min(list_left)
        minRight = min(list_right)
        Idx_L = list_left.index(minLeft)
        Idx_R = list_right.index(minRight)
        Idx_shift_L =  Idx_L
        Idx_shift_R = Idx_R
        
        #(3) 변화하는 곳 찾아서 돌기
        if V[20] < 170: 
        #우회전
            while  V[Idx_shift_L] > V[Idx_L] + 11 * (Idx_shift_L - Idx_L) - 50:
                Idx_shift_L += 1
            if V[10] < V[30]:
                slope_L = (V[Idx_shift_L + 3] -V[Idx_shift_L]) / 3
                steer = (11-slope_L)*90//11 +5

        #좌회전
            while  V[40-Idx_shift_R] > V[40-Idx_R] + 11 * (Idx_shift_R - Idx_R) -50:
                Idx_shift_R += 1
            if V[30] < V[10]:
                slope_R = (V[37-Idx_shift_R] - V[40-Idx_shift_R]) / 3
                steer =  (11-slope_R)*90//11 +5


        # 4. 점선 진입 코드 (점선임을 인식하는 방법 고안 필요)
        if (V[35] - V[37]) // (R[17] - R[15]) < (V[40] - V[38]) // (R[20] - R[18]):
            steer = 100 + 5

        # 5. 속도 조정 코드
        if 0 < steer < 10 :
            velocity = 50

        # 6. 방향타 고장 방지
        if steer > 100 +5 :
            steer = 100 +5
        if steer < -100 +5 :
            steer = -100 +5

        # 7. 보행자 인식 후 멈춤
        if 0< frontLidar < 100 :
            velocity = 0

        print ('L[20]=', L[20], 'L[19]=', L[19], 'L[18]=', L[18], end="  //  ")
        print ('R[20]=', R[20], 'R[19]=', R[19], 'R[18]=', R[18],)
        print ('total=', total, 'average=', average, 'ignore=',ignore)
        print (20-t, "보다 작으면 무시")
        print('벽과의 거리',V[20])
        print ('Idx_L=',Idx_L, 'Idx_R=', Idx_R)
        print ('Idx_shift_L=',Idx_shift_L , 'Idx_shift_R=', Idx_shift_R )
        print ('V[10]=', V[10], 'V[30]=', V[30])
        # print ('V[0]=', V[39], 'V[1]=', V[38],'V[2]=', V[37], 'V[3]=', V[36], 'V[4]=', V[35], 'V[5]=', V[34], 'V[6]=',)
        # print('frontLidar=', frontLidar, end="..//..")
        # print('rearLidar=', rearLidar, end="       => => =>    ")
        print('[steer=', steer, end="]  ")
        print('[velocity=', velocity, "]")
        print()

        self.vars.steer = steer
        self.vars.velocity = velocity

        # self.vars.redCnt = redCnt  # 변수 설정
        # self.vars.greenCnt = greenCnt  # 변수 설정
        # self.vars.stop = stop
        return self.vars.steer, self.vars.velocity



if __name__ == "__main__":
    g = Graphics(Planning)  # 자주차 컨트롤러 실행
    g.root.mainloop()  # 클릭 이벤트 처리
    g.exit()  # 자주차 컨트롤러 종료