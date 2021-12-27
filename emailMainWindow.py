from email.message import EmailMessage
import sys
import smtplib
import imaplib
import email
import quopri
from email.mime.text import MIMEText
from typing import Text
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc


class MainWindow(qtw.QMainWindow):
    def __init__(self,email,password,mail,server_SMTP):
        "Main Window constructor"
        super().__init__()

        #Main UI code goes here
        #Set the title and size for this window
        self.setWindowTitle("MyEmail")
        self.winWidth = 1200
        self.winHeight = 900
        self.setFixedSize(self.winWidth,self.winHeight)

        self.font = qtg.QFont("Consolas", 10)
        self.setFont(self.font)

        #Servers
        self.mail = mail
        self.server = server_SMTP

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
        self.delete_signal = False
        self.refresh_signal = False
        
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
        self.tab6 = self.search_results_tab()

        self.initUI()
        #End main UI code
        self.show()

    def initUI(self):
        "Function that defines the main layout for the window"
        #Defines the layout as vertical
        left_layout = qtw.QVBoxLayout()
        #Adding the buttons to the layout
        left_layout.addSpacing(5)
        left_layout.addWidget(self.new_email_button)
        left_layout.addWidget(self.sent_button)
        left_layout.addWidget(self.inbox_button)
        left_layout.addWidget(self.account_button)

        left_layout.addStretch(5)
        left_layout.setSpacing(20)
        #Widget for the left part of the screen
        left_widget = qtw.QWidget()
        left_widget.setFont(self.font)
        left_widget.setLayout(left_layout)

        #Defines widget for the right part of the screen
        self.right_widget = qtw.QTabWidget()
        self.right_widget.setFont(self.font)
        self.right_widget.tabBar().setObjectName("mainTab")
        #Adding tabs to the tab Widget
        self.update_tab()

       # 隐藏了标签部件的标签并初始化显示页面
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
        main_widget.setFont(self.font)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
    
    def closeEvent(self, event):
        "Disconnecting to the servers"
        self.server.close()
        self.mail.logout()
        qtw.QMessageBox.information(self,'Notification','Logging Out...')
    
    def my_unicode(s, encoding):
      if encoding:
            return str(s, encoding)
      else:
            return (s)

    

    def update_tab(self):
        "Function that updates the tabs layout when there are new changes"
        self.right_widget.addTab(self.tab1, '')
        self.right_widget.addTab(self.tab2, '')
        self.right_widget.addTab(self.tab3, '')
        self.right_widget.addTab(self.tab4, '')
        self.right_widget.addTab(self.tab5, '')
        self.right_widget.addTab(self.tab6, '')
        self.right_widget.setFont(self.font)

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
    def btn_search_mail(self):
        "Opens the search email tab" 
        self.right_widget.setCurrentIndex(5)

#Important Functions
    def send_function(self):
        "Implement the sending function"
        try:
            if self.receiver.text() == '':
                qtw.QMessageBox.warning(self,'Warning','The receiver cannot be blank')
                return
            else:
                text_type = 'plain'
                msg2Send = MIMEText(self.body.toPlainText(),text_type,'utf-8') 
                msg2Send['Subject']  = self.subject.text()
                msg2Send['From']  =  self.my_email
                msg2Send['To']  = self.receiver.text()
                self.server.send_message(msg2Send)
                #message2Send = 'Subject: {}\n\n{}'.format(self.subject.text(),self.body.toPlainText())
                #self.server.sendmail(self.my_email,self.receiver.text(),msg2Send.as_string())
                qtw.QMessageBox.information(self,'Notificatioon','Message Sent')
        except Exception as error:
            print(error)
            qtw.QMessageBox.information(self,'Notificatioon','Message Not Sent')

    def check_for_new_mails(self):
        "Check if there are new emails"
        self.mail.select('inbox')
        _, search_data = self.mail.search(None,'UNSEEN')
        #self.mail.store(search_data[0].replace(' ',','),'+FLAGS','\Seen')
        for num in search_data[0].split():
            
            email_data = {}

            _, data = self.mail.fetch(num,"RFC822")
            _,b = data[0]
            email_message = email.message_from_bytes(b)

            Sender = email_message['from'].split()
            if len(Sender) == 2 :
                sender_name = email.header.decode_header((Sender[0]).strip('\"'))
                sender_name = self.my_unicode(sender_name[0][0], sender_name[0][1]) + Sender[1]
            else:
                sender_name = email_message['from']
            
            subject,encoding = email.header.decode_header(email_message['subject'])[0]
            #print(subject.decode(encoding))

            string= 'v'
            bit   = b''
            ty1 = type(string)
            ty2 = type(bit)


            if type(subject) == ty1:
                email_data['subject'] = subject
            elif type(subject) == ty2:
                email_data['subject'] = subject.decode(encoding)

                
            email_data['to'] =  email_message['to']
            email_data['from'] =  sender_name
            email_data['date']   = email_message['date']


            for part in email_message.walk():
                if part.get_content_type() == 'text/plain':
                    body = part.get_payload(decode= True)

                    email_data['body'] = body.decode('utf-8')#'ISO 8859-1'

                    #print(body.decode())
                elif part.get_content_type() == 'text/html':
                    body = part.get_payload(decode= True)
                    email_data['body'] = body.decode('utf-8')
                    # print(body.decode())
            self.my_messages.insert(0,email_data)
           # _, response = self.mail.store(num, '+FLAGS', r'(\Seen)')
    
    def display_emails_list(self):
        "Display emails in the inbox tab"
        if self.source2display == 0:
            print('step1')
            self.check_for_new_mails()
            if self.my_messages:
                for email_data in self.my_messages:
                    self.source2display = 1 
                    From,Subject,Date =  email_data['from'],email_data['subject'],email_data['date']
                    item_title = "{:45s}{:20s}{:50s}".format(From,Subject,Date)
                    item = qtw.QListWidgetItem(item_title)
                    item.setFont(self.font)
                    self.mails_list.addItem(item)
        elif self.refresh_signal:
            print('step2')
            #Get the number of emails before update maillist
            old_emails_counter = len(self.my_messages)
            #Check for new messages
            self.check_for_new_mails()
            #Get the number of emails before update maillist
            new_emails_counter = len(self.my_messages)
            if new_emails_counter > old_emails_counter: # and self.source2display == 1:
                print('step2_1')
                for email_data in self.my_messages[0:new_emails_counter - old_emails_counter]:
                    From,Subject,Date =  email_data['from'],email_data['subject'],email_data['date']
                    item_title = "{:45s}{:20s}{:50s}".format(From,Subject,Date)
                    item = qtw.QListWidgetItem(item_title)
                    item.setFont(self.font)
                    self.mails_list.insertItem(0,item)
                self.refresh_signal = False
            else:
                print("no new emails")
                self.refresh_signal = False
        elif self.delete_signal:
            print('step3')
            #self.inbox_layout.replaceWidget(self.mails_list,self.mails_list)
            self.delete_signal = False
        else:
            print("no change")

    def refresh_function(self):
        "Function to display to new emails if there are"
        self.refresh_signal = True
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

    def delete_email(self):
        "Delete emails"
        if self.my_messages:
            self.delete_signal = True
            current_item_index = self.mails_list.currentRow()
            item = self.mails_list.takeItem(current_item_index)
            self.my_messages.remove(self.my_messages[current_item_index])
            self.right_widget.clear()
            self.tab3 = self.inbox_tab()
            self.update_tab()
            self.btn_inbox_function()
            
    def search_function(self):
        "Search for emails"
        searched_results = self.mails_list.findItems(self.search.text(),qtc.Qt.MatchContains)
        if searched_results:
            self.right_widget.clear()
            self.tab6 = self.search_results_tab()
            self.update_tab()
            self.btn_search_mail()
        else:
            qtw.QMessageBox.information(self,'Notification','No Matches Found')
        
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
        self.receiver   =  qtw.QLineEdit(self,clearButtonEnabled = 1,placeholderText = "Please input the email address of the receiver here")
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
        main.setFont(self.font)
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
        search_button.clicked.connect(self.search_function)

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
        
        #Functions for the double click action onthe item
        self.mails_list.itemDoubleClicked.connect(self.helper_function)

        self.mails_list.setFont(self.font)
        self.inbox_layout.addWidget(self.mails_list)

        #Main Widget for this tab
        main = qtw.QWidget()
        main.setFont(self.font)
        main.setLayout(self.inbox_layout)
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
            from_text = qtw.QLabel(f'From:   {email_data["from"]}')
            from_text.setTextInteractionFlags(qtc.Qt.TextSelectableByMouse)
            subject_text =  qtw.QLabel(f'Subject:{email_data["subject"]}')
            subject_text.setTextInteractionFlags(qtc.Qt.TextSelectableByMouse)
            date_text =  qtw.QLabel(f'Date:   {email_data["date"]}')
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
        main.setFont(self.font)
        main.setLayout(read_email_layout)
        return main
    
    def search_results_tab(self):
        "Display the search results"
        #Create the layout for this tab
        search_tab_layout = qtw.QVBoxLayout()
    
        search_label = qtw.QLabel(f'<b>Displaying results for ({self.search.text()}) </b>')
        searched_list_items = qtw.QListWidget()
        searched_results = self.mails_list.findItems(self.search.text(),qtc.Qt.MatchContains)
        if searched_results:
            for item in searched_results:
                print('Matches Found')
                index = self.mails_list.row(item)
                email_data = self.my_messages[index]
                From,Subject,Date =  email_data['from'],email_data['subject'],email_data['date']
                item_title = "{:45s}{:20s}{:50s}".format(From,Subject,Date)
                s_item = qtw.QListWidgetItem(item_title)
                s_item.setFont(self.font)
                searched_list_items.addItem(s_item)
        else:
            pass
        search_tab_layout.addWidget(search_label)
        search_tab_layout.addWidget(searched_list_items)

        #Main Widget for this tab
        main = qtw.QWidget()
        main.setFont(self.font)
        main.setLayout(search_tab_layout)
        return main
        #Functions for the double click action on the items
        #self.mails_list.itemDoubleClicked.connect(self.helper_function)
        
    def sent_tab(self):
        "Layout for the sent tab"
        main_layout = qtw.QVBoxLayout()
        main_layout.addWidget(qtw.QLabel('page 2'))
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
    mw = MainWindow('alkanstephen@gmail.com','abc1235*ULTRA',)
    sys.exit(app.exec()) 




