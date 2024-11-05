import sqlite3

# 创建数据库并初始化两个表
db_file = 'lecture_monitor.db'

conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# 创建订阅者表
cursor.execute('''
    CREATE TABLE IF NOT EXISTS subscribers (
        email TEXT PRIMARY KEY
    )
''')

# 创建已发送的讲座表
cursor.execute('''
    CREATE TABLE IF NOT EXISTS sent_lectures (
        title TEXT,
        date TEXT,
        PRIMARY KEY (title, date)
    )
''')

conn.commit()
conn.close()
