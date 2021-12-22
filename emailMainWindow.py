import sys
import smtplib
import imaplib
import email
from typing import Text
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc


class MainWindow(qtw.QMainWindow):
    def __init__(self,email,password):
        "Main Window constructor"
        super().__init__()

        #Main UI code goes here
        #Set the title and size for this window
        self.setWindowTitle("MyEmail")
        self.winWidth = 1200
        self.winHeight = 900
        self.setFixedSize(self.winWidth,self.winHeight)

        #Create the server
        self.host = 'imap.gmail.com'
        self.server = self.host
        self.mail  = imaplib.IMAP4_SSL(self.server)
        self.login = False
       
        #存储邮件账户与密码
        self.my_email = email
        self.password = password
        self.email_label = qtw.QLabel(email)
        self.password_label = qtw.QLabel(password)
        
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

        #Create a tab for when each sidebar button is pressed
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
        self.right_widget.setCurrentIndex(2)
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

    def login_in(self):
        "Test if user has been logging in"
        #print('step2')
        try:
            if (self.login == False):
                self.mail.login(self.my_email,self.password)
                #print('step2"')
                self.login = True
        except Exception as error:
            print(error)
            self.login = False

    def send_function(self):
        "Implement the sending function"
        try:
            if self.receiver.text() == '':
                qtw.QMessageBox.warning(self,'Warning','The receiver cannot be blank')
                return
            else: 
                message2Send = 'Subject: {}\n\n{}'.format(self.subject.text(),self.body.toPlainText())
                server = smtplib.SMTP('smtp.gmail.com',587)#'smtp.gmail.com',587
                server.starttls()
                server.login(self.my_email,self.password)
                server.sendmail(self.my_email,self.receiver.text(),message2Send)
                print("Message Sent")
        except Exception as error:
            print(error)
            print("Message Not Sent")

    def check_for_new_mails(self):
        "Check if there are new emails"
        #print('step3')
        self.login_in()
        if self.login:
            self.mail.select('inbox')
            _, search_data = self.mail.search(None,'UNSEEN')
            my_messages  = []
            for num in search_data[0].split():
                
                email_data = {}

                _, data = self.mail.fetch(num,"RFC822")
                _,b = data[0]
                email_message = email.message_from_bytes(b)
                
                for header in ['subject','to','from','date']:
                    #print("{}:{}".format(header,email_message[header]))
                    email_data[header] = email_message[header]

                for part in email_message.walk():
                    if part.get_content_type() == 'text/plain':
                        body = part.get_payload(decode= True)
                        email_data[body] = body.decode()
                        #print(body.decode())
                    elif part.get_content_type() == 'text/html':
                        body = part.get_payload(decode= True)
                        email_data[body] = body.decode()
                       # print(body.decode())
                my_messages.append(email_data)
            return my_messages
    
    def display_emails_list(self):
        "Display emails in the inbox tab"
        my_messages = self.check_for_new_mails()
        my_messages.reverse()
        self.mails_list = qtw.QListWidget()
        if my_messages:
            for email_data in my_messages:
                item_title = f"From : {email_data['from'] } \nSubject : {email_data['subject']}\nDate : {email_data['date']}"
                item = qtw.QListWidgetItem(item_title)
                self.mails_list.addItem(item)
        else:
            print("no new emails")
        return self.mails_list

    def refresh_function(self):
        "Function to display to new emails if there are"
        my_messages = self.check_for_new_mails()
        my_messages.reverse()
        if my_messages:
            for email_data in my_messages:
                item_title = f"From : {email_data['from'] } \nSubject : {email_data['subject']}\nDate : {email_data['date']}"
                item = qtw.QListWidgetItem(item_title)
                self.mails_list.addItem(item)
            self.inbox_layout.replaceWidget(self.mails_list,self.mails_list)
        else:
            print("no new emails")
        

    def new_email_tab(self):
        "Layout for the email tab"
         #create the layout for this tab
        main_layout = qtw.QVBoxLayout()
        header_layout = qtw.QHBoxLayout()
        form_layout = qtw.QFormLayout()
        form_layout.setFormAlignment(qtc.Qt.AlignCenter)
        #create the "send button" and the "insert button"
        send_button = qtw.QPushButton("Send")
        send_button.clicked.connect(self.send_function)
        insert_button = qtw.QPushButton("Insert")
        #insert_button.clicked.connect('')
        # "From" label
        from_label = qtw.QLabel(f"From:     {self.email_label.text()}")
        # Receiver and Subject input"
        self.receiver    =  qtw.QLineEdit(self,clearButtonEnabled = 1,placeholderText = "Please input the email address of the receiver here")
        self.subject    =  qtw.QLineEdit(self,clearButtonEnabled = 1,placeholderText = "Please input the subject of the email here")
        self.body = qtw.QTextEdit(self,placeholderText = "Enter your text here",acceptRichText = False,
                                        lineWrapMode = qtw.QTextEdit.FixedColumnWidth,
                                        lineWrapColumnOrWidth = 100)
        #Adding receiver and subject to the form layout 
        form_layout.addRow('To:',self.receiver)
        form_layout.addRow('Subject:',self.subject)
        #Adding the buttons to the layout
        header_layout.addWidget(insert_button)
        header_layout.addWidget(send_button)
        
        main_layout.addLayout(header_layout)
        main_layout.addWidget(from_label)
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.body)
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
        self.inbox_layout = qtw.QVBoxLayout()
        header_layout = qtw.QHBoxLayout()
        #Create the Refresh and Select Button
        refresh_button = qtw.QPushButton("Refresh")
        refresh_button.clicked.connect(self.refresh_function)
        search_button = qtw.QPushButton("Search")
        #select_button.clicked.connect(self.search_function)
        select_button = qtw.QPushButton("Select")
        #select_button.clicked.connect(self.select_function)
        self.search =  qtw.QLineEdit(self,clearButtonEnabled = 0,placeholderText = "Search for emails")
        header_layout.addWidget(self.search)
        header_layout.addWidget(search_button)
        header_layout.addSpacing(50)
        header_layout.addWidget(refresh_button)
        header_layout.addWidget(select_button)
        
        self.inbox_layout.addLayout(header_layout)
        
        mails_list = self.display_emails_list()
        self.inbox_layout.addWidget(mails_list)

        main = qtw.QWidget()
        main.setLayout(self.inbox_layout)
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
    mw = MainWindow('alkanstephen@gmail.com','MSC102hynix5*ULTRA')
    sys.exit(app.exec()) 




