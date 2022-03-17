from bdb import Breakpoint
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

        steer = 5  #기본 조향       
        velocity = 15
        LR_index_reversed = max(V) // 11.5 -1 # 255 나누기 22 11.5 -1 끝을 셀때 인덱스 오류가 나서 -1을 해줌
        # 1. 필요없는 점 무시하기 코드
        for i in range (0,20 + 1) : # 앞서 t

            if LR_index_reversed < 20-i : # 20-i 실전 좌표 순서가 뒤바뀌어 있어 작성해줌.
                R[i] = "무시"
                L[i] = "무시"
            else:
                if 321 <= R[i] <= 322: R[i] = "없음"
                if L[i] == 320: L[i] = "없음"

        # 2. 중앙보정 11~20 까지의 값을 평균내어 직선보정을 하는 방식, 정확성을 높일 수 있음
        # 없음 처리 겹침
        total = 0
        ignore = 0
        
        for i in range (11,20 + 1):

            if R[i] == "무시" or L[i] == "무시" :
                ignore += 1
            elif R[i] == "없음" or L[i] == "없음" :
                ignore += 1
            else:
                center = L[i] - R[i]
                if center == 0:
                    steer = 5   #기본값
                
                elif center < 0:
                    steer = R[i] - L[i] + 5
                
                elif center > 0:
                    steer = L[i] - R[i] + 5
            total = total + steer # 모든 steer값을 다 더한 것
        
        if ignore == 10: 
            average = 0
        
        else: average = total // (10-ignore)
        
        steer = average //5 #너무 크게 돌아 나누기 5를 해줌
        

        # 3. 커브 코드
        
        #(1) 리스트 나누기 (왼쪽, 오른쪽)
        list_left = V[0:19]
        list_right= V[40:21:-1]
        # 중앙을 기준으로 좌우 list를 나눔 (중앙으로 모이는 방향)
        #(2) 기준점 정하기
        minLeft = min(list_left)
        minRight = min(list_right)
        Idx_L = list_left.index(minLeft)
        Idx_R = list_right.index(minRight)
        # 최소가 되는 점을 기준으로 하였음
        Idx_shift_L =  Idx_L
        Idx_shift_R = Idx_R
        angle_L = "미감지"
        angle_R = "미감지"
        slope_L = "미감지"
        slope_R = "미감지"

        #(3) 변화하는 곳 찾아서 돌기
        if V[20] < 200: 
        #우회전
            while  V[Idx_shift_L] > V[Idx_L] + 11 * (Idx_shift_L - Idx_L) -30 and Idx_shift_L <= 19: # 11은 실제 측정한 y의 증가량 (직진으로 갈때)
                # 11로 일정하게 증가하였을 때 여유 y 증가량을 30으로 해줌 (결론적으로 조금 더 가서 잡힘)
                Idx_shift_L += 1
            if L.count("없음") < R.count("없음") and V[Idx_shift_L] > V[Idx_L]: #count로 빈곳을 찾음 and 예외조건이 있어 추가로 넣어줌
                slope_L = (V[Idx_shift_L + 3] -V[Idx_shift_L]) / 3
                angle_L= np.arctan(slope_L/6)*180//3.14
                steer = int (90-angle_L) +5
        #좌회전
            while  V[40-Idx_shift_R] > V[40-Idx_R] + 11 * (Idx_shift_R - Idx_R) -30 and Idx_shift_R < 19:
                Idx_shift_R += 1
            if L.count("없음") > R.count("없음") and V[40-Idx_shift_R] > V[40-Idx_R]:
                slope_R = (V[37-Idx_shift_R] - V[40-Idx_shift_R]) / 3
                angle_R = np.arctan(slope_R/6)*180//3.14
                steer =  int (angle_R - 90) +5

        #(4) 모자라는 회전량 채워주기       
        
            if V[30] < 50 : steer = -100 +5
            if V[10] < 50: steer = 100 +5           


        # 4. 점선 진입 코드 
#        if R[17] == R[15]:
#            R[15] += 1
#        if R[20] == R[18]:
#           R[18] += 1
#        if (V[35] - V[37]) // (R[17] - R[15]) < (V[40] - V[38]) // (R[20] - R[18]):
#            steer = 70 + 5
        # (1) 왼쪽 직선에서 오른쪽 직선 빼기
        # (2) -+        

        # 5. 속도 조정 코드
        # if 0 < steer < 10 :
        #     velocity = 50

        # 6. 방향타 고장 방지
        # if steer > 100 +5 :
        #     steer = 100 +5
        # if steer < -100 +5 :
        #     steer = -100 +5

        # # 7. 보행자 인식 후 멈춤
        # if 0< frontLidar < 100 :
        #     velocity = 0

        # reds, greens = frontObject
        # if reds:
        #     self.vars.redCnt += 1
        # else:
        #     self.vars.redCnt = 0
        # if greens:
        #     self.vars.greenCnt = 0
        # else:
        #     self.vars.greenCnt = 0
        
        # if self.vars.redCnt >= 6:
        #     self.vars.greenCnt = 0
        #     self.vars.stop = True
        #     return 0,0
        # if self.vars.greenCnt >= 2:
        #     self.vars.redCnt = 0
        #     self.vars.stop = False
        
        if self.vars.stop:
            return self.vars.steer, 0

        # print ('L[20]=', L[20], 'L[19]=', L[19], 'L[18]=', L[18], end="  //  ")
        # print ('R[20]=', R[20], 'R[19]=', R[19], 'R[18]=', R[18],)
        print ('V[3]=', V[3])
        print ("slope_L=", slope_L, "slope_R=", slope_R, "angle_L=", angle_L, "angle_R=", angle_R)
        print ("없음인 L 갯수", L.count("없음") , "없음인 R 갯수", R.count("없음"))
        # print ('total=', total, 'average=', average, 'ignore=',ignore)
        # print (20-t, "보다 작으면 무시")
        print('벽과의 거리',V[20])
        print ('Idx_L=',Idx_L, 'Idx_R=', Idx_R)
        print ('Idx_shift_L=',Idx_shift_L , 'Idx_shift_R=', Idx_shift_R )
        print ('V[5]=', V[5], 'V[35]=', V[35])
        # print ('V[0]=', V[39], 'V[1]=', V[38],'V[2]=', V[37], 'V[3]=', V[36], 'V[4]=', V[35], 'V[5]=', V[34], 'V[6]=',)
        # print('frontLidar=', frontLidar, end="..//..")
        # print('rearLidar=', rearLidar, end="       => => =>    ")
        print('[steer=', steer, end="]  ")
        print('[velocity=', velocity, "]")
        print('self.vars.redCnt', self.vars.redCnt)

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