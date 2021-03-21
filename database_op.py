
# connect_orm.py
from sqlalchemy import create_engine, Column, String
import pymysql
from sqlalchemy.orm import declarative_base




# 创建基类
BASE = declarative_base()

# 定义学生对象
class Student(BASE):
    # 表的名字:STUDENT
    __tablename__ = 'STUDENT'
    id = Column(String(32))
    # 学号
    sno = Column(String(10))
    # 姓名
    sname = Column(String(20), primary_key=True)
    # 创建表的参数
    __table_args__ = {
        "mysql_charset": "utf8"
    }

if __name__ == '__main__':
    print('---- 数据库连接 ---')

    try:
        # 连接MySQL数据库，地址：localhost:3306,账号：root,密码：123,数据库：test
        MySQLEngine = create_engine('mysql+pymysql://root:admin@192.168.232.130:3306/test?charset=utf8', encoding='utf-8')
        print('连接MySQL数据库成功', MySQLEngine)
        print('table_names:', MySQLEngine.table_names)
        # # 连接SQLite数据库，如果当前目录不存在test.db文件则会自动生成
        # SQLiteEngine = create_engine('sqlite:///:test.db', encoding='utf-8')
        # print('连接SQLite数据库成功', SQLiteEngine)

        # 创建STUDENT表
        BASE.metadata.create_all(MySQLEngine)
        print('创建STUDENT表成功')

    except Exception as e:
        print('连接数据库失败', e)

