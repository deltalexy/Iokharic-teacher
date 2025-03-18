from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QIcon
import os
from functions import *

class IokharicApp(QWidget):
    def __init__(self):
        super().__init__()
        if not os.path.exists(os.path.join(os.getenv('APPDATA'), 'Iokharic-teacher')):
            os.makedirs(os.path.join(os.getenv('APPDATA'), 'Iokharic-teacher'))
            iokharic_downloader()
        self.wordlist = generate_wordlist()
        self.type = 'cp'
        self.initUI()
        self.func()

    def initUI(self):
        # Main layout
        optionbox = QGroupBox()
        layout = QGridLayout()
        cpb = QPushButton('Characters Passive')
        cmb = QPushButton('Characters Multiple Choice')
        cab = QPushButton('Characters Active')
        wpb = QPushButton('Words Passive')
        wab = QPushButton('Words Active')
        npb = QPushButton('Numbers Passive')
        nab = QPushButton('Numbers Active')
        cpb.clicked.connect(self.assignfunc('cp'))
        cmb.clicked.connect(self.assignfunc('cm'))
        cab.clicked.connect(self.assignfunc('ca'))
        wpb.clicked.connect(self.assignfunc('wp'))
        wab.clicked.connect(self.assignfunc('wa'))
        npb.clicked.connect(self.assignfunc('np'))
        nab.clicked.connect(self.assignfunc('na'))
        layout.addWidget(cpb,0,0)
        layout.addWidget(cmb,1,0)
        layout.addWidget(cab,2,0)
        layout.addWidget(wpb,3,0)
        layout.addWidget(wab,4,0)
        layout.addWidget(npb,5,0)
        layout.addWidget(nab,6,0)
        optionbox.setLayout(layout)

        self.functionbox = QGroupBox()
        self.funclayout = QGridLayout()
        self.titlefield = QLabel()
        self.asklabel = QLabel('Translate:')
        self.askfield = QLabel()
        self.answerlabel = QLabel('Answer:')
        self.answerfield = QLineEdit()
        self.checkbutton = QPushButton('Check answer')
        self.checkbutton.clicked.connect(self.answer_check)
        self.nextbutton = QPushButton('Next')
        self.nextbutton.clicked.connect(self.func)
        self.judge = QLabel()
        self.buttonlist = [QPushButton() for _ in range(4)]
        for i in range(len(self.buttonlist)):
            self.buttonlist[i].clicked.connect(self.answerbuttenpush(i))
            self.buttonlist[i].setIcon(QIcon(symbollink('A')))
            for _ in range(4):
                self.buttonlist[i].setIconSize(self.buttonlist[i].sizeHint())
        self.funclayout.addWidget(self.titlefield, 0,0,1,4)
        self.funclayout.addWidget(self.asklabel, 1,0,1,1)
        self.funclayout.addWidget(self.askfield, 1,1,1,3)
        self.funclayout.addWidget(self.answerlabel, 2,0,1,1)
        self.funclayout.addWidget(self.answerfield, 2,1,1,3)
        self.funclayout.addWidget(self.checkbutton, 3,0,1,2)
        self.funclayout.addWidget(self.nextbutton, 3,2,1,2)
        self.funclayout.addWidget(self.judge, 4,0,1,4)
        for i in range(len(self.buttonlist)):
            self.funclayout.addWidget(self.buttonlist[i], 2,i,1,1)
            self.buttonlist[i].hide()
        self.functionbox.setLayout(self.funclayout)

        layout = QGridLayout()
        layout.addWidget(optionbox,0,0,5,1)
        layout.addWidget(self.functionbox,0,1,5,5)

        self.setLayout(layout)
        self.setWindowTitle('Iokharic Learning Tool')
        self.show()

    def assignfunc(self, type):
        def interfunc():
            self.type = type
            for i in range(len(self.buttonlist)):
                self.buttonlist[i].hide()
            self.answerlabel.show()
            self.answerfield.show()
            if type == 'cm':
                self.answerlabel.hide()
                self.answerfield.hide()
                for i in range(len(self.buttonlist)):
                    self.buttonlist[i].show()
            elif (type == 'wa') or (type == 'ca') or (type == 'na'):
                self.answerlabel.hide()
                self.answerfield.hide()
            self.func()
        return interfunc

    def answer_check(self):
        if (self.type == 'wa') or (self.type == 'ca') or (self.type == 'na'):
            if self.type == 'ca':
                pixmap = QPixmap(symbollink(self.askfield.text()))
            else:
                pixmap = QPixmap(os.path.join(os.getenv('APPDATA'), 'Iokharic-teacher', 'temp.png'))
            self.judge.setPixmap(pixmap)
            self.judge.resize(pixmap.width(), pixmap.height())
        else:
            self.answer_given = self.answerfield.text()
            if self.answer_given == self.answer:
                self.judge.setText('Correct')
            else:
                self.judge.setText('Incorrect: {}'.format(self.answer))
    
    def answerbuttenpush(self, index):
        def interfunc():
            if self.sample[index] == self.answer:
                self.judge.setText('Correct')
            else:
                self.judge.setText('Incorrect')
        return interfunc

    def func(self):
        self.answerfield.clear()
        self.judge.clear()
        if self.type == 'cp':
            self.cpfunc()
        elif self.type == 'cm':
            self.cmfunc()
        elif self.type == 'ca':
            self.cafunc()
        elif self.type == 'wp':
            self.wpfunc()
        elif self.type == 'wa':
            self.wafunc()
        elif self.type == 'np':
            self.npfunc()
        else:
            self.nafunc()
            

    def cpfunc(self):
        self.titlefield.setText('Characters Passive')
        char = randomcharacter()
        pixmap = QPixmap(symbollink(char))
        self.askfield.setPixmap(pixmap)
        self.askfield.resize(pixmap.width(), pixmap.height())
        self.answer = char.lower()

    def cmfunc(self):
        self.titlefield.setText('Characters Multiple Choice')
        self.answer, self.sample = get_sample_characters()
        self.askfield.setText(self.answer)
        for i in range(len(self.buttonlist)):
                self.buttonlist[i].setIcon(QIcon(symbollink(self.sample[i])))

    def cafunc(self):
        self.titlefield.setText('Characters Active')
        char = randomcharacter()
        self.askfield.setText(char)

    def wpfunc(self):
        self.titlefield.setText('Words Passive')
        word = get_word(self.wordlist)
        iokharic_word(word)
        pixmap = QPixmap(os.path.join(os.getenv('APPDATA'), 'Iokharic-teacher', 'temp.png'))
        self.askfield.setPixmap(pixmap)
        self.askfield.resize(pixmap.width(), pixmap.height())
        self.answer = word

    def wafunc(self):
        self.titlefield.setText('Words Active')
        word = get_word(self.wordlist)
        iokharic_word(word)
        self.askfield.setText(word)

    def npfunc(self):
        self.titlefield.setText('Numbers Passive')
        number = get_number()
        iokharic_word(number)
        pixmap = QPixmap(os.path.join(os.getenv('APPDATA'), 'Iokharic-teacher', 'temp.png'))
        self.askfield.setPixmap(pixmap)
        self.askfield.resize(pixmap.width(), pixmap.height())
        self.answer = number

    def nafunc(self):
        self.titlefield.setText('Numbers Active')
        number = get_number()
        iokharic_word(number)
        self.askfield.setText(number)