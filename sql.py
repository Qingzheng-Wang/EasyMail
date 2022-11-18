import pymysql

class SQL:  # 数据存储类

    @staticmethod
    def create_db():
        try:
            conn = pymysql.connect(host='localhost',user='root',password='4268',database='mail')
        except Exception as e:
            print(f'数据库连接失败：{e}')
        cursor = conn.cursor()
        sql_init = "CREATE DATABASE IF NOT EXISTS mail"
        cursor.execute(sql_init)
        cursor.close()
        conn.close()

    @staticmethod
    def show_tables():
        try:
            conn = pymysql.connect(host='localhost',user='root',password='4268',database='mail')
        except Exception as e:
            print(f'数据库连接失败：{e}')
        cursor = conn.cursor()
        sql_init = "show tables from mail" 
        cursor.execute(sql_init)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results

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
    def search_sql(receiver,name):
        try:
            conn = pymysql.connect(host='localhost',user='root',password='4268',database='mail')
        except Exception as e:
            print(f'数据库连接失败：{e}')
        cursor = conn.cursor()
        sql_search = "select * from %s WHERE receiver = '%s' " \
                     % (name,receiver)
        cursor.execute(sql_search)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        if not results:
            return
        return results

    @staticmethod
    def delete_sql(uid,name):
        try:
            conn = pymysql.connect(host='localhost',user='root',password='4268',database='mail')
        except Exception as e:
            print(f'数据库连接失败：{e}')
        cursor = conn.cursor()
        sql_delete = "DELETE FROM %s WHERE uid = '%s'" % (name,uid)
        cursor.execute(sql_delete)
        cursor.close()
        conn.close()

    @staticmethod
    def add_sql(sender, receiver, topic,uid,num,name):
        try:
            conn = pymysql.connect(host='localhost',user='root',password='4268',database='mail')
        except Exception as e:
            print(f'数据库连接失败：{e}')
        cursor = conn.cursor()
        sql_add = "INSERT INTO %s VALUES ('%s','%s','%s','%s',%s)" % (name,sender, receiver, topic, uid,num)
        cursor.execute(sql_add)
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def drop_table(name):
        try:
            conn = pymysql.connect(host='localhost',user='root',password='4268',database='mail')
        except Exception as e:
            print(f'数据库连接失败：{e}')
        cursor = conn.cursor()
        sql_add = "DROP TABLE %s" % (name)
        cursor.execute(sql_add)
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def update_after_dele(index):
        try:
            conn = pymysql.connect(host='localhost',user='root',password='4268',database='mail')
        except Exception as e:
            print(f'数据库连接失败：{e}')
        cursor = conn.cursor()
        sql_add = "UPDATE Mail SET listnum=listnum-1 WHERE uid IN \
                    (SELECT M1.uid FROM \
                    (SELECT M.uid FROM Mail AS M WHERE M.listnum>%d)\
                    AS M1);" % (index)
        cursor.execute(sql_add)
        conn.commit()
        cursor.close()
        conn.close()