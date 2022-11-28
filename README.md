# EasyMail

[中文](#c)

EasyMail是一个使用Python编写的电子邮件收发客户端。此项目是武汉大学计算机网络课程的大作业。

项目主要使用SMTP和POP3协议收发邮件，使用PyQt5编写用户界面，使用MySQL管理数据库。

实现细节以及代码描述如下。

[English](#e)

EasyMail is an email client written in Python. This project is the major assignment of the computer network course of Wuhan University. 

The project mainly uses SMTP and POP3 protocols to send and receive mail, PyQt5 to write the user interface, and MySQL to manage the database. 

The implementation details and code are described below. 



<a id= "c">   </a>



 #### 邮件封装与生成

本实验中设置Mail类。其中uid在发件时为正文md5 hash函数值，收件时为POP3协议中生成的邮件唯一标识符。

邮件封装生成通过Sender_proc类实现，代码见附录2。邮件初始化时需前端提供邮件发件人，收件人，主题，正文内容四条信息，并通过gene_mail()函数生成初始邮件。gene_mail()函数将类初始化的内容按照标准的邮件报文格式生成标准邮件报文，并按照utf-8编码生成对应的字符串。同时生成邮件时再邮件报文内写入时间戳，可以在提供发件人发送时间的同时使邮件内容不存在重复，即hash函数值不存在相同情况，便于数据库管理。

gene_mailclass()函数将提供的初始化值生成对应的Mail对象，便于发件系统处理。其中，uid通过gene_uid()函数生成。

gene_uid()函数通过md5函数生成邮件报文的md5哈希值，由于初始化Sender_proc类时便注入时间戳，因此生成的hash在邮件信息相同的情况下仍不会出现相同情况。

store()函数将生成的邮件报文与Mail对象按照一定的规则存储在磁盘对应的路径下。本程序设置的发件路径为C:\MailSever\Draft若不存在对应路径则生成该路径。存储与写入则通过Python标准的open()与close()函数实现。存储的文件名则为uid.txt，即通过邮件报文的uid作为邮件存储在本地的文件名称，这样可保证文件不会出现重复情况。

add_to_sql()函数将生成的Mail对象存储进数据库中。通过数据库连接模块提供的写入数据库的接口add_sql()将Mail对象中的元素写入Draft关系表中。

delete_draft()函数提供将草稿箱中邮件从本地以及数据库中删除的接口。通过os.remove()函数与数据库连接的接口delete_sql()函数从本地以及数据库中删除。

Sender_proc类使用时，执行流程为：初始化—生成邮件报文—生成Mail对象—存储—连接数据库。发送邮件时可无需连接进数据库，之后并调用Smtp发送类对生成的邮件进行发送。

#### SMTP客户端实现

Smtp类发送前需初始化邮件服务器，用户名，密码以及发送邮件的Mail对象与存储邮件的地址，其中地址默认为C:\MailSever\Draft。

发送时调用socket库进行网络编程操作，并按照SMTP协议进行发送操作。首先通过connect()函数通过SMTP的25号端口连接到邮件服务器，若链接成功则返回2，每次在发送信息后通过sleep()函数等待0.8秒后再读取返回缓冲区的内容，若等待时间过短则会出现无法连接的情况。每次在读取返回信息后对返回信息进行判断，若成功则进行下一步，若失败则返回对应错误代码。链接成功后向服务器发送HELO命令，若成功返回250，每次发送时通过encode()函数对发送信息进行编码，接收时通过decode()函数对接收到的信息进行解码。

返回250后发送AUTH LOGIN命令。若返回334则成功。之后通过base64编码向服务器发送用户的用户名与密码，发送前通过base64.b64encode ()函数对发送的信息进行编码。发送用户名时返回334，发送密码后返回235则证明用户验证成功。验证成功后则发送MAIL FROM命令，格式为MAIL FROM: +<+mail.sender+>+\r\n。若返回250则证明发送成功。之后发送RCPT TO命令，格式为RCPT TO: +<+mail.receiver+>\r\n。若返回250则表示发送成功。

成功后发送DATA命令准备发送邮件报文，若返回354则证明邮件服务器已准备好接收邮件报文。程序通过初始化的本地路径读取对应的邮件报文，并发送至邮件服务器，之后发送\r\n.\r\n表示正文发送完毕。若返回250则证明发送完成，之后发送QUIT命令完成邮件发送。

#### POP3客户端实现

邮件接收类Pop3在接收前初始化对应的邮件服务器、用户名、密码三条信息，并通过recvmail(operation,index)函数接收邮件，其中operation提供LIST，RETR，DELE三种指令，RETR与DELE需提供用于操作的index参数。LIST为更新邮件列表，RETR为下载对应邮件，DELE为删除对应邮件。

程序与发送邮件一样，通过connect()函数通过110端口与服务器建立连接，若链接成功，则返回数据中前三个字符为‘+OK’。连接建立成功后发送USER命令，并发送用户名，若连接成功，接着通过PASS命令发送用户密码，若返回‘+OK’则用户验证成功。

用户验证成功后判断operation提供的选项，若选项为LIST，则发送LIST命令，并返回邮件收件箱当前的邮件序号列表与对应的大小。之后遍历得到的收件箱序号列表，对于每一个邮件序号，程序发送TOP命令获取当前邮件的邮件头，并将得到的结果通过split()函数在‘\r\n’划分后得到邮件的内容数据，并在划分后的数据中寻找From： 与Subject： 获取邮件的发件人与标题，之后根据这些数据初始化Mail对象，对于邮件主题，若主题符合MIME的标准邮件格式，则通过email.header类中的decode_header()函数对其解码，收件人则直接为用户名与邮件服务器。之后发送UIDL命令获取Pop3协议中生成的邮件uid，用于初始化Mail对象。对于生成的每一个Mail对象，程序将其存储与一个列表中，并调用store()函数存储进数据库中。

若选项为RETR，则向服务器发送RETR命令与index值，服务器返回对应的邮件报文。对于返回的邮件报文，程序首先通过get_body()函数获取邮件正文，之后查找原文获取邮件的编码（默认为utf-8），并通过decode()函数通过获取的编码方式解码，生成对应的邮件正文。程序将打开路径为C:\MailServer的目录（若不存在则新建目录）,将生成的邮件正文写入目录中，文件名为uid.txt，uid为Pop3协议生成的邮件唯一标识符。

若为DELE命令，则程序向服务器发送DELE命令与index值，服务器删除对应邮件，之后调用os.remove()函数与delete_sql()函数删除本地与数据库中邮件记录。

store()函数将生成的Mail对象列表写入数据库中，数据库打开mail关系表（若不存在则新建），通过add_sql()函数将列表中每一个邮件信息写入数据库。

#### 数据库连接

数据库连接通过pymysql类实现。通过建立游标对SQL语句进行执行操作。默认数据库为mail，存在两个关系mail与draft，mail用于存储收件信息，draft用于存储草稿信息。两个数据库有相同的属性，分别为：sender、receiver、topic、uid、listnum。分别为发件人、收件人、主题、uid与操作数。对应Mail类中的sender、receiver、topic、uid与Pop3协议中的index值。Draft关系中listnum则全部置0。

create_db()函数用于建立新的数据库mail，在程序初始化时需要运行。

create_sql()函数用于新建关系表。 

search_sql()通过receiver查询数据库中全部信息。

search_sql_by_sender()函数通过sender查询数据库中全部信息。

search_sql_by_uid()函数通过receiver与uid查询数据库中全部信息。

search_sql_by_uid_with_sender()函数通过sender与uid查询数据库中全部信息。

delete_sql()函数用于删除对应uid的元组。

add_sql()函数用于在对应数据库下增加新的元组。

drop_table()函数用于删除对应关系表。

#### 业务逻辑实现

业务逻辑使用Qt框架的信号与槽机制实现，将槽函数与UI模块对应的信号连接，实现用户对用户界面的操作。

SignInWindowUi类和MainWindowUI类分别封装登录页面和主窗口，两者分别继承的SignInWindow_Ui类和MainWindow_Ui类是由Qt Designer工具生成的定义用户界面器件的类。业务逻辑代码需在SignInWindowUi类和MaindowUi类里定义一些操作界面的函数。这些函数关联的操作与用户在界面上输入的信息无关，即对界面的操作不会因用户不同而改变。

fetch_info()函数连接到登录界面登录按钮，信号为clicked。其作用是从文本框中获取邮件服务器、用户名和密码信息。

select_server_address()函数连接登录界面的复选框，信号为activated。其作用是将复选框中的选项转换为邮件服务器的地址。

display_subpage()函数的连接主窗口listWidget模块，信号为currentRowChanged。函数实现通过点击listWidget中的选项切换主窗口的子页面。

resend_butt()函数连接到草稿箱重发送的按钮，信号为clicked。程序从数据库中获取当前访问的草稿箱邮件，并初始化Mail对象。之后调用Smtp类发送邮件。发送成功后调用数据库处理模块删除邮件记录与本地文件并打开发件成功窗口。

delete_mail()函数连接到收件箱窗口的删除按钮，信号为clicked。函数调用pop3类的DELE指令删除当前访问的邮件。删除后调用LIST指令更新邮件数据库。

MailServer类继承Smtp类和Pop3类，其主要作用是完成后端程序的初始化，同时也能使代码结构更清晰。

BussinessLogic类是业务逻辑代码的主要组成部分。其作用是实现与用户信息有关的操作。这些操作会因用户不同而不同。

show_draft()函数连接到功能listWidget模块，信号为itemClicked。函数判断是否为Drafts栏目，若为真，则访问数据库中draft关系中全部数据，并对每一条数据生成List_item对象，并通过addItem函数加入至草稿箱列表ListWidget中。若为假或数据库中无数据，则直接返回。

open_draft()函数连接到草稿箱列表listWidget模块，信号为item Clicked。函数将访问路径为C:\MailServer\Draft路径下uid.txt的数据，并将读取的数据通过setText函数写入draft窗口的文本框内。

compose_to_inbox()连接到发件成功窗口的返回inbox按钮，信号为clicked。函数调用setCurrentIndex(1)函数返回inbox子窗口。

back_to_comp()函数连接到发件成功窗口的返回compose按钮，信号为clicked。函数调用setCurrentIndex(0)函数返回comp子窗口。

click_sign_in()函数连接到comp子窗口的发送按钮，信号为clicked。函数将通过登录窗口输入的用户信息初始化MailServer对象，打开主窗口并关闭登录窗口。

click_send()函数连接到发送页面的发送按钮，信号为clicked。函数将发送页面输入的邮件信息初始化Sender_proc对象，并生成Mail对象以及向默认路径存储邮件正文。之后程序调用Smtp类对生成的邮件信息进行发送操作。发送成功后打开发送成功界面。若发送失败则退回登录界面并重新输入账号密码。

click_save()函数连接的发送界面的保存按钮，信号为clicked。函数将发送页面输入的邮件信息初始化Sender_proc对象，并生成Mail对象以及向默认路径存储邮件正文。之后调用数据库接口将邮件信息存入draft关系中。

reflesh_recv()函数连接到inbox窗口的刷新按钮，信号为clicked。函数将调用Pop3类的LIST指令刷新数据库中mail关系。之后清空原有收件ListWidget模块并将数据库mail关系中信息初始化List_item对象并加入到ListWidget中。若从服务器获取信息失败，则跳转到登录页面重新数据用户名与密码，若访问数据为空，则直接返回。

show_recv()函数连接到功能listWidget模块，信号为itemClicked。函数判断是否为Inbox栏目，若为真，则访问数据库中mail关系中全部数据，并对每一条数据生成List_item对象，并通过addItem函数加入至草稿箱列表ListWidget中。若为假或数据库中无数据，则直接返回。

show_mail()函数连接到收件箱列表listWidget模块，信号为item Clicked。函数将判断C:\MailServer路径下uid.txt文件是否存在，若存在，则直接打开uid.txt中的数据，并将读取的数据通过setText函数写入inbox窗口的文本框内。若不存在，则通过pop3类RETR指令下载对应邮件。

List_item类初始化需提供subject、sender、uid、index四个参数。Uid和index存储备用，subject与sender生成相应的QLabel，并将两个QLabel垂直对齐到QVBoxLayout类下，最后将对齐的QVBoxLayout加入生成的QWidget对象中作为邮件列表项。



<a id= "e">     </a>



#### Mail encapsulation and generation

The Mail class is set in this experiment. The uid is the value of the body md5 hash function at the time of sending and the unique identifier of the message generated in the POP3 protocol at the time of receiving. 

Mail encapsulation generated through Sender_The proc class is implemented. See Appendix 2 for the code. When initializing an email, the front-end needs to provide four pieces of information: the sender, the recipient, the subject, and the body content of the email_The mail () function generates the initial mail. gene_The mail() function generates a standard mail message from the content initialized by the class according to the standard mail message format, and generates the corresponding string according to the utf-8 code. When the email is generated at the same time, the timestamp is written in the email message, which can provide the sender's sending time and make the email content not duplicate, that is, the hash function value is not the same, so as to facilitate database management. 

gene_mailclass() function will generate the corresponding Mail object from the provided initialization value for the convenience of the sending system. Where, uid uses gene_Uid () function generation. 

gene_uid() function generates the md5 hash value of the mail message through the md5 function_The proc class will inject a timestamp, so the generated hash will not be the same when the mail information is the same. 

store() function stores the generated mail message and Mail object in the path corresponding to the disk according to certain rules. The sending path set in this program is C:  MailServer  Draft. If there is no corresponding path, this path will be generated. Storage and writing are realized through Python standard open () and close () functions. The stored file name is uidTxt, that is, the uid of the mail message is used as the local file name of the mail message to ensure that the file will not repeat. 

add_to_sql() function stores the generated Mail object in the database. Write to the database through the interface add provided by the database connection module_Sql() writes the elements in the Mail object to the Draft relational table. 

delete_draft () function provides an interface to delete the mail in the draft box from the local and database. Through osThe interface between the remove() function and the database delete_The sql() function is deleted from the local and database. 

Sender_proc class is used, the execution process is: initialization - generate mail message - generate Mail object - store - connect to the database. When sending an email, it is not necessary to connect to the database, and then call the Smtp sending class to send the generated email. 

#### SMTP client implementation

Before sending the Smtp class, you need to initialize the mail server, user name, password, mail object for sending mail, and the address for storing mail. The default address is C:  MailSever  Draft. 

When sending, call the socket library for network programming operation, and send according to the SMTP protocol. First, connect to the mail server through port 25 of SMTP through the connect() function. If the connection is successful, 2 is returned. After sending the message, wait 0.8 seconds through the sleep() function before reading the contents of the returned buffer. If the waiting time is too short, the connection cannot be made. After reading the returned information each time, judge the returned information. If it succeeds, go to the next step. If it fails, return the corresponding error code. After the link is successful, send the HELO command to the server. If 250 is returned successfully, encode the sent information with the encode() function each time you send it, and decode the received information with the decode() function when you receive it. 

Send the AUTH LOGIN command after returning 250. If 334 is returned, it is successful. Then send the user name and password to the server through base64 encoding. Before sending, send the user name and password through base64The b64encode() function encodes the sent information. 334 is returned when sending the user name, and 235 is returned after sending the password to prove that the user authentication is successful. After the verification is successful, the mail FROM command is sent in the format of MAIL FROM:+<+MAILsender+>+\r\n。If 250 is returned, the transmission is successful. Then send the RCPT TO command in the format of RCPT TO:+<+mailreceiver+>\r\n。If 250 is returned, the transmission is successful. 

After success, send the DATA command to prepare to send the mail message. If 354 is returned, it indicates that the mail server is ready to receive the mail message. The program reads the corresponding mail message through the initialized local path and sends it to the mail server, and then sends  r  n.  r  n to indicate that the body has been sent. If 250 is returned, the sending is proved to be completed, and then the QUIT command is sent to complete the mail sending. 

#### POP3 client implementation

The mail receiving class Pop3 initializes the corresponding mail server, user name, and password before receiving, and receives mail through the recvmail (operation, index) function. Operation provides LIST, RETR, and DELE instructions. RETR and DELE need to provide the index parameter for operation. LIST is to update the mailing list, RETR is to download the corresponding mail, and DELE is to delete the corresponding mail. 

The program is the same as sending an email. It establishes a connection with the server through port 110 through the connect() function. If the connection succeeds, the first three characters in the returned data are '+OK'. After the connection is established successfully, send the USER command and the user name. If the connection is successful, then send the user password through the PASS command. If "+OK" is returned, the user verification is successful. 

After successful verification, the user judges the options provided by the operation. If the option is LIST, the user sends the LIST command and returns the current mail serial number list and the corresponding size of the mail inbox. Then traverse the list of inbox serial numbers obtained. For each mail serial number, the program sends the TOP command to obtain the header of the current mail, and uses the split () function to obtain the content data of the mail after ' r  n' division, and looks for From: and Subject: in the divided data to obtain the sender and title of the mail, Then initialize the Mail object according to these data. For the mail subject, if the subject conforms to the MIME standard mail format, use emailDecode in header class_The header () function decodes it, and the recipient is the user name and mail server directly. Then send the UIDL command to obtain the mail uid generated in the Pop3 protocol, which is used to initialize the Mail object. For each Mail object generated, the program stores it in a list and calls the store() function to store it in the database. 

If the option is RETR, send the RETR command and index value to the server, and the server returns the corresponding mail message. For the returned mail message, the program first gets_The body () function obtains the mail body, and then looks up the original text to obtain the mail code (the default is utf-8), and decodes it through the encoding method obtained by the decode () function to generate the corresponding mail body. The program will open the directory with the path of C:  MailServer (if it does not exist, create a new directory), and write the generated message body into the directory. The file name is uidTxt, uid is the unique identifier of the message generated by Pop3 protocol. 

If it is a DELE command, the program sends the DELE command and index value to the server, and the server deletes the corresponding mail, and then calls remove() function and delete_The sql() function deletes the local and database mail records. 

The store() function writes the generated Mail object list to the database. The database opens the mail relational table (if it does not exist, create a new one)_The sql() function writes each mail information in the list to the database. 

#### Database Connection

The database connection is implemented through the pymysql class. Execute SQL statements by creating cursors. The default database is mail. There are two relationships: mail and draft. Mail is used to store receipt information and draft is used to store draft information. The two databases have the same attributes: sender, receiver, topic, uid, and listnum. They are sender, recipient, subject, uid and operand respectively. Corresponds to sender, receiver, topic, uid in Mail class and index value in Pop3 protocol. All listnums in the Draft relationship are set to 0. 

create_db() function is used to create a new database mail, which needs to be run when the program is initialized. 

create_sql() function is used to create a new relationship table. 

search_sql () queries all the information in the database through the receiver. 

search_sql_by_sender () function queries all the information in the database through the sender. 

search_sql_by_uid () function queries all information in the database through the receiver and uid. 

search_sql_by_uid_with_sender () function queries all information in the database through sender and uid. 

delete_sql() function is used to delete the tuple of the corresponding uid. 

add_sql() function is used to add new tuples under the corresponding database. 

drop_table () function is used to delete the corresponding table. 

#### Business logic implementation

The business logic is implemented using the signal and slot mechanism of the Qt framework. The slot function is connected to the signal corresponding to the UI module to achieve the user's operation of the user interface. 

The SignInWindowUi class and MainWindowUI class encapsulate the login page and main window respectively, and they inherit the SignInWindow respectively_Ui class and MainWindow_Ui class is a class generated by Qt Designer tool to define user interface devices. The business logic code needs to define some functions of the operation interface in the SignInWindowUi class and MaindowUi class. The operations associated with these functions are independent of the information entered by the user on the interface, that is, the operations on the interface will not change depending on the user. 

fetch_info() function is connected to the login button on the login interface, and the signal is clicked. It is used to obtain the mail server, user name and password information from the text box. 

select_server_address() function connects the check box of the login interface. The signal is activated. It is used to convert the options in the check box to the address of the mail server. 

display_subpage() function connects the listWidget module of the main window, and the signal is currentRowChanged. Function to switch sub pages of the main window by clicking options in the listWidget. 

resend_button () function is connected to the scratchpad resend button, and the signal is clicked. The program gets the currently accessed draft box mail from the database and initializes the Mail object. Then call Smtp class to send mail. After successful sending, call the database processing module to delete the mail record and local file and open the sending success window. 

delete_mail() function connects to the delete button in the inbox window, and the signal is clicked. The function calls the DELE instruction of pop3 class to delete the currently accessed mail. After deletion, the LIST command is called to update the mail database. 

The MailServer class inherits the Smtp class and Pop3 class. Its main function is to complete the initialization of the back-end program, and also to make the code structure clearer. 

BussinessLogic class is the main component of business logic code. Its function is to realize operations related to user information. These operations vary from user to user. 

show_draft () function is connected to the function listWidget module, and the signal is itemClicked. Function to determine whether it is a Draft column. If it is true, access all data in the draft relationship in the database and generate a List for each piece of data_The item object is added to the draft box list ListWidget through the addItem function. If it is false or there is no data in the database, it will be returned directly. 

open_draft () function connects to the draft box list widget module, and the signal is item Clicked. The function will access the uid under the C:  MailServer  Draft pathTxt, and write the read data into the text box of the draft window through the setText function. 

compose_to_inbox () is connected to the return inbox button in the sending success window. The signal is clicked. The function calls the setCurrentIndex (1) function to return to the inbox child window. 

back_to_comp() function is connected to the return compose button in the sending success window. The signal is clicked. The function calls the setCurrentIndex (0) function to return the comp sub window. 

click_sign_The in() function is connected to the send button of the comp sub window, and the signal is clicked. The function will initialize the MailServer object with the user information entered in the login window, open the main window, and close the login window. 

click_send () function connects to the send button of the send page, and the signal is clicked. The function initializes the Sender of the mail information input on the sending page_Proc object, and generate a Mail object and store the message body to the default path. Then the program calls the Smtp class to send the generated email information. After successful transmission, the successful transmission interface will be opened. If the sending fails, return to the login interface and re-enter the account password. 

click_save button of the sending interface connected by the save() function. The signal is clicked. The function initializes the Sender of the mail information input on the sending page_Proc object, and generate a Mail object and store the message body to the default path. Then call the database interface to store the mail information into the draft relationship. 

reflesh_recv() function is connected to the refresh button of the inbox window, and the signal is clicked. The function will call the LIST instruction of Pop3 class to refresh the mail relationship in the database. Then clear the original receiving ListWidget module and initialize the list with the information in the database mail relationship_The item object is added to the ListWidget. If it fails to obtain information from the server, it will jump to the login page to re data the user name and password. If the access data is empty, it will be returned directly. 

show_recv() function is connected to the function listWidget module, and the signal is itemClicked. Function to determine whether it is an Inbox column. If it is true, access all data in the mail relationship in the database and generate a List for each piece of data_The item object is added to the draft box list ListWidget through the addItem function. If it is false or there is no data in the database, it will be returned directly. 

show_mail() function connects to the inbox list listWidget module, and the signal is item Clicked. The function will determine the uid under the C:  MailServer pathWhether the txt file exists. If so, directly open the uidTxt, and write the read data into the text box of the inbox window through the setText function. If it does not exist, download the corresponding email through the POP3 RETR command. 

List_initialization of the item class requires four parameters: subject, sender, uid, and index. The Uid and index are stored for backup. The subject and sender generate the corresponding QLabels, vertically align the two QLabels under the QVBoxLayout class, and finally add the aligned QVBoxLayout to the generated QWidget object as a mailing list item. 