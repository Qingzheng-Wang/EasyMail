from socket import *
from copy import *
import os
import time
import email.header
from email.parser import Parser
import sql
import hashlib
import base64

sleeptime=0.8

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
    def __init__(self,mailserver, username, password, path=None, mail=None) -> None:
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
        if recv[0:3]!='2':
            #输出错误,print()函数仅用作测试
            print("error")
            return
        helomsf='HELO '+self.username+'\r\n'
        Socket.send(helomsf.encode())
        time.sleep(sleeptime)
        recv=Socket.recv(1024).decode()
        recvlist=recv.split('\r\n')
        if recvlist[1][0:3]!='250':
            print("error")
            return
        Socket.sendall(('AUTH LOGIN\r\n').encode())
        time.sleep(sleeptime)
        recv=Socket.recv(1024).decode()
        if recv[0:3]!='334':
            print("error")
            return
        Socket.sendall((str(base64.b64encode((self.username+'@'+self.mailserver).encode()),'utf-8')+'\r\n').encode())
        time.sleep(sleeptime)
        recv=Socket.recv(1024).decode()
        if recv[0:3]!='334':
            print("error")
            return
        Socket.sendall((str(base64.b64encode(self.password.encode()),'utf-8')+'\r\n').encode())
        time.sleep(sleeptime)
        recv=Socket.recv(1024).decode()
        if recv[0:3]!='235':
            print("error")
            return
        Socket.sendall(('MAIL FROM: '+'<'+self.mail.sender+'>\r\n').encode())
        time.sleep(sleeptime)
        recv=Socket.recv(1024).decode()
        if recv[0:3]!='250':
            print("error")
            return
        Socket.sendall(('RCPT TO: '+'<'+self.mail.receiver+'>\r\n').encode())
        time.sleep(sleeptime)
        recv=Socket.recv(1024).decode()
        if recv[0:3]!='250':
            print("error")
            return
        Socket.sendall(('DATA\r\n').encode())
        time.sleep(sleeptime)
        recv=Socket.recv(1024).decode()
        if recv[0:3]!='354':
            print("error")
            return

        Socket.sendall(message.encode())
        Socket.sendall('\r\n.\r\n'.encode())
        time.sleep(sleeptime)
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
        dbtuple=sql.SQL.show_tables()
        dblist=''
        for i in dbtuple:
            dblist+=i[0]
        if(dblist.find('mail')==-1):
            sql.SQL.create_sql('Mail')
        else:
            sql.SQL.drop_table('Mail')
            sql.SQL.create_sql('Mail')
        cnt=1
        for i in maillist:
            sql.SQL().add_sql(i.sender,i.receiver,i.topic,i.uid,cnt,'Mail')
            cnt+=1
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
        time.sleep(sleeptime)
        recv=Socket.recv(1024).decode()
        if recv[0:3]!='+OK':
            print("error")
            return 
        Socket.sendall(('USER '+self.username+'\r\n').encode())
        time.sleep(sleeptime)
        recv=Socket.recv(1024).decode()
        if recv[0:3]!='+OK':
            print("error")
            return 
        Socket.sendall(('PASS '+self.password+'\r\n').encode())
        time.sleep(sleeptime)
        recv=Socket.recv(1024).decode()
        if recv[0:3]!='+OK':
            print("error")
            return 

        if operation=='STAT':
            Socket.send('STAT\r\n'.encode())
            time.sleep(sleeptime)
            recv=Socket.recv(1024).decode()
            print(recv) #仅作测试用
        elif operation=='LIST':
            Socket.send('LIST\r\n'.encode())
            time.sleep(sleeptime)
            recv=Socket.recv(65536).decode()
            if recv[0:3]!='+OK':
                print("error")
                return 
            recvlist=recv.split('\r\n')
            maillist=[]
            for per in range(1,len(recvlist[1:len(recvlist)-2])+1):
                Socket.sendall(('TOP '+str(per)+' 5\r\n').encode())
                time.sleep(sleeptime)
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
                time.sleep(sleeptime)
                uid=Socket.recv(1024).decode()
                uidlist=uid.split(' ')
                mail.uid=uidlist[2][0:len(uidlist[2])-2]
                maillist.append(mail)
            self.store(maillist)
            ##此处需连接数据库##
        elif operation=='RETR':
            Socket.sendall(('UIDL '+str(index)+'\r\n').encode())
            time.sleep(sleeptime)
            uid=Socket.recv(1024).decode()
            uidlist=uid.split(' ')
            Socket.sendall(('RETR '+str(index)+'\r\n').encode())
            time.sleep(sleeptime)
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
            time.sleep(sleeptime)
            uid=Socket.recv(1024).decode()
            uidlist=uid.split(' ')
            Socket.sendall(('DELE '+str(index)+'\r\n').encode())
            os.remove(path+'\\'+uidlist[2][0:len(uidlist[2])-2]+'.txt')
            sql.SQL.delete_sql(uidlist[2][0:len(uidlist[2])-2],'Mail')
            sql.SQL.update_after_dele(index)
        Socket.send('QUIT'.encode())
        Socket.close()
        return 

class Sender_proc:
    def __init__(self,sender,receiver,subject,message) -> None:  #init时创建邮件报文
        self.sender=sender
        self.receiver=receiver
        self.message=message
        self.subject=subject
        self.msg=self.gene_mail()  #此时确定时间戳
    
    def gene_uid(self):
        return hashlib.md5(self.msg.encode('utf-8')).hexdigest()

    def gene_mail(self):
        msg="From: "+self.sender+'\n' \
            +"To: "+self.receiver+'\n' \
            +"Subject: "+self.subject+'\n' \
            +"Date: "+time.asctime()+"\n"\
            +"Content-Type: text/plain; charset=UTF-8 \n"\
            +'\r\n'\
            +self.message.encode('utf-8').decode('utf-8')+'\r\n'
        return msg

    def gene_mailclass(self):
        mail=Mail()
        mail.receiver=self.receiver
        mail.sender=self.sender
        mail.topic=self.subject
        mail.uid=self.gene_uid()
        return mail

    def store(self):
        mail=self.gene_mailclass()
        path='C:\\MailServer\\Draft'
        while not os.path.exists(path):
            os.makedirs(path)
        f=open(path+'\\'+mail.uid+'.txt',mode='w')
        f.write(self.msg)
        f.close()
        return path+'\\'+mail.uid+'.txt'

    def add_to_sql(self):
        dbtuple=sql.SQL.show_tables()
        dblist=''
        for i in dbtuple:
            dblist+=i[0]
        if(dblist.find('draft')==-1):
            sql.SQL.create_sql('Draft')
        sql.SQL.add_sql(self.sender,self.receiver,self.subject,self.gene_uid(),0,'Draft')




