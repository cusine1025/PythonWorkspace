import random,time,hashlib,copy
from assets.dataBaseModule import *

from firebase_admin import db
from datetime import datetime

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import *

from main import MainWindow
from main import userId

voteSubject = []
voteOptions = []
voteCount = []
optionPage = 0
voteCode = ''
fireBaseData = {}

voteSelect = []
voteArchiveDB = DataBase('vote', userId = 'text', result = 'text', date = 'text')
ID = 0
USER_ID = 1
RESULT = 2
DATE = 3
MainWindow = ''
userId = ''
def settingVoteModule(id,window=None):
    global MainWindow,userId
    if window is not None : MainWindow = window
    userId = copy.copy(id)

class GetFireBaseInfo(QThread):
    update = pyqtSignal(bool)
    def __init__(self, interest):
        QThread.__init__(self) 
        self.interest = interest
        self.working = True
    
    def run(self):
        global fireBaseData
        ref = db.reference(self.interest)
        while self.working:
            info = ref.get()
            if info != fireBaseData:
                fireBaseData = ref.get()
                self.update.emit(True)
            time.sleep(1)

def clearVoteData(save = False):
    if save : global voteCount
    ref = db.reference('vote')
    items = ref.get()
    if save : voteCount = items[voteCode]
    if len(items.keys()) != 1:
        del items[voteCode]
        ref.set(items)
    else:
        ref = db.reference('vote')
        ref.set({})
    ref = db.reference("voteJoin")
    items = ref.get()
    if len(items.keys()) != 1:
        del items[voteCode]
        ref.set(items)
    else:
        ref = db.reference('voteJoin')
        ref.set({})
    ref = db.reference("voteSubject")
    items = ref.get()
    if len(items.keys()) != 1:
        del items[voteCode]
        ref.set(items)
    else:
        ref = db.reference('voteSubject')
        ref.set({})
    ref = db.reference("voteOptions")
    items = ref.get()
    if len(items.keys()) != 1:
        del items[voteCode]
        ref.set(items)
    else:
        ref = db.reference('voteOptions')
        ref.set({})

class VoteWindow(QMainWindow, QWidget, FORM_VOTE):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()

    def initUI(self):
        self.setupUi(self)
        self.goBackBtn.clicked.connect(self.goBack)
        self.makeBtn.clicked.connect(self.openMakeVote)
        self.joinBtn.clicked.connect(self.openJoinVote)
        self.archiveBtn.clicked.connect(self.openArchive)

    def goBack(self):
        self.main = MainWindow()
        self.main.show()
        self.close()

    def openMakeVote(self):
        self.makeVote = SubjectVoteWindow()
        self.makeVote.show()
        self.close()

    def openJoinVote(self):
        self.joinVote = JoinVoteWindow()
        self.joinVote.show()
        self.close()

    def openArchive(self):
        self.archive = VoteArchiveWindow()
        self.archive.show()
        self.close()

class SubjectVoteWindow(QMainWindow, QWidget, FORM_SUBJECT_VOTE):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()

    def initUI(self):
        self.setupUi(self)
        self.goBackBtn.clicked.connect(self.goBack)
        self.addBtn.clicked.connect(self.addSubject)
        self.editBtn.clicked.connect(self.editSubject)
        self.removeBtn.clicked.connect(self.removeSubject)
        self.nextBtn.clicked.connect(self.next)

        self.subjectInput.returnPressed.connect(self.addSubject)
        self.subjectList.clicked.connect(self.showTools)

        self.editBtn.hide()
        self.removeBtn.hide()
        self.subjectList.addItems(voteSubject)
        if len(voteSubject) == 0:
            self.nextBtn.hide()

    def goBack(self):
        self.vote = VoteWindow()
        self.vote.show()
        self.close()

    def addSubject(self):
        if self.subjectInput.text() != '':
            if self.subjectList.currentRow() != -1:
                self.subjectList.insertItem(self.subjectList.currentRow()+1, self.subjectInput.text())
            else:
                self.subjectList.addItem(self.subjectInput.text())
            self.nextBtn.show()
            self.subjectInput.setText('')

    def editSubject(self):
        if self.subjectInput.text() != '':
            self.subjectList.currentItem().setText(self.subjectInput.text())
            self.subjectInput.setText('')

    def removeSubject(self):
        self.subjectList.takeItem(self.subjectList.currentRow())
        self.hideTools()
        self.subjectList.setCurrentRow(-1)
        if self.subjectList.count() == 0 :
            self.nextBtn.hide()

    def showTools(self):
        self.editBtn.show()
        self.removeBtn.show()

    def hideTools(self):
        self.editBtn.hide()
        self.removeBtn.hide()

    def next(self):
        global voteSubject
        global voteOptions
        voteSubject = [self.subjectList.item(i).text() for i in range(self.subjectList.count())]
        voteOptions = [[] for i in range(self.subjectList.count())]
        self.voteOptionWindow = MakeVoteOptionWindow()
        self.voteOptionWindow.show()
        self.close()

class MakeVoteOptionWindow(QMainWindow, QWidget, FORM_MAKE_VOTE_OPTION):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()

    def initUI(self):
        self.setupUi(self)
        self.goBackBtn.clicked.connect(self.goBack)
        self.addBtn.clicked.connect(self.addOption)
        self.editBtn.clicked.connect(self.editOption)
        self.removeBtn.clicked.connect(self.removeOption)
        self.nextBtn.clicked.connect(self.nextPage)
        self.subjectNameLabel.setText(f'주제 : {voteSubject[optionPage]}')
        self.optionList.setCurrentRow(-1)
        self.hideTools()

        self.optionInput.returnPressed.connect(self.addOption)
        self.optionList.clicked.connect(self.showTools)

        self.optionList.addItems(voteOptions[optionPage])
        if len(voteOptions[optionPage]) == 0:
            self.nextBtn.hide()
        else:
            self.nextBtn.show()

    def addOption(self):
        if self.optionInput.text() != '':
            if self.optionList.currentRow() != -1:
                self.optionList.insertItem(self.optionList.currentRow()+1, self.optionInput.text())
            else:
                self.optionList.addItem(self.optionInput.text())
            self.nextBtn.show()
            self.optionInput.setText('')

    def editOption(self):
        if self.optionInput.text() != '':
            self.optionList.currentItem().setText(self.optionInput.text())
            self.optionInput.setText('')

    def removeOption(self):
        self.optionList.takeItem(self.optionList.currentRow())
        self.hideTools()
        self.optionList.setCurrentRow(-1)
        if self.optionList.count() == 0 :
            self.nextBtn.hide()

    def showTools(self):
        self.editBtn.show()
        self.removeBtn.show()

    def hideTools(self):
        self.editBtn.hide()
        self.removeBtn.hide()

    def nextPage(self):
        global optionPage
        global voteOptions
        global voteCode
        global fireBaseData

        voteOptions[optionPage] = [self.optionList.item(i).text() for i in range(self.optionList.count())]
        if optionPage >= len(voteSubject) - 1:
            code = self.makeCode()
            ref = db.reference("vote")
            ref.update({code:[[0 for j in range(len(voteOptions[i]))] for i in range(len(voteSubject))]})
            fireBaseData = ref.get()
            ref = db.reference("voteJoin")
            ref.update({code:'None'})
            ref = db.reference("voteSubject")
            ref.update({code:voteSubject})
            ref = db.reference("voteOptions")
            ref.update({code:voteOptions})
            voteCode = str(code)

            self.voteWait = VoteWaitWindow()
            self.voteWait.show()
            self.close()
        else:
            optionPage += 1
            self.optionList.clear()
            self.subjectNameLabel.setText(f'주제 : {voteSubject[optionPage]}')
            self.optionList.addItems(voteOptions[optionPage])
            if len(voteOptions[optionPage]) == 0:
                self.nextBtn.hide()
            else:
                self.nextBtn.show()

    def goBack(self):
        global optionPage
        if optionPage == 0:
            self.goBackAlert = GoBackAlertWindow()
            self.goBackAlert.show()
            self.close()
        else:
            optionPage -= 1
            self.optionList.clear()
            self.subjectNameLabel.setText(f'주제 : {voteSubject[optionPage]}')
            self.optionList.addItems(voteOptions[optionPage])
            if len(voteOptions[optionPage]) == 0:
                self.nextBtn.hide()
            else:
                self.nextBtn.show()

    def makeCode(self):
        ref = db.reference('vote')
        code = random.randint(0,999999)
        if ref.get() is not None:
            while code in ref.get().keys():
                code = random.randint(0,999999)
        return code

class GoBackAlertWindow(QMainWindow, QWidget, FORM_GO_BACK_ALERT):
    def __init__(self,option = 0):
        super().__init__()
        self.option = option
        self.initUI()
        self.show()

    def initUI(self):
        self.setupUi(self)
        if self.option == 0:
            self.goBackBtn.clicked.connect(self.goBack)
            self.cancelBtn.clicked.connect(self.cancel)
        elif self.option == 1:
            self.voteLabel.setText('정말로 돌아가시겠습니까?\n(현재 진행중인 투표는 중단됩니다.)')
            self.goBackBtn.setText('돌아가기')
            self.goBackBtn.clicked.connect(self.goPre)
            self.cancelBtn.clicked.connect(self.cancelInVote)
            #self.ui.closeButton.clicked.connect(self.exit)
        elif self.option == 2:
            self.voteLabel.setText('정말로 투표를 종료하시겠습니까?')
            self.goBackBtn.setText('투표 종료')
            self.goBackBtn.clicked.connect(self.goEnd)
            self.cancelBtn.clicked.connect(self.cancelInVote)
            #self.ui.closeButton.clicked.connect(self.exit)
        elif self.option == 3:
            self.voteLabel.setText('아직 투표를 다 하지 않았습니다. 그래도 제출하시겠습니까?\n(한 번 제출한 표는 수정할 수 없습니다.)')
            self.goBackBtn.setText('제출하기')
            self.goBackBtn.clicked.connect(self.submit)
            self.cancelBtn.clicked.connect(self.option3_cancel)
            #self.ui.closeButton.clicked.connect(self.exit)
        elif self.option == 4:
            self.voteLabel.setText('돌아가시면 현재 투표는 저장되지 않습니다.\n 그래도 돌아가시겠습니까?')
            self.goBackBtn.setText('돌아가기')
            self.goBackBtn.clicked.connect(self.option4_goBack)
            self.cancelBtn.clicked.connect(self.option3_cancel)
            #self.ui.closeButton.clicked.connect(self.exit)

    def goBack(self):
        self.subjectVote = SubjectVoteWindow()
        self.subjectVote.show()
        self.close()

    def goEnd(self):
        clearVoteData(True)
        self.endVoteWindow = EndVoteWindow()
        self.endVoteWindow.show()
        self.close()
        
    def option4_goBack(self):
        global voteSelect
        voteSelect = []
        self.endVoteWindow = JoinVoteWindow()
        self.endVoteWindow.show()
        self.close()

    def submit(self):
        if db.reference(f'voteJoin').get() is None:
            self.failVoting = FailJoinVoteWindow(1)
            self.failVoting.show()
            self.close()
        elif db.reference(f'voteJoin').get()[voteCode] is None:
            self.failVoting = FailJoinVoteWindow(1)
            self.failVoting.show()
            self.close()
        else:
            global voteSelect
            m = hashlib.sha256()
            m.update(userId.encode('utf-8'))
            hashedId = m.hexdigest()
            ref = db.reference(f'voteJoin/{voteCode}')
            data = ref.get()
            if data == "None":
                ref.set([hashedId])
            else:
                ref.update(data + [hashedId])
            ref = db.reference(f'vote/{voteCode}')
            data = ref.get()
            for i in range(len(voteSelect)):
                if voteSelect[i] != -1 : data[i][voteSelect[i]] += 1
            ref.update(data)
            voteSelect = []
            self.success = FailJoinVoteWindow(2)
            self.success.show()
            self.close()

    def option3_cancel(self):
        self.joinAndVotingWindow = JoinAndVotingWindow()
        self.joinAndVotingWindow.show()
        self.close()

    def cancel(self):
        self.vote = MakeVoteOptionWindow()
        self.vote.show()
        self.close()

    def cancelInVote(self):
        self.thisWindow = VoteWaitWindow()
        self.thisWindow.show()
        self.close()

    def goPre(self):
        clearVoteData()
        self.MakeVoteOptionWindow = MakeVoteOptionWindow()
        self.MakeVoteOptionWindow.show()
        self.close()

    def exit(self):
        clearVoteData()
        self.close()


class VoteWaitWindow(QMainWindow, QWidget, FORM_WAIT_VOTE):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()

    def initUI(self):
        self.setupUi(self)
        self.goBackBtn.clicked.connect(self.goBack)
        #self.ui.closeButton.clicked.connect(self.exit)
        self.subjectComboBox.addItems(voteSubject)
        self.endVoteBtn.clicked.connect(self.endVote)
        self.joinCodeLabel.setText(f'참여 코드 : {voteCode}')
        self.subjectComboBox.currentIndexChanged.connect(self.updateOptionList)

        self.th = GetFireBaseInfo('vote')
        self.th.update.connect(self.updateData)
        self.th.start()
        idx = self.subjectComboBox.currentIndex()
        formattedOptions = [f'{voteOptions[idx][i]} : {fireBaseData[voteCode][idx][i]}표' for i in range(len(voteOptions[idx]))]
        self.optionList.addItems(formattedOptions)

    def goBack(self):
        self.th.working = False
        self.goBackAlert = GoBackAlertWindow(1)
        self.goBackAlert.show()
        self.close()

    def endVote(self):
        self.th.working = False
        self.goBackAlert = GoBackAlertWindow(2)
        self.goBackAlert.show()
        self.close()

    def updateOptionList(self):
        self.optionList.clear()
        idx = self.subjectComboBox.currentIndex()
        formattedOptions = [f'{voteOptions[idx][i]} : {fireBaseData[voteCode][idx][i]}표' for i in range(len(voteOptions[idx]))]
        self.optionList.addItems(formattedOptions)

    def exit(self):
        clearVoteData()
        self.close()

    @pyqtSlot(bool)
    def updateData(self):
        idx = self.subjectComboBox.currentIndex()
        options = voteOptions[idx]
        for i in range(len(options)):
            self.optionList.item(i).setText(f'{options[i]} : {fireBaseData[voteCode][idx][i]}표')

class EndVoteWindow(QMainWindow, QWidget, FORM_END_VOTE):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()
    
    def initUI(self):
        self.setupUi(self)
        self.endVoteBtn.clicked.connect(self.ok)
        result = [[(voteOptions[subject][i],voteCount[subject][i]) for i in range(len(voteCount[subject]))] for subject in range(len(voteSubject))]
        rank = [sorted(result[i], key=lambda x: x[1],reverse=True) for i in range(len(voteSubject))]
        rank = [voteSubject[item]+" : "+', '.join([f'{rank[item][i][0]}({rank[item][i][1]}표)' for i in range(len(rank[item]))]) for item in range(len(rank))]
        now = datetime.now()
        now = str(now.strftime("%Y.%m.%d/%H:%M"))
        voteArchiveDB.add((userId,str(rank),now))
        self.resultList.addItems(rank)

    def ok(self):
        global voteSubject
        voteSubject = []
        self.vote = VoteWindow()
        self.vote.show()
        self.close()

class VoteArchiveWindow(QMainWindow, QWidget, FORM_VOTE_ARCHIVE):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()

    def initUI(self):
        self.setupUi(self)
        self.goBackBtn.clicked.connect(self.goBack)
        self.viewBtn.clicked.connect(self.view)
        self.removeBtn.clicked.connect(self.removeArchive)
        self.removeBtn.hide()
        self.viewBtn.hide()
        self.archiveList.clicked.connect(self.showTools)
        self.archive = voteArchiveDB.select(f'userId = "{userId}"')[::-1]
        self.archiveList.addItems(['/'.join(eval(self.archive[i][RESULT]))[:20]+("..." if len('/'.join(eval(self.archive[i][RESULT]))) > 20 else "")+" ("+self.archive[i][DATE]+")" for i in range(len(self.archive))])

    def view(self):
        self.vote = ViewVoteArchiveWindow(self.archiveList.currentRow())
        self.vote.show()
        self.close()

    def removeArchive(self):
        deletedItemId = self.archive[self.archiveList.currentRow()][ID]
        voteArchiveDB.excute(f'''
            DELETE FROM 'vote' WHERE id = {deletedItemId}
        ''')
        self.archiveList.takeItem(self.archiveList.currentRow())
        self.archive = voteArchiveDB.select(f'userId = "{userId}"')
        self.archiveList.setCurrentRow(-1)
        self.removeBtn.hide()
        self.viewBtn.hide()

    def goBack(self):
        self.vote = VoteWindow()
        self.vote.show()
        self.close()

    def showTools(self):
        self.removeBtn.show()
        self.viewBtn.show()

class ViewVoteArchiveWindow(QMainWindow, QWidget, FORM_VIEW_VOTE_ARCHIVE):
    def __init__(self,idx):
        super().__init__()
        self.idx = idx
        self.initUI()
        self.show()

    def initUI(self):
        self.setupUi(self)
        self.goBackBtn.clicked.connect(self.goBack)
        archive = voteArchiveDB.select(f'userId = "{userId}"')
        self.archiveList.addItems(eval(archive[self.idx][RESULT]))

    def goBack(self):
        self.vote = VoteArchiveWindow()
        self.vote.show()
        self.close()

class JoinVoteWindow(QMainWindow, QWidget, FORM_JOIN_VOTE):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()

    def initUI(self):
        self.setupUi(self)
        self.goBackBtn.clicked.connect(self.goBack)
        self.numberInput.returnPressed.connect(self.join)
        self.joinBtn.clicked.connect(self.join)

    def join(self):
        ref = db.reference('vote')
        data = ref.get()
        m = hashlib.sha256()
        m.update(userId.encode('utf-8'))
        hashedId = m.hexdigest()
        if data is not None:
            if self.numberInput.text() in data.keys() and not hashedId in db.reference('voteJoin').get()[self.numberInput.text()]:
                global voteCode
                voteCode = self.numberInput.text()
                self.joinAndVoting = JoinAndVotingWindow()
                self.joinAndVoting.show()
                self.close()
            else:
                self.failJoinVote = FailJoinVoteWindow()
                self.failJoinVote.show()
                self.close()
        else:
            self.failJoinVote = FailJoinVoteWindow()
            self.failJoinVote.show()
            self.close()

    def goBack(self):
        self.vote = VoteWindow()
        self.vote.show()
        self.close()

class FailJoinVoteWindow(QMainWindow, QWidget, FORM_FAIL_JOIN_VOTING):
    def __init__(self,option = 0):
        super().__init__()
        self.option = option
        self.initUI()
        self.show()

    def initUI(self):
        self.setupUi(self)
        self.goBackBtn.clicked.connect(self.goBack)
        if self.option == 1:
            self.reasonLabel.setText('제출 실패\n투표하는동안 방이 사라졌습니다!')
            self.goBackBtn.setText('확인')
        elif self.option == 2:
            self.reasonLabel.setText('성공적으로 제출되었습니다!')
            self.goBackBtn.setText('확인')
            self.goBackBtn.setStyleSheet('''
                background-color : #516BEB;
                border-radius : 5px;
            ''')

    def goBack(self):
        self.vote = JoinVoteWindow()
        self.vote.show()
        self.close()

class RadioButton:
    def __init__(self,subject,idx,item,screen):
        self.subject = subject
        self.idx = idx
        self.radio = QRadioButton(item,screen)
        self.radio.clicked.connect(lambda : self.changeValue(self.subject,self.idx))
        if idx == voteSelect[subject]:
            self.radio.setChecked(True)
        
    def changeValue(self,subject,idx):
        global voteSelect
        voteSelect[subject] = idx

class JoinAndVotingWindow(QMainWindow, QWidget, FORM_JOIN_AND_VOTING):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()

    def initUI(self):
        global voteSelect
        ref = db.reference('voteSubject')
        subject = ref.get()[voteCode]
        if voteSelect == []:
            voteSelect = [-1 for i in range(len(subject))]

        ref = db.reference('voteOptions')
        self.option = ref.get()[voteCode]

        self.setupUi(self)
        self.goBackBtn.clicked.connect(self.goBack)
        self.subjectComboBox.addItems(subject)
        self.submitBtn.clicked.connect(self.submit)
        idx = self.subjectComboBox.currentIndex()
        for i in range(len(self.option[idx])):
            item = self.option[idx][i]
            wItem = QListWidgetItem()
            self.optionList.addItem(wItem)
            self.optionList.setItemWidget(wItem,RadioButton(idx,i,item,self).radio)
        self.subjectComboBox.currentIndexChanged.connect(self.updateOptionList)

    def goBack(self):
        self.vote = GoBackAlertWindow(4)
        self.vote.show()
        self.close()

    def submit(self):
        global voteSelect
        if -1 in voteSelect:
            self.goBackAlert = GoBackAlertWindow(3)
            self.goBackAlert.show()
            self.close()
        elif db.reference(f'voteJoin/{voteCode}').get() is None:
            self.failVoting = FailJoinVoteWindow(1)
            self.failVoting.show()
            self.close()
        else:
            m = hashlib.sha256()
            m.update(userId.encode('utf-8'))
            hashedId = m.hexdigest()
            ref = db.reference(f'voteJoin/{voteCode}')
            data = ref.get()
            if data == "None":
                ref.set([hashedId])
            else:
                data.append(hashedId)
                ref.set([data])
            ref = db.reference(f'vote')
            data = ref.get()[voteCode]
            for i in range(len(voteSelect)):
                data[i][voteSelect[i]] += 1
            ref.update({voteCode:data})
            self.success = FailJoinVoteWindow(2)
            voteSelect = []
            self.success.show()
            self.close()

    def updateOptionList(self):
        self.optionList.clear()
        idx = self.subjectComboBox.currentIndex()
        for i in range(len(self.option[idx])):
            item = self.option[idx][i]
            wItem = QListWidgetItem()
            self.optionList.addItem(wItem)
            self.optionList.setItemWidget(wItem,RadioButton(idx,i,item,self).radio)
        self.subjectComboBox.currentIndexChanged.connect(self.updateOptionList)