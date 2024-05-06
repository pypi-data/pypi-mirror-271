import pymysql


class Mysql:
    '''
    数据库类
     :参数 db=选择数据库，默认为Week_event，data_dict返回数据是否需要dict形式，默认为false
     :每一种方法只需sql语句参数即可使用
     :insert,updata,delete方法没区别，便于使用时review
     :empty为清空表并排序自动递增
     :暂未写入关闭连接，因为不知道原理以及相关性能影响，待学习
    '''

    def __init__(self, host="152.136.113.50", db='personal', port=3306, user='neely', passwd='Neely2018',  data_dict=False):

        self.my_con = pymysql.connect(
            host=host, port=port, user=user, passwd=passwd, db=db, connect_timeout=1000)

        if data_dict:
            self.my_cousor = self.my_con.cursor(
                cursor=pymysql.cursors.DictCursor)
        else:
            self.my_cousor = self.my_con.cursor()

    def get_one(self, sql):
        ''' 获取一条数据 '''

        self.my_cousor.execute(sql)

        data = self.my_cousor.fetchone()

        # self.my_cousor.close()
        # self.my_con.close()

        return data

    def get_all(self, sql, singleColum=False):
        ''' 获取多条数据
            formed="single"
        '''
        self.my_cousor.execute(sql)

        data = self.my_cousor.fetchall()

        if singleColum:
            return [i[0] for i in data]

        return data

    def insert(self, sql):
        ''' 插入数据 '''
        msg = self.my_cousor.execute(sql)

        self.my_con.commit()

        return msg

    def insert_many(self, sql, param):
        ''' 插入多条数据 '''
        msg = self.my_cousor.executemany(sql, param)

        self.my_con.commit()

        return msg

    def update(self, sql):
        ''' 更新数据 '''
        msg = self.my_cousor.execute(sql)

        self.my_con.commit()

        return msg

    def delete(self, sql):
        ''' 删除数据 '''
        msg = self.my_cousor.execute(sql)

        self.my_con.commit()

        return msg

    def empty(self, db):
        '''
        直接清空表并排序key

        用于重新写入全部数据
        '''

        sql = (f'DELETE from {db}')
        sql2 = (f'alter table {db} AUTO_INCREMENT 1')

        msg = self.my_cousor.execute(sql)
        self.my_cousor.execute(sql2)
        self.my_con.commit()

        print(f'已删除{msg}条数据，清空{db}表')
