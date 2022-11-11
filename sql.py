
import pymysql
class SQL:  #数据存储类
    mailserver = ''
    username = ''
    password = ''

    def __init__(self,mailserver,username,password) -> None:
        self.mailserver=mailserver
        self.username=username
        self.password=password

    #连接到数据库
    def get_conn(self):
      return pymysql.connect(
      mailsever='mailserver',
      username='username',
      password='password',
    )




    # 查询数据库
    def query_data(sql):
        # 创建一个游标
        coon=get_coon()
        cursor = coon.cursor
    cursor.execute(sql)
    #获取单条数据
    print(cursor.fetchone())
    #获取多条数据
    all =cursor.fetchall()
    for i in all:
        print(i[0])
        #关闭链接
        coon.close()


     #插入数据库
    def insert_data(sql):
       # 创建一个游标
      coon=get_coon()
      cursor = coon.cursor
    insert_sql='''
    insert into email values('mailsever','username','password')
    '''
    cursor.execute(insert_sql)
    coon.commit()
    #关闭链接
    coon.close()



   #删除操作
    def delete_data(sql):
    # 创建一个游标
      coon=get_coon()
      cursor = coon.cursor
    del_sql='''
    del email values('mailsever','username','password')
    '''
    cursor.execute(del_sql)
    coon.commit()
    #关闭链接
    coon.close()
    rerurn





