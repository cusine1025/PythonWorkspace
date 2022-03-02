import random,copy
from assets.dataBaseModule import *
from assets.parameter import *

from datetime import datetime
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import *

shuffle_col = 1
shuffle_row = 1
shuffle_number = [1]
shuffle_location = []

shuffleArchiveDB = DataBase('shuffle', userId = 'text', rowAndCol = 'text', shuffled = 'text', location = 'text', date = 'text')
ID = 0
USER_ID = 1
ROW_AND_COL = 2
SHUFFLED = 3
LOCATION = 4
DATE = 5

MainWindow = ''
userId = ''
def settingShuffleModule(id,window=None):
    global MainWindow,userId
    if window is not None : MainWindow = window
    userId = copy.copy(id)

class ShufflePrepareWindow(QMainWindow, QWidget, FORM_SHUFFLE_PREPARE):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()

    def initUI(self):
        self.setupUi(self)
        self.goBackBtn.clicked.connect(self.goBack)
        self.makeBtn.clicked.connect(self.setting)
        self.archiveBtn.clicked.connect(self.archive)
        
    def setting(self):
        self.settingWindow = ShuffleSettingWindow()
        self.settingWindow.show()
        self.close()
        
    def goBack(self):
        self.back = MainWindow()
        self.back.show()
        self.close()
        
    def archive(self):
        self.archiveWindow = ShuffleArchiveWindow()
        self.archiveWindow.show()
        self.close()
    
class ShuffleSettingWindow(QMainWindow, QWidget, FORM_SHUFFLE_SETTING):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()
        
    def initUI(self):
        self.setupUi(self)
        self.goBackBtn.clicked.connect(self.goBack)
        self.okBtn.clicked.connect(self.ok)
        self.rowSpinBox.setValue(shuffle_row)
        self.colSpinBox.setValue(shuffle_col)
        self.numberSpinBox.setValue(max(shuffle_number))
    
    def goBack(self):
        self.back = ShufflePrepareWindow()
        self.back.show()
        self.close()
    
    def ok(self):
        global shuffle_row, shuffle_col, shuffle_number, shuffle_location
        shuffle_row,shuffle_col,shuffle_number = self.rowSpinBox.value(), self.colSpinBox.value(), list(range(1,1+self.numberSpinBox.value()))
        shuffle_location = [[True for x in range(shuffle_row)] for y in range(shuffle_col)]
        self.next = ShuffleMainWindow()
        self.next.show()
        self.close()
    
class SeatButton:
    def __init__(self,location,color = 'rgb(39, 197, 255)',option = 0) -> None:
        self.x, self.y = location[0],location[1]
        self.button = QPushButton('')
        self.changeColor(color)
        self.button.setMinimumHeight(10)
        self.button.setMinimumWidth(10)
        self.button.setMaximumHeight(100)
        self.button.setMaximumWidth(100)
        if option == 0: self.button.clicked.connect(lambda : self.clicked(self.x,self.y))
        if option == 1:
            if shuffle_location[self.y][self.x]:
                self.changeColor('rgb(255, 255, 255)')
            else:
                self.changeColor('rgb(255, 54, 14)')
        if option == 2:
            if (self.x,self.y) in shuffle_location:
                self.changeColor('rgb(255, 255, 255)')
            else:
                self.changeColor('rgb(255, 54, 14)')
    
    def clicked(self,x,y):
        global shuffle_location
        shuffle_location[y][x] = not shuffle_location[y][x]
        if shuffle_location[y][x]:
            self.changeColor('rgb(39, 197, 255)')
        else:
            self.changeColor('rgb(255, 54, 14)')
    
    def changeColor(self,color):
        self.button.setStyleSheet(f'''
            font-family: 'Noto Sans CJK KR Black';
            font-size : 12px;
            color : black;
            background-color : {color};
            border-radius : 5px;
        ''')

class ShuffleMainWindow(QMainWindow, QWidget, FORM_SHUFFLE_MAIN):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()
    
    def initUI(self):
        self.setupUi(self)
        self.goBackBtn.clicked.connect(self.goBack)
        for y in range(shuffle_col):
            for x in range(shuffle_row):
                self.viewer.addWidget(SeatButton((x,y)).button,y,x)
        self.getResultBtn.clicked.connect(self.getResult)
        self.exceptInput.returnPressed.connect(self.getResult)
        reg_ex = QRegExp("([0-9]*(,){,1})*")
        input_validator = QRegExpValidator(reg_ex, self.exceptInput)
        self.exceptInput.setValidator(input_validator)
    
    def goBack(self):
        self.back = ShuffleSettingWindow()
        self.back.show()
        self.close()
    
    def getResult(self):
        exceptNums = map(lambda x : None if x == '' else int(x),self.exceptInput.text().split(','))
        shuffled = shuffle_number
        popped = 0
        for num in exceptNums:
            if num in shuffle_number:
                del shuffled[num-popped-1]
                popped += 1
        random.shuffle(shuffled)
        sumOfAvail = 0
        for y in range(shuffle_col):
            for x in range(shuffle_row):
                sumOfAvail += int(shuffle_location[y][x])
        fitNum = min(len(shuffled),sumOfAvail)
        shuffled = shuffled[:fitNum]
        location = []
        for i in range(fitNum):
            x = random.randint(0,shuffle_row-1)
            y = random.randint(0,shuffle_col-1)
            while (x,y) in location or not shuffle_location[y][x]:
                x = random.randint(0,shuffle_row-1)
                y = random.randint(0,shuffle_col-1)
            location.append((x,y))
        self.result = ShuffleResultWindow(shuffled,location)
        self.result.show()
        self.close()

class ShuffleResultWindow(QMainWindow, QWidget, FORM_SHUFFLE_RESULT):
    def __init__(self,shuffled,location):
        super().__init__()
        self.location = location
        self.shuffled = shuffled
        self.initUI()
        self.show()
    
    def initUI(self):
        global shuffle_number,shuffle_location,shuffle_row,shuffle_col
        self.setupUi(self)
        self.okBtn.clicked.connect(self.end)
        now = datetime.now()
        now = str(now.strftime("%Y.%m.%d/%H:%M:%S"))
        shuffleArchiveDB.add((userId,f'{str(shuffle_row)}x{str(shuffle_col)}',str(self.shuffled),str(self.location),now))
        for y in range(shuffle_col):
            for x in range(shuffle_row):
                self.viewer.addWidget(SeatButton((x,y),option=1).button,y,x)
        for location in self.location:
            self.viewer.itemAtPosition(location[1],location[0]).widget().setText(str(self.shuffled.pop()))
        shuffle_col = 1
        shuffle_row = 1
        shuffle_number = [1]
        shuffle_location = []
    
    def end(self):
        self.shufflePrepare = ShufflePrepareWindow()
        self.shufflePrepare.show()
        self.close()
    
class ShuffleArchiveWindow(QMainWindow, QWidget, FORM_VOTE_ARCHIVE):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()
    
    def initUI(self):
        self.setupUi(self)
        self.archive = shuffleArchiveDB.select(f'userId = "{userId}"')[::-1]
        self.archiveList.addItems([item[DATE] for item in self.archive])
        self.removeBtn.hide()
        self.viewBtn.hide()
        self.archiveList.clicked.connect(self.showTools)
        self.viewBtn.clicked.connect(self.view)
        self.removeBtn.clicked.connect(self.removeArchive)
        self.goBackBtn.clicked.connect(self.goBack)

    def removeArchive(self):
        deletedItemId = self.archive[self.archiveList.currentRow()][ID]
        shuffleArchiveDB.excute(f'''
            DELETE FROM 'shuffle' WHERE id = {deletedItemId}
        ''')
        self.archiveList.takeItem(self.archiveList.currentRow())
        self.archive = shuffleArchiveDB.select(f'userId = "{userId}"')
        self.archiveList.setCurrentRow(-1)
        self.removeBtn.hide()
        self.viewBtn.hide()

    def view(self):
        self.vote = ViewShuffleArchiveWindow(self.archive[self.archiveList.currentRow()])
        self.vote.show()
        self.close()
    
    def goBack(self):
        self.pre = ShufflePrepareWindow()
        self.pre.show()
        self.close()

    def showTools(self):
        self.removeBtn.show()
        self.viewBtn.show()

class ViewShuffleArchiveWindow(QMainWindow, QWidget, FORM_SHUFFLE_RESULT):
    def __init__(self,archive):
        super().__init__()
        self.archive = archive
        self.initUI()
        self.show()
    
    def initUI(self):
        global shuffle_location
        self.setupUi(self)
        self.okBtn.clicked.connect(self.goBack)
        row,col = map(int,self.archive[ROW_AND_COL].split('x'))
        self.location = eval(self.archive[LOCATION])
        self.shuffled = eval(self.archive[SHUFFLED])
        shuffle_location = self.location
        for y in range(col):
            for x in range(row):
                self.viewer.addWidget(SeatButton((x,y),option=2).button,y,x)
        for location in self.location:
            x = location[0]
            y = location[1]
            self.viewer.itemAtPosition(y,x).widget().setText(str(self.shuffled.pop()))

    def goBack(self):
        self.pre = ShuffleArchiveWindow()
        self.pre.show()
        self.close()