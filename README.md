# EasyMail

EasyMail是一个使用Python编写的电子邮件收发客户端。此项目是武汉大学计算机网络课程的大作业。

项目主要使用SMTP和POP3协议收发邮件，使用PyQt5编写用户界面，使用MySQL管理数据库。

实现细节以及代码描述如下。

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