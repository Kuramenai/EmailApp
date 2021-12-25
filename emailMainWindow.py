from email.message import EmailMessage
import sys
import smtplib
import imaplib
import email
from typing import Text
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc


class MainWindow(qtw.QMainWindow):
    def __init__(self,email,password,mail,server_SMPTP):
        "Main Window constructor"
        super().__init__()

        #Main UI code goes here
        #Set the title and size for this window
        self.setWindowTitle("MyEmail")
        self.winWidth = 1200
        self.winHeight = 900
        self.setFixedSize(self.winWidth,self.winHeight)

        #Servers
        self.mail = mail
        self.server = server_SMPTP

        #存储邮件账户与密码
        self.my_email = email
        self.password = password
        self.email_label = qtw.QLabel(email)
        self.password_label = qtw.QLabel(password)

        self.my_messages = []
        self.mails_list = qtw.QListWidget()
        self.current_item = 0
        self.selected_items = []
        self.source2display = 0
        
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
        self.tab1 = self.new_email_tab()
        self.tab2 = self.sent_tab()
        self.tab3  = self.inbox_tab()
        self.tab4 = self.account_tab()
        self.tab5 = self.read_email_tab()

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
        self.update_tab()

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

    def update_tab(self):
        "Function that updates the tabs layout when there are new changes"
        self.right_widget.addTab(self.tab1, '')
        self.right_widget.addTab(self.tab2, '')
        self.right_widget.addTab(self.tab3, '')
        self.right_widget.addTab(self.tab4, '')
        self.right_widget.addTab(self.tab5, '')

#SideMenu Buttons   
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
   
    def btn_read_email(self):
        "Opens the read email tab" 
        self.right_widget.setCurrentIndex(4)

#Important Functions
    # def login_in(self):
    #     "Test if user has been logging in"
    #     #print('step2')
    #     try:
    #         if (self.login == False):
    #             self.mail.login(self.my_email,self.password)
    #             #print('step2"')
    #             self.login = True
    #     except Exception as error:
    #         print(error)
    #         self.login = False

    def send_function(self):
        "Implement the sending function"
        try:
            if self.receiver.text() == '':
                qtw.QMessageBox.warning(self,'Warning','The receiver cannot be blank')
                return
            else: 
                message2Send = 'Subject: {}\n\n{}'.format(self.subject.text(),self.body.toPlainText())
                # server = smtplib.SMTP('smtp.gmail.com',587)#'smtp.gmail.com',587
                # server.starttls()
                # server.login(self.my_email,self.password)
                self.server.sendmail(self.my_email,self.receiver.text(),message2Send)
                print("Message Sent")
        except Exception as error:
            print(error)
            print("Message Not Sent")

    def check_for_new_mails(self):
        "Check if there are new emails"
        #print('step3')
        #self.login_in()
        #if self.login:
        self.mail.select('inbox')
        _, search_data = self.mail.search(None,'UNSEEN')
    
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
                    email_data['body'] = body.decode()
                    #print(body.decode())
                elif part.get_content_type() == 'text/html':
                    body = part.get_payload(decode= True)
                    email_data['body'] = body.decode()
                    # print(body.decode())
            self.my_messages.append(email_data)
    
    def display_emails_list(self):
        "Display emails in the inbox tab"
        #Get the number of emails before update maillist
        old_emails_counter = len(self.my_messages)
        #Check for new messages
        self.check_for_new_mails()
        #Get the number of emails before update maillist
        new_emails_counter = len(self.my_messages)

        if self.my_messages and self.source2display == 0:
            print('step1')
            for email_data in self.my_messages:
                self.source2display = 1 
                item_title = f"From : {email_data['from'] } \nSubject : {email_data['subject']}\nDate : {email_data['date']}"
                item = qtw.QListWidgetItem(item_title)
                self.mails_list.addItem(item)
        elif new_emails_counter > old_emails_counter and self.source2display == 1:
            print('step2')
            for email_data in self.my_messages[old_emails_counter:new_emails_counter]:
                item_title = f"From : {email_data['from'] } \nSubject : {email_data['subject']}\nDate : {email_data['date']}"
                item = qtw.QListWidgetItem(item_title)
                self.mails_list.addItem(item)
        else:
            print("no new emails")

    def refresh_function(self):
        "Function to display to new emails if there are"
        self.right_widget.clear()
        self.tab3 = self.inbox_tab()
        self.update_tab()
        self.btn_inbox_function()
    
    def helper_function(self,item):
        "Method to browse email content"
        self.current_item = self.mails_list.row(item)
        self.right_widget.removeTab(4)
        self.new_read_email_tab = self.read_email_tab()
        self.right_widget.addTab(self.new_read_email_tab,'')
        self.btn_read_email()

    def delete_email(self,item):
        "Delete emails"
        # self.tab3 = self.inbox_tab()
        # print("step1")
        # print(len(self.selected_items))
        # if self.selected_items :
        #     print("step2")
        #     for item in self.selected_items:
        #         self.mails_list.removeItemWidget(item)
        #         self.my_messages.remove(self.mails_list.row(item))
        #         self.refresh_function()
       
    def forward_function(self):
        pass
#Tabs
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
        from_label.setTextInteractionFlags(qtc.Qt.TextSelectableByMouse)
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
        #Create the layout for this tab
        self.inbox_layout = qtw.QVBoxLayout()
        header_layout = qtw.QHBoxLayout()
        #Create the Search,Refresh ,Select and Delete Buttons
        refresh_button = qtw.QPushButton("Refresh")
        refresh_button.clicked.connect(self.refresh_function)

        search_button = qtw.QPushButton("Search")
        #select_button.clicked.connect(self.search_function)

        delete_button = qtw.QPushButton("Delete")
        delete_button.clicked.connect(self.delete_email)
        
       
        self.search =  qtw.QLineEdit(self,clearButtonEnabled = 0,placeholderText = "Search for emails")

        #Adding the widgets to the layout
        header_layout.addWidget(self.search)
        header_layout.addWidget(search_button)
        header_layout.addSpacing(50)
        header_layout.addWidget(refresh_button)
        header_layout.addWidget(delete_button)
        
        #layout for the header of this tab
        self.inbox_layout.addLayout(header_layout)
        
        #Check for new emails
        self.display_emails_list()
        
        #Functions for the button
        self.mails_list.itemDoubleClicked.connect(self.helper_function)
        self.mails_list.itemClicked.connect(self.delete_email)
        self.inbox_layout.addWidget(self.mails_list)

        #Main Widget for this tab
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

    def read_email_tab(self):
        "Layout for the read email tab"
        read_email_layout = qtw.QVBoxLayout()
       
        #Create the Forward Button
        forward_button = qtw.QPushButton("Forward")
        forward_button.clicked.connect(self.forward_function)

        read_email_layout.addWidget(forward_button)

        if self.my_messages :
            print(f'inside:{self.current_item}')
            email_data = self.my_messages[self.current_item]
            from_text = qtw.QLabel(f'From:  {email_data["from"]}')
            from_text.setTextInteractionFlags(qtc.Qt.TextSelectableByMouse)
            subject_text =  qtw.QLabel(f'Subject:    {email_data["subject"]}')
            subject_text.setTextInteractionFlags(qtc.Qt.TextSelectableByMouse)
            date_text =  qtw.QLabel(f'Date: {email_data["date"]}')
            date_text.setTextInteractionFlags(qtc.Qt.TextSelectableByMouse)
            body_text  =  qtw.QTextBrowser()
            body_text.setText(email_data['body'])

            read_email_layout.addSpacing(20)
            read_email_layout.addWidget(from_text)
            read_email_layout.addWidget(subject_text)
            read_email_layout.addWidget(date_text)
            read_email_layout.addSpacing(10)
            read_email_layout.addWidget(body_text)

        main = qtw.QWidget()
        main.setLayout(read_email_layout)
        return main

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow('alkanstephen@gmail.com','abc1235*ULTRA',)
    sys.exit(app.exec()) 




