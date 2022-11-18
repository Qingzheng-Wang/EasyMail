# SMTPClient.py
from socket import *

msg = "\r\n I love computer networks!"
endMsg = "\r\n.\r\n"
# 选择一个邮件服务
mailServer = "smtp.qq.com"
# 发送方地址和接收方地址，from 和 to
fromAddress = "wangqingzheng123@qq.com"
toAddress = "qingzhengwangchina@gmail.com   "
# 发送方，验证信息，由于邮箱输入信息会使用base64编码，因此需要进行编码
username = "d2FuZ3Fpbmd6aGVuZzEyMw=="  # 输入自己的用户名对应的编码
password = "Z3hya3RveWNwbmdjYmVlZQ=="  # 此处不是自己的密码，而是开启SMTP服务时对应的授权码

# 创建客户端套接字并建立连接
serverPort = 25  # SMTP使用25号端口
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailServer, serverPort))  # connect只能接收一个参数
# 从客户套接字中接收信息
recv = clientSocket.recv(1024).decode()
print(recv)
if '220' != recv[:3]:
    print('220 reply not received from server.')

# 发送 HELO 命令并且打印服务端回复
# 开始与服务器的交互，服务器将返回状态码250,说明请求动作正确完成
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode())  # 随时注意对信息编码和解码
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if '250' != recv1[:3]:
    print('250 reply not received from server.')

# 发送"AUTH LOGIN"命令，验证身份.服务器将返回状态码334（服务器等待用户输入验证信息）
clientSocket.sendall('AUTH LOGIN\r\n'.encode())
recv2 = clientSocket.recv(1024).decode()
print(recv2)
if '334' != recv2[:3]:
    print('334 reply not received from server.')

# 发送验证信息
clientSocket.sendall((username + '\r\n').encode())
recvName = clientSocket.recv(1024).decode()
print(recvName)
if '334' != recvName[:3]:
    print('334 reply not received from server')

clientSocket.sendall((password + '\r\n').encode())
recvPass = clientSocket.recv(1024).decode()
print(recvPass)
# 如果用户验证成功，服务器将返回状态码235
if '235' != recvPass[:3]:
    print('235 reply not received from server')

# TCP连接建立好之后，通过用户验证就可以开始发送邮件。邮件的传送从MAIL命令开始，MAIL命令后面附上发件人的地址。
# 发送 MAIL FROM 命令，并包含发件人邮箱地址
clientSocket.sendall(('MAIL FROM: <' + fromAddress + '>\r\n').encode())
recvFrom = clientSocket.recv(1024).decode()
print(recvFrom)
if '250' != recvFrom[:3]:
    print('250 reply not received from server')

# 接着SMTP客户端发送一个或多个RCPT (收件人recipient的缩写)命令，格式为RCPT TO: <收件人地址>。
# 发送 RCPT TO 命令，并包含收件人邮箱地址，返回状态码 250
clientSocket.sendall(('RCPT TO: <' + toAddress + '>\r\n').encode())
recvTo = clientSocket.recv(1024).decode()  # 注意UDP使用sendto，recvfrom
print(recvTo)
if '250' != recvTo[:3]:
    print('250 reply not received from server')

# 发送 DATA 命令，表示即将发送邮件内容。服务器将返回状态码354（开始邮件输入，以"."结束）
clientSocket.send('DATA\r\n'.encode())
recvData = clientSocket.recv(1024).decode()
print(recvData)
if '354' != recvData[:3]:
    print('354 reply not received from server')

# 编辑邮件信息，发送数据
subject = "I love computer networks!"
contentType = "text/plain"

message = 'from:' + fromAddress + '\r\n'
message += 'to:' + toAddress + '\r\n'
message += 'subject:' + subject + '\r\n'
message += 'Content-Type:' + contentType + '\t\n'
message += '\r\n' + msg
clientSocket.sendall(message.encode())

# 以"."结束。请求成功返回 250
clientSocket.sendall(endMsg.encode())
recvEnd = clientSocket.recv(1024).decode()
print(recvEnd)
if '250' != recvEnd[:3]:
    print('250 reply not received from server')

# 发送"QUIT"命令，断开和邮件服务器的连接
clientSocket.sendall('QUIT\r\n'.encode())

clientSocket.close()

