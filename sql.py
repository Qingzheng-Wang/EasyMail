import pymysql

class SQL:  # 数据存储类
    @staticmethod
    def create_sql(name):
        try:
            conn = pymysql.connect(host='localhost',user='root',password='4268',database='mail')
        except Exception as e:
            print(f'数据库连接失败：{e}')
        cursor = conn.cursor()
        sql_init = "create table  %s (sender char(80), receiver char(50), topic char(50), uid char(50),listnum INT,  \
                   PRIMARY KEY(uid))" % (name)
        cursor.execute(sql_init)
        cursor.close()
        conn.close()

    @staticmethod
    def search_sql(sender, receiver, topic,uid,listnum):
        try:
            conn = pymysql.connect(host='localhost',user='root',password='4268',database='mail')
        except Exception as e:
            print(f'数据库连接失败：{e}')
        cursor = conn.cursor()
        sql_search = "select * from GroupII WHERE sender = '%s' AND receiver = '%s' AND topic = '%s' AND uid = '%s' AND listnum=%s" \
                     % (sender, receiver, topic, uid,listnum)
        cursor.execute(sql_search)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        if not results:
            return
        return results

    @staticmethod
    def delete_sql(uid):
        try:
            conn = pymysql.connect(host='localhost',user='root',password='4268',database='mail')
        except Exception as e:
            print(f'数据库连接失败：{e}')
        cursor = conn.cursor()
        sql_delete = "DELETE FROM user WHERE uid = '%s'" % (uid)
        cursor.execute(sql_delete)
        cursor.close()
        conn.close()

    @staticmethod
    def add_sql(sender, receiver, topic,uid,num):
        try:
            conn = pymysql.connect(host='localhost',user='root',password='4268',database='mail')
        except Exception as e:
            print(f'数据库连接失败：{e}')
        cursor = conn.cursor()
        sql_add = "INSERT INTO Mail VALUES ('%s','%s','%s','%s',%s)" % (sender, receiver, topic, uid,num)
        cursor.execute(sql_add)
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def drop_table():
        try:
            conn = pymysql.connect(host='localhost',user='root',password='4268',database='mail')
        except Exception as e:
            print(f'数据库连接失败：{e}')
        cursor = conn.cursor()
        sql_add = "DROP TABLE Mail"
        cursor.execute(sql_add)
        conn.commit()
        cursor.close()
        conn.close()
