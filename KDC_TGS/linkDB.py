import pymysql

# 数据库配置信息
DB_HOST = '127.0.0.1'
DB_PORT = 3306
DB_NAME = 'kerberoslibrary'
DB_USER = 'root'
DB_PASS = 'zxcvbnm.123'


class link_DB:
    # 打开数据库连接
    def __init__(self):
        self.conn = pymysql.connect(host=DB_HOST,
                                    port=DB_PORT,
                                    user=DB_USER,
                                    password=DB_PASS,
                                    database=DB_NAME)

        # 使用 cursor() 方法创建一个游标对象 cursor
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def getClientEk(self, id):
        sql = '''
        SELECT
            *
        FROM
            tgs_use
        WHERE
            ID=%s
        '''
        self.cursor.execute(sql, id)
        res = self.cursor.fetchall()
        return res[0][1]

    def getClientPk(self, id):
        sql = '''
        SELECT
            *
        FROM
            tgs_use
        WHERE
            ID=%s
        '''
        self.cursor.execute(sql, id)
        res = self.cursor.fetchall()
        return res[0][2]
