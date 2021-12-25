import sys
import smtplib
import imaplib
import smtplib
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from qtwidgets import PasswordEdit
from emailMainWindow  import MainWindow


class EmailLoginWindow(qtw.QWidget):

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

        #IMAP Server for Gmail
        #Create the server
        self.host = 'imap.gmail.com'
        self.server = self.host
        self.mail  = imaplib.IMAP4_SSL(self.server)

        #IMAP Server for QQ
        #Create the server
        self.mail_qq  = imaplib.IMAP4_SSL('imap.qq.com')

        #flag to open main window
        self.verif_email = False
        self.verif_password = False
        self.login_IMAP = False
        self.login_SMTP = False

        #存储邮件账户与密码的变量
        self.input_email    =  qtw.QLineEdit(self,clearButtonEnabled = 1,placeholderText = "Please input your email here")
        #self.input_password =  qtw.QLineEdit(self,clearButtonEnabled = 1,placeholderText = "Please input your password here").setEchoMode(qtw.QLineEdit.Password)
        self.input_password = PasswordEdit(self,clearButtonEnabled = 1,placeholderText = "Please input your password here" )
        

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
        #form_layout.addRow(qtw.QLabel('',alignment = 5))
        
        self.qq = qtw.QRadioButton("QQMail")
        self.gmail = qtw.QRadioButton("GMail")

        layout.addWidget(self.qq)        
        layout.addWidget(self.gmail)

        #Create the next button
        next_button = qtw.QPushButton("Login",checkable = False)
        layout.addWidget(next_button,alignment=qtc.Qt.AlignCenter)
        next_button.clicked.connect(self.test_input_values)

        self.show()

    def login_in_IMAP_func(self):
        "Test if user has been logging in"
    
        try:
            if self.gmail.isChecked():
                if (self.login_IMAP == False):
                    self.mail.login(self.input_email.text(),self.input_password.text())
                    self.login_IMAP = True
            elif self.qq.isChecked():
                if (self.login_IMAP == False):
                    self.mail_qq.login(self.input_email.text(),self.input_password.text())
                    self.login_IMAP = True    
            else:
                qtw.QMessageBox.warning(self,'Warning','Please an email provider')
        except Exception as error:
            qtw.QMessageBox.warning(self,'Error Login',f'{str(error)}\nPlease be sure your email and password are corrrect')
            self.login_IMAP= False

    def login_in_SMPT_func(self):
        "Test if user has been logging in"
        try:
            if self.gmail.isChecked():
                if (self.login_SMTP == False):
                    self.server_SMPTP = smtplib.SMTP('smtp.gmail.com',587)#'smtp.gmail.com',587
                    self.server_SMPTP.starttls()
                    self.server_SMPTP.login(self.input_email.text(),self.input_password.text())
                    self.login_SMTP = True
            elif self.qq.isChecked():
                 if (self.login_IMAP == False):
                    self.server_SMPTP = smtplib.SMTP_SSL('smtp.qq.com', smtplib.SMTP_SSL_PORT)
                    self.server_SMPTP.starttls()
                    self.server_SMPTP.login(self.input_email.text(),self.input_password.text())
                    self.login_SMTP = True
                
            else:
                qtw.QMessageBox.warning(self,'Warning','Please an email provider')

        except Exception as error:
            qtw.QMessageBox.warning(self,'Error Login',f'{str(error)}\nPlease be sure your email and password are corrrect')
            self.login_SMTP = False


    def openMainWindow(self):
        "Opens MainWindow"
        if(self.verif_email  and self.verif_password ):
            self.login_in_IMAP_func()
            self.login_in_SMPT_func()
            print(self.login_SMTP)
            print(self.login_SMTP)
            if self.login_SMTP and self.login_IMAP :
                self.mw = MainWindow(self.input_email.text(),self.input_password.text(),self.mail,self.server_SMPTP)
                self.close()
                self.mw.show()
        else:
            pass
        
    def test_input_values(self):
        "function that tests if entered email and password are correct"
        if self.input_email.text():
            self.verif_email= True
            self.openMainWindow()
        else:
            self.verif_email = False
            qtw.QMessageBox.warning(self,'Warning','The email cannot be blank')
        if self.input_password.text():
            self.verif_password = True
            self.openMainWindow()
        else:
            self.verif_password = False
            qtw.QMessageBox.warning(self,'Warning','The password cannot be blank')


        #End main UI code
    

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    elw = EmailLoginWindow()
    sys.exit(app.exec()) 




