import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc


class MainWindow(qtw.QMainWindow):
    def __init__(self):
        "Main Window constructor"
        super().__init__()

        #Main UI code goes here
        #Set the title and size for this window
        self.setWindowTitle("MyEmail")
        self.winWidth = 1200
        self.winHeight = 900
        self.setFixedSize(self.winWidth,self.winHeight)

        #存储邮件账户与密码
        self.email_label = qtw.QLabel('')
        self.password_label = qtw.QLabel('')
        

        #Create the buttons for the sidebar menu
        self.new_email_button = qtw.QPushButton("New Email")
        self.sent_button = qtw.QPushButton("Sent")
        self.inbox_button = qtw.QPushButton("Inbox")
        self.account_button = qtw.QPushButton("Account")

        #Connect the buttons with the appropriate functions
        self.new_email_button.clicked.connect(self.btn_email_function)
        self.sent_button.clicked.connect(self.btn_sent_function)
        self.inbox_button.clicked.connect(self.btn_inbox_function)
        self.account_button.clicked.connect(self.btn_account_function)

        #Create a tab for when every button is pressed
        self.new_email_tab = self.new_email_tab()
        self.sent_tab = self.sent_tab()
        self.inbox_tab  = self.inbox_tab()
        self.account_tab = self.account_tab()

        self.initUI()
        #End main UI code
        self.show()

    def initUI(self):
        "Function that defines the main layout for the window"
        #Defines the layout as vertical
        left_layout = qtw.QVBoxLayout()
        #Adding the buttons to the layout
        left_layout.addWidget(self.new_email_button)
        left_layout.addWidget(self.sent_button)
        left_layout.addWidget(self.inbox_button)
        left_layout.addWidget(self.account_button)

        left_layout.addStretch(5)
        left_layout.setSpacing(20)
        #Widget for the left part of the screen
        left_widget = qtw.QWidget()
        left_widget.setLayout(left_layout)

        #Defines widget for the right part of the screen
        self.right_widget = qtw.QTabWidget()
        self.right_widget.tabBar().setObjectName("mainTab")
        #Adding tabs to the tab Widget
        self.right_widget.addTab(self.new_email_tab, '')
        self.right_widget.addTab(self.sent_tab, '')
        self.right_widget.addTab(self.inbox_tab, '')
        self.right_widget.addTab(self.account_tab, '')

       # 下面这段代码隐藏了标签部件的标签并初始化显示页面
        self.right_widget.setCurrentIndex(1)
        self.right_widget.setStyleSheet('''QTabBar::tab{width: 0; \ height: 0; margin: 0; padding: 0; border: none;}''')

        #Defines the main layout
        main_layout = qtw.QHBoxLayout()
        main_layout.addWidget(left_widget)
        main_layout.addWidget(self.right_widget)
        #
        main_layout.setStretch(0, 40)
        main_layout.setStretch(1, 200)
        #
        main_widget = qtw.QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
    
    def btn_email_function(self):
        "Opens the new email tab"
        self.right_widget.setCurrentIndex(0)
    def btn_sent_function(self):
        "Opens the sent tab"
        self.right_widget.setCurrentIndex(1)
    def btn_inbox_function(self):
        "Opens the inbox tab"
        self.right_widget.setCurrentIndex(2)
    def btn_account_function(self):
        "Opens the account tab"
        self.right_widget.setCurrentIndex(3)

    def new_email_tab(self):
        "Layout for the email tab"
        main_layout = qtw.QVBoxLayout()
        main_layout.addWidget(qtw.QLabel('page 1'))
        main_layout.addWidget(self.email_label)
        main_layout.addWidget(qtw.QLabel('page 1'))
        main_layout.addWidget(self.password_label)
        main_layout.addStretch(5)
        main = qtw.QWidget()
        main.setLayout(main_layout)
        return main

    def sent_tab(self):
        "Layout for the sent tab"
        main_layout = qtw.QVBoxLayout()
        main_layout.addWidget(qtw.QLabel('page 2'))
        main_layout.addStretch(5)
        main = qtw.QWidget()
        main.setLayout(main_layout)
        return main
        
    def inbox_tab(self):
        "Layout for the inbox tab"
        main_layout = qtw.QVBoxLayout()
        main_layout.addWidget(qtw.QLabel('page 3'))
        main_layout.addStretch(5)
        main = qtw.QWidget()
        main.setLayout(main_layout)
        return main

    def account_tab(self):
        "Layout for the account tab"
        main_layout = qtw.QVBoxLayout()
        main_layout.addWidget(qtw.QLabel('page 4'))
        main_layout.addStretch(5)
        main = qtw.QWidget()
        main.setLayout(main_layout)
        return main

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec()) 




