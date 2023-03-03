import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget, QPushButton
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt
from PyQt5 import QtGui, QtWidgets

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("자리배치")
        self.setGeometry(0, 0, 3840, 2160) # 모니터 크기에 맞는 창 크기로 설정
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        self.gridLayout = QGridLayout(centralWidget)
        try:
            with open("list.txt", "r", encoding='utf-8') as file:
                contents = file.read()
            self.names = contents.split(sep = ',')
            print(True)
        except:
            pass
        random.shuffle(self.names)
        self.label_list = []
        for i in range(5):
            for j in range(6):
                index = i*6 + j
                if index < len(self.names):
                    label = QLabel(self.names[index], self)
                    label.setFont(QtGui.QFont("궁서",20)) #폰트,크기 조절
                    label.setAlignment(Qt.AlignCenter)
                    self.gridLayout.addWidget(label, i, j)
                    label.setHidden(True)
                    self.label_list.append(label)

        self.button = QtWidgets.QPushButton("자리 뽑기", self)

        self.button.resize(200,100)
        self.button.setGeometry(0, 0, 100, 30)
        self.button.clicked.connect(self.on_button_clicked)

        self.countdown_label = QLabel("", self)
        self.countdown_label.setGeometry(100, 0, 100, 30)
        self.countdown_label.setAlignment(Qt.AlignCenter)

    def on_button_clicked(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_label)
        self.counter = 5
        self.timer.start(1000) # 1초마다 호출

    def update_label(self):
        self.counter -= 1
        if self.counter == 0:
            self.timer.stop()
            self.show_result()
        else:
            self.countdown_label.setText("")

    def show_result(self):
        for i,label in enumerate(self.label_list):
            label.setHidden(False)
            
        self.countdown_label.setText("")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

