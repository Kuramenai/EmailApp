from PyQt5.QtWidgets import *
import sys


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        # set the title of main window
        self.setWindowTitle('Sidebar layout - www.luochang.ink')

        # set the size of window
        self.Width = 800
        self.height = int(0.618 * self.Width)
        self.resize(self.Width, self.height)
		
        self.x = 0
		# add all widgets
        self.btn_1 = QPushButton('1', self)
        self.btn_2 = QPushButton('2', self)
        self.btn_3 = QPushButton('3', self)
        self.btn_4 = QPushButton('4', self)

        self.tab1 = self.ui1()
        self.tab2 = self.ui2()
        self.tab3 = self.ui3()
        self.tab4 = self.ui4()

       

        self.initUI()

    def initUI(self):
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.btn_1)
        left_layout.addWidget(self.btn_2)
        left_layout.addWidget(self.btn_3)
        left_layout.addWidget(self.btn_4)
        left_layout.addStretch(5)
        left_layout.setSpacing(20)
        left_widget = QWidget()
        left_widget.setLayout(left_layout)

        self.right_widget = QTabWidget()
        self.right_widget.tabBar().setObjectName("mainTab")

        self.right_widget.addTab(self.tab1, '')
        self.right_widget.addTab(self.tab2, '')
        self.right_widget.addTab(self.tab3, '')
        self.right_widget.addTab(self.tab4, '')

        main_layout = QHBoxLayout()
        main_layout.addWidget(left_widget)
        main_layout.addWidget(self.right_widget)
        main_layout.setStretch(0, 40)
        main_layout.setStretch(1, 200)
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
    
    def test_function(self):
        self.x += 1
        print(self.x)

    def ui1(self):
        main_layout = QVBoxLayout()
        test_button =QPushButton('Test')
        main_layout.addWidget(QLabel('page 1'))
        main_layout.addWidget(test_button)
        test_button.clicked.connect(self.test_function)
        main_layout.addStretch(5)
        main = QWidget()
        main.setLayout(main_layout)
        return main
    
    def ui2(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel(str(self.x)))
        main_layout.addStretch(5)
        main = QWidget()
        main.setLayout(main_layout)
        return main
    
    def ui3(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel('page 3'))
        main_layout.addStretch(5)
        main = QWidget()
        main.setLayout(main_layout)
        return main
    
    def ui4(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel('page 4'))
        main_layout.addStretch(5)
        main = QWidget()
        main.setLayout(main_layout)
        return main
        
        
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec_())
