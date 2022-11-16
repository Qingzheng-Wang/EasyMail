from socket import *
from copy import *
import os
import time
import email.header
from email.parser import Parser
import sql

class Mail:
    sender=''  #发件人地址
    receiver=''  #收件人地址
    topic=''  #标题
    uid=''  #文件uid

class Smtp: #邮件发送类
    mailserver=''  #邮件服务器
    username=''   #用户名
    password=''     #密码
    path=''
    mail=Mail()
    def __init__(self,mail,mailserver,username,password,path) -> None:
        self.mail=deepcopy(mail)
        self.mailserver=mailserver
        self.username=username
        self.password=password
        self.path=path
    def sendmail(self):
        f=open(self.path+'\\'+self.mail.uid+'.txt')
        message=f.read()
        Socket=socket(AF_INET,SOCK_STREAM)
        Socket.connect((self.mailserver,25))
        recv=Socket.recv(1024).decode()
        if recv[0:3]!='220':
            #输出错误,print()函数仅用作测试
            print("error")
            return
        helomsf='HELO '+self.username+'\r\n'
        Socket.send(helomsf.encode())
        time.sleep(1)
        recv=Socket.recv(1024).decode()
        if recv[0:3]!='250':
            print("error")
            return
        Socket.sendall('AUTH LOGIN\r\n')
        time.sleep(1)
        recv=Socket.recv(1024).decode()
        if recv[0:3]!='334':
            print("error")
            return
        Socket.sendall((self.username+'\r\n').encode())
        time.sleep(1)
        recv=Socket.recv(1024).decode()
        if recv[0:3]!='334':
            print("error")
            return
        Socket.sendall((self.password+'\r\n').encode)
        time.sleep(1)
        recv=Socket.recv(1024).decode()
        if recv[0:3]!='334':
            print("error")
            return
        Socket.sendall(('MAIL FROM: '+'<'+self.mail.sender+'>\r\n').encode())
        time.sleep(1)
        recv=Socket.recv(1024).decode()
        if recv[0:3]!='250':
            print("error")
            return
        Socket.sendall(('RCPT TO: '+'<'+self.mail.receiver+'>\r\n').encode())
        time.sleep(1)
        recv=Socket.recv(1024).decode()
        if recv[0:3]!='250':
            print("error")
            return
        Socket.sendall(('DATA\r\n').encode())
        time.sleep(1)
        recv=Socket.recv(1024).decode()
        if recv[0:3]!='354':
            print("error")
            return

        Socket.sendall(message.encode())
        Socket.sendall('\r\n.\r\n'.encode())
        time.sleep(1)
        recv=Socket.recv(1024).decode()
        if recv[0:3]!='250':
            print("error")

        Socket.send('QUIT\r\n'.encode())
        Socket.close()
        f.close()

class Pop3:  #邮件接收类
    mailserver=''
    username=''
    password=''
    def __init__(self,mailserver,username,password) -> None:
        self.mailserver=mailserver
        self.username=username
        self.password=password

    def store(self,maillist):
        sql.SQL.drop_table()
        sql.SQL.create_sql('Mail')
        for i in maillist:
            sql.SQL().add_sql(i.sender,i.receiver,i.topic,i.uid)
        return
    def get_body(self,msg):
        if msg.is_multipart():
            return self.get_body(msg.get_payload(0))
        else:
            return msg.get_payload(None,decode=True)
    
    def recvmail(self,operation,index):
        
        path='C:\\MailServer'  #默认路径
        while not os.path.exists(path):
            os.makedirs(path)
        Socket=socket(AF_INET,SOCK_STREAM)
        Socket.connect((self.mailserver,110))
        time.sleep(1)
        recv=Socket.recv(1024).decode()
        if recv[0:3]!='+OK':
            print("error")
            return 
        Socket.sendall(('USER '+self.username+'\r\n').encode())
        time.sleep(1)
        recv=Socket.recv(1024).decode()
        if recv[0:3]!='+OK':
            print("error")
            return 
        Socket.sendall(('PASS '+self.password+'\r\n').encode())
        time.sleep(1)
        recv=Socket.recv(1024).decode()
        if recv[0:3]!='+OK':
            print("error")
            return 

        if operation=='STAT':
            Socket.send('STAT\r\n'.encode())
            time.sleep(1)
            recv=Socket.recv(1024).decode()
            print(recv) #仅作测试用
        elif operation=='LIST':
            Socket.send('LIST\r\n'.encode())
            time.sleep(1)
            recv=Socket.recv(65536).decode()
            if recv[0:3]!='+OK':
                print("error")
                return 
            recvlist=recv.split('\r\n')
            maillist=[]
            for per in range(1,len(recvlist[1:len(recvlist)-2])+1):
                Socket.sendall(('TOP '+str(per)+' 5\r\n').encode())
                time.sleep(1)
                recv=Socket.recv(65536).decode()
                toplist=recv.split('\r\n')
                mail=Mail()
                mail.receiver=self.username+'@'+self.mailserver
                findex=0
                starti=0
                dflag=False
                for i in range(len(toplist)):
                    if(toplist[i].find('From: ') != -1):
                        findex=i
                        break
                mail.sender=toplist[findex][5:]
                for i in range(len(toplist)):
                    if(toplist[i].find('Subject: ') != -1):
                        findex=i
                        starti=toplist[i].find('=?')
                        if(starti!=-1):
                            dflag=True
                        break
                if(dflag):
                    stmp,fcode=email.header.decode_header(toplist[findex][starti:])[0]
                    mail.topic=stmp.decode(fcode)
                else:
                    mail.topic=toplist[findex][8:]
                Socket.send(('UIDL '+str(per)+'\r\n').encode())
                time.sleep(1)
                uid=Socket.recv(1024).decode()
                uidlist=uid.split(' ')
                mail.uid=uidlist[2][0:len(uidlist[2])-2]
                maillist.append(mail)
            self.store(maillist)
            print(recv)
            ##此处需连接数据库##
        elif operation=='RETR':
            Socket.sendall(('UIDL '+str(index)+'\r\n').encode())
            time.sleep(1)
            uid=Socket.recv(1024).decode()
            uidlist=uid.split(' ')
            Socket.sendall(('RETR '+str(index)+'\r\n').encode())
            time.sleep(1)
            recv=Socket.recv(65536).decode()
            if(recv[0:3]!='+OK'):
                print("error")
                return 
            recvlist=recv.split('\n',1)
            msg=Parser().parsestr(recvlist[1])
            charset=msg.get_charset()
            if charset is None:
                if(recv.find('UTF-8')!=-1 or recv.find('utf-8')!=-1):
                    charset='utf-8'
                elif(recv.find('GBK')!=-1):
                    charset='gbk'
                else:
                    charset='utf-8'
            body=self.get_body(msg).decode(charset)
            f=open(path+'\\'+uidlist[2][0:len(uidlist[2])-2]+'.txt',mode='w')
            #recvlist=recv.split('\n',1)
            f.write(body)
            f.close()
        elif operation == 'DELE':
            Socket.sendall(('UIDL '+str(index)+'\r\n').encode())
            time.sleep(1)
            uid=Socket.recv(1024).decode()
            uidlist=uid.split(' ')
            Socket.sendall(('DELE '+str(index)+'\r\n').encode())
            sql.SQL.delete_sql(uidlist[2][0:len(uidlist)-2])
        Socket.send('QUIT'.encode())
        Socket.close()
        return 


