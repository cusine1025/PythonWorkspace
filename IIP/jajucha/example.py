from turtle import speed
from jajucha.planning import BasePlanning
from jajucha.graphics import Graphics


class Planning(BasePlanning):
    def __init__(self, graphics):
        super().__init__(graphics)
        # --------------------------- #
        self.vars.steer = 0  # 변수 설정

    def process(self, t, frontImage, rearImage, frontLidar, rearLidar):
        """
        자주차의 센서 정보를 바탕으로 조향과 속도를 결정하는 함수
        t: 주행 시점으로부터의 시간 (초)
        frontImage: 전면 카메라 이미지
        rearImage: 후면 카메라 이미지
        frontLidar: 전면 거리 센서 (mm), 0은 오류를 의미함
        rearLidar: 후면 거리 센서 (mm), 0은 오류를 의미함
        """
        frontPoints = self.gridFront(frontImage)
        frontLights = self.lightsFront(frontImage)
        rearPoints = self.gridRear(rearImage)

        V, L, R = frontPoints
        reds, greens = frontLights

        steer = 0
        velocity = 40

        print("steer=" , steer)
        print("velocity=", velocity)
        print ('L[0]=', L[0], 'L[1]=', L[1], 'L[2]=', L[2], end="  //  ")
        print ('R[0]=', R[0], 'R[1]=', R[1], 'R[2]=', R[2])
        print ('V[0]=', V[0], 'V[1]=', V[1], 'V[2]=', V[2], 'V[3]=', V[3], 'V[4]=', V[4], 'V[5]=', V[5], 'V[6]=', V[6])

        #우회전할 때  steer = 60






        return steer, velocity


if __name__ == "__main__":
    g = Graphics(Planning)  # 자주차 컨트롤러 실행
    g.root.mainloop()  # 클릭 이벤트 처리
    g.exit()  # 자주차 컨트롤러 종료