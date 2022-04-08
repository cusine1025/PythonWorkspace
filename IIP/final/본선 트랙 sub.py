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
        if L[2] == 325:  # L[i]가 잡히지 않은 경우  (중앙 픽셀이 324라서 왼쪽으로 최대 324)
            ...
        if R[2] == 316:  # R[i]가 잡히지 않은 경우  (중앙 픽셀이 324라서 오른쪽으로 최대 315)
            ...

        # # [2] 주행 처리
        # if L[2] < 325:  # L[2]는 잡히고 R[2]는 잡히지 않은 경우
        #     #print ('Left Line', end="// ") 
        #     e = 334 - L[2]

        # # 둘 다 잡히지 않은 경우
        # else:
        #     e = 0
        # #else:
        # #    return self.vars.steer, self.vars.velocity  # 이전 명령

        # #cv2.imshow('Front Grid Image', frontImage)
        # # 왼쪽 차선을 따라 가는 프로그램
        # steer = int(e / 3) - 20  # 계수 1/3, 조정 -20
        # if steer > 100:
        #     steer = 100
        # elif steer < -100:
        #     steer = -100
        standard_steer = 5
        steer = standard_steer
        velocity = 70
        # 오른쪽 차선을 기준으로 왼쪽으로 턴하기
        # junmo = L.count(320)
        # cheondohyun = R.count(321)
        # hyungjoo = V.count(255)

    


        #(1) 리스트 나누기 (왼쪽, 오른쪽)
        list_left = V[0:19]
        list_right= V[40:21:-1]

        #(2) 기준점 정하기
        minLeft = min(list_left)
        Idx_L = list_left.index(minLeft)
        L_left_min = min(L)
        R_right_min = min(R)
        L_index = L.index(L_left_min)
        R_index = R.index(R_right_min)

        # (1) 1번 삼거리
        if frontLidar <= 3000:
            steer = -70
        
            
        if L.count(325) >= 10: #and V.count(255) >= 3 :
            velocity = 50
            if V.count(255) >= 4 and L.count(325) <= 16: steer =  -100 + standard_steer
            elif Idx_L >= 15: steer = -100 + standard_steer
            elif Idx_L >= 3 and V[20] < 200: steer = -80 +standard_steer

                #elif 구문 2개 없어도 되지 않을까?
        # if V.count(255) >= 3 and L.count(325) >= 17 and R.count(255) <= 5:
        #     steer = -70
        # if V.count(255) <= 3:

        if V[35] < 70:
            steer = -80 + standard_steer

        if V[5] < 70:
            steer = 80 + standard_steer

        if V[20] < 80 and V[10] > V[30]: steer = -90
        if V[20] < 80 and V[30] > V[10]: steer = 90



        # 현재 부족한 점 : steer 값에 따른 바퀴의 회전 각도, 밸런스 조정이 안되어 이탈 가능, 더 많은 경우의 수 수집 요망

        if 0 < frontLidar < 150 :
            velocity = 0


        print ('L[0]=', L[0], 'L[1]=', L[1], 'L[2]=', L[2], end="  //  ")
        print ('R[0]=', R[0], 'R[1]=', R[1], 'R[2]=', R[2])
        print ('V[0]=', V[0], 'V[1]=', V[1], 'V[2]=', V[2], 'V[3]=', V[3], 'V[4]=', V[4], 'V[5]=', V[5], 'V[6]=', V[6])
        print('frontLidar=', frontLidar, end="..//..")
        print('rearLidar=', rearLidar, end="       => => =>    ")
        print('[steer=', steer, end="]  ")
        print('[velocity=', velocity, "]")
        print(L[20], R[20])
        print(L.count(325), R.count(316))
        print(R_index, L_index)

        self.vars.steer = steer
        self.vars.velocity = velocity
        return self.vars.steer, self.vars.velocity


if __name__ == "__main__":
    g = Graphics(Planning)  # 자주차 컨트롤러 실행
    g.root.mainloop()  # 클릭 이벤트 처리
    g.exit()  # 자주차 컨트롤러 종료