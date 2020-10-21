import sys
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
import algorithm
import random

class MainWindow(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.title = '重排九宫'
        self.width = 1600
        self.height = 900
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.resize(self.width, self.height)
        self.squares()

        self.label1 = QtWidgets.QLabel(self)
        self.label1.setText('设置初始状态：')
        self.label1.move(1000, 100)
        self.label1.setFont(QtGui.QFont('Microsoft YaHei', 20, 75))

        self.randButton = QtWidgets.QPushButton('随机初始状态', self)
        self.randButton.setFont(QtGui.QFont('Microsoft YaHei',10)) 
        self.randButton.move(1000, 150)
        self.randButton.resize(150, 50)
        self.randButton.clicked.connect(self.rand)
        
        self.inputButton = QtWidgets.QPushButton('输入初始状态',self)
        self.inputButton.setFont(QtGui.QFont('Microsoft YaHei',10)) 
        self.inputButton.move(1200, 150)
        self.inputButton.resize(150, 50)
        self.inputButton.clicked.connect(self.input)

        self.label2 = QtWidgets.QLabel(self)
        self.label2.setText('搜索：')
        self.label2.move(1000, 250)
        self.label2.setFont(QtGui.QFont('Microsoft YaHei', 20, 75))

        self.searchButton = QtWidgets.QPushButton('开始搜索',self)
        self.searchButton.setFont(QtGui.QFont('Microsoft YaHei',10)) 
        self.searchButton.move(1000, 300)
        self.searchButton.resize(150, 50)
        self.searchButton.clicked.connect(self.begin_search)

        self.label3 = QtWidgets.QLabel(self)
        self.label3.setText('模式1：自动演示')
        self.label3.move(1000, 400)
        self.label3.setFont(QtGui.QFont('Microsoft YaHei', 20, 75))

        self.startButton = QtWidgets.QPushButton('开始',self)
        self.startButton.setFont(QtGui.QFont('Microsoft YaHei',10)) 
        self.startButton.move(1000, 450)
        self.startButton.resize(150, 50)
        self.startButton.clicked.connect(self.start)

        self.pauseButton = QtWidgets.QPushButton('暂停',self)
        self.pauseButton.setFont(QtGui.QFont('Microsoft YaHei',10)) 
        self.pauseButton.move(1200, 450)
        self.pauseButton.resize(150, 50)
        self.pauseButton.clicked.connect(self.pause)

        self.pBar = QtWidgets.QProgressBar(self)
        self.pBar.setGeometry(1000, 700, 350, 25)
        self.pBar.setValue(0)

        self.label4 = QtWidgets.QLabel(self)
        self.label4.setText('模式2：手动演示')
        self.label4.move(1000, 550)
        self.label4.setFont(QtGui.QFont('Microsoft YaHei', 20, 75))

        self.nextButton = QtWidgets.QPushButton('下一步',self)
        self.nextButton.setFont(QtGui.QFont('Microsoft YaHei',10)) 
        self.nextButton.move(1000, 600)
        self.nextButton.resize(150, 50)
        self.nextButton.clicked.connect(self.next)

        self.lastButton = QtWidgets.QPushButton('上一步',self)
        self.lastButton.setFont(QtGui.QFont('Microsoft YaHei',10)) 
        self.lastButton.move(1200, 600)
        self.lastButton.resize(150, 50)
        self.lastButton.clicked.connect(self.last)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.new_state)

        self.show()
    

    def squares(self):
        a = 256
        interval = 20
        self.w = []
        self.image = []
        self.labels = []
        self.array = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        for i in range(3):
            self.w.append([])
            self.labels.append([])
            for j in range(3):
                self.w[i].append(QtWidgets.QWidget(self)) 
                self.w[i][j].setGeometry(50 + j * (interval + a), 50 + i * (interval + a), a, a)
                self.w[i][j].setStyleSheet('background-color:white')
                self.labels[i].append(QtWidgets.QLabel(self.w[i][j])) 
                self.image.append(QtGui.QPixmap('figures/' + str(3 * i + j) + '.png'))
        self.show_state()
    
    def rand(self):
        self.init = []
        self.init = random.sample(range(0, 9), 9)
        self.array = self.init
        self.show_state()
    
    def show_state(self):
        for i in range(3):
            for j in range(3):
                self.labels[i][j].setPixmap(self.image[self.array[3 * i + j]])
    
    def input(self):
        self.init = []
        inputArray, okPressed = QtWidgets.QInputDialog.getText(self, '输入初始状态',
        '从左到右，从上到下，依次输入九个数字（空格用数字0代替），用英文逗号隔开。', QtWidgets.QLineEdit.Normal)
        inputArray = inputArray.split(",")
        for i in range(9):
            self.init.append(int(inputArray[i])) 
        self.array = self.init
        self.show_state()

    def begin_search(self):
        self.alg = algorithm.Algorithm()
        self.alg.get_start(self.array)
        self.alg.have_solution()
        if not self.alg.haveSolution:
            failMessage = QtWidgets.QMessageBox.critical(self, '错误', '该初始状态无解！', QtWidgets.QMessageBox.Ok)
        else:
            self.alg.search()
            self.steps = self.alg.bestNode.depth
            successMessage = QtWidgets.QMessageBox.information(self, 
            '提示', '找到一个解，共用' + str(self.steps) + '步！', QtWidgets.QMessageBox.Ok)
            self.currentStep = -1

    def new_state(self):
        if self.currentStep == len(self.alg.solution) - 1:
            self.end()
        else:
            self.currentStep += 1
            self.array = self.alg.solution[self.currentStep]
            self.show_state()
            self.pBar.setValue(100 * (self.currentStep + 1) / self.steps)
            
    
    def start(self):
        self.timer.start(1000)
        self.startButton.setEnabled(False)
        self.pauseButton.setEnabled(True)

    def pause(self):
        self.timer.stop()
        self.startButton.setEnabled(True)
        self.pauseButton.setEnabled(False)

    def end(self):
        self.timer.stop()
        self.startButton.setEnabled(True)
        self.pauseButton.setEnabled(True)
        finishMessage = QtWidgets.QMessageBox.information(self, '提示', '已到达目标状态！', QtWidgets.QMessageBox.Ok)

    def next(self):
        if self.currentStep == len(self.alg.solution) - 1:
            self.end()
        else:
            self.currentStep += 1
            self.array = self.alg.solution[self.currentStep]
            self.show_state()
            self.pBar.setValue(100 * (self.currentStep + 1) / self.steps)
            
    def last(self):
        if self.currentStep == -1:
            failMessage = QtWidgets.QMessageBox.warning(self, '警告', '这是初始状态！', QtWidgets.QMessageBox.Ok)
        elif self.currentStep == 0:
            self.currentStep -= 1
            self.array = self.init
            self.show_state()
            self.pBar.setValue(100 * (self.currentStep + 1) / self.steps)
        else:
            self.currentStep -= 1
            self.array = self.alg.solution[self.currentStep]
            self.show_state()
            self.pBar.setValue(100 * (self.currentStep + 1) / self.steps)



        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())