import sys
import smtplib
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from qtwidgets import PasswordEdit
from email_Login import EmailLoginWindow
from emailMainWindow  import MainWindow

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    elw = EmailLoginWindow()
    sys.exit(app.exec()) 
     

