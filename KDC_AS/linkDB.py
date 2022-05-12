import pymysql

# 数据库配置信息
DB_HOST = '127.0.0.1'
DB_PORT = 3306
DB_NAME = ''
DB_USER = 'ZUO'
DB_PASS = 'zxcvbnm.123'

def link_DB():
    # 打开数据库连接
    db = pymysql.connect(host=DB_HOST,
                         user=DB_USER,
                         password=DB_PASS,
                         database=DB_NAME)

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    return cursor