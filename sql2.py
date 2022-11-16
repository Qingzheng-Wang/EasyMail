
class SQL:  # 数据存储类
    @staticmethod
    def create_sql(self):
        try:
            conn = pymysql.connect(sender='sender', receiver='receiver', topic='topic', uid='store_addr', charset='utf8')
        except Exception as e:
            print(f'数据库连接失败：{e}')
        cursor = conn.cursor()
        sql_init = 'create table  %s (sender char(20), receiver char(20), topic char(30), uid char(50) ' \
                   'PRIMARY KEY(uid))' % (GroupII,)
        cursor.execute(sql_init)
        cursor.close()
        conn.close()

    @staticmethod
    def search_sql(sender, receiver, topic):
        try:
            conn = pymysql.connect(sender='sender', receiver='receiver', topic='topic', uid='store_addr', charset='utf8')
        except Exception as e:
            print(f'数据库连接失败：{e}')
        cursor = conn.cursor()
        sql_search = 'select * from GroupII WHERE sender = %s AND receiver = %s AND topic = %s AND uid = %s' \
                     % (sender, receiver, topic, uid)
        cursor.execute(sql_search)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        if not results:
            return
        return results

    @staticmethod
    def delete_sql(sender, receiver, topic):
        try:
            conn = pymysql.connect(sender='sender', receiver='receiver', topic='topic', uid='store_addr', charset='utf8')
        except Exception as e:
            print(f'数据库连接失败：{e}')
        cursor = conn.cursor()
        sql_delete = 'DELETE FROM user WHERE sender = %s AND receiver = %s AND topic = %s AND uid = %s' % (sender, receiver, topic, uid)
        cursor.execute(sql_delete)
        cursor.close()
        conn.close()

    @staticmethod
    def add_sql(sender, receiver, topic, store_addr):
        try:
            conn = pymysql.connect(sender='sender', receiver='receiver', topic='topic', uid='store_addr', charset='utf8')
        except Exception as e:
            print(f'数据库连接失败：{e}')
        cursor = conn.cursor()
        sql_add = 'INSERT INTO GroupII VALUES (%s,%s,%s,%s)' % (sender, receiver, topic, uid)
        cursor.execute(sql_add)
        conn.commit()
        cursor.close()
        conn.close()
