import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from qtwidgets import PasswordEdit
from emailMainWindow  import MainWindow


class EmailLoginWindow(qtw.QWidget):

     #将输入变量传输给主window
    submitted_email = qtc.pyqtSignal(str)
    submitted_password = qtc.pyqtSignal(str)

    def __init__(self):
        "Window when first logging into the app"
        super().__init__()
        #Main UI code goes here
        #Set the title and size for this window
        self.setWindowTitle("MyEmail")
        self.setFixedSize(650,400)
        
        #Create layout for this window
        layout = qtw.QVBoxLayout()
        self.setLayout(layout)

        #存储邮件账户与密码的变量
        self.input_email    =  qtw.QLineEdit(self,clearButtonEnabled = 1,placeholderText = "Please input your email here")
        #self.input_password =  qtw.QLineEdit(self,clearButtonEnabled = 1,placeholderText = "Please input your password here").setEchoMode(qtw.QLineEdit.Password)
        self.input_password = PasswordEdit(self,clearButtonEnabled = 1,placeholderText = "Please input your password here" )
        
       

        #flag to open main window
        self.verif_email = False
        self.verif_password = False
        #self.openMainwindow = False

        #Create layout form for this window 
        form_layout = qtw.QFormLayout()
        form_layout.setFormAlignment(qtc.Qt.AlignCenter)
        layout.addLayout(form_layout)

        #Empty space
        form_layout.addRow(qtw.QLabel('',alignment = 5))
        form_layout.addRow(qtw.QLabel('',alignment = 5))
        #
        form_layout.addRow(qtw.QLabel('<b>Welcome to MyEmail APP</b>',alignment = 5))
        form_layout.addRow(qtw.QLabel('',alignment = 5))
        form_layout.addRow(qtw.QLabel('<b>Please enter the details of the account you would like to bind with MyEmail</b>',alignment = 5))
        form_layout.addRow(qtw.QLabel('',alignment = 5))
        form_layout.addRow('Email:',self.input_email)
        form_layout.addRow('Password:',self.input_password)
        form_layout.addRow(qtw.QLabel('',alignment = 5))
        
        #Create the next button
        next_button = qtw.QPushButton("Next",checkable = False)
        layout.addWidget(next_button,alignment=qtc.Qt.AlignCenter)
        next_button.clicked.connect(self.test_input_values)

        self.show()

    def openMainWindow(self):
        "Opens MainWindow"
        self.mw = MainWindow()
        self.submitted_password.connect(self.mw.email_label.setText)
        self.submitted_password.connect(self.mw.password_label.setText)
        self.mw.show()
        #return self.mw
        


    def test_input_values(self):
        "function that tests if entered email and password are correct"
        if self.input_email.text():
            self.verif_email= True
            self.submitted_email.emit(self.input_email.text())
        else:
            self.verif_email = False
            qtw.QMessageBox.warning(self,'Warning','The email cannot be blank')
        if self.input_password.text():
            self.verif_password = True
            self.submitted_password.emit(self.input_password.text())
            self.openMainWindow()
            self.close()
        else:
            self.verif_password = False
            qtw.QMessageBox.warning(self,'Warning','The password cannot be blank')


        #End main UI code
    

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    elw = EmailLoginWindow()
    sys.exit(app.exec()) 




