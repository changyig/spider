import time
import pymysql
class Mysql:
    def __init__(self):
        self.connect = False
        self.connect = pymysql.connect(
            host="127.0.0.1",
            db="scrapy",
            user="root",
            passwd="root",
            charset='utf8',
            use_unicode=True
        )
        self.sql=None
        self.where=''
        self.limit=''
        self.table=''
        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()
    #操作的表名字
    def table(self,table=''):
        try:
            if table:
                self.table="select * from {}".format(table)
        except Exception as e:
            print(e)
        return self
    #解析操作 = like in 等有待完善
    def pare(self,op=[]):
        try:
            if op:
                if op[0]=='=':
                    pass
                if op[0]=='like':
                    op[1]= "'%"+str(op[1])+"%'"
        except Exception as e:
            print(e)
        return op
    #查询的条件 格式[{'title':['=',1]},{'name':['like','chang']}] 字段字典形式 条件列表形式
    def where(self,lists=[]):
        try:
            if lists:
                where_list=[]
                for list in lists:
                    str1 = ' '
                    (field,value), = list.items()
                    value = self.pare(value)
                    str1 =' '+ field + ' ' + str(value[0]) + ' ' + str(value[1])
                    where_list.append(str1)
                str1=' and '.join(where_list)
                self.sql=self.sql+' where '+str1
        except Exception as e:
            print(e)
        return self
    #获取其中一条记录
    def get_one(self, sql='', params=()):
        result = None
        if sql=='':
            sql=self.sql
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
        except Exception as e:
            print(e)
        return result
    #获取所有的记录
    def get_all(self,sql,params=()):
        list_data = ()
        try:
            self.connect()
            self.cursor.execute(sql,params)
            list_data = self.cursor.fetchall()
        except Exception as e:
            print(e)
        return list_data

    #获取指定的数目
    def limit(self,param=10):
        list_data = ()
        try:
            self.sql = self.sql + ' limit ' + str(param)
            self.cursor.execute(self.sql)
            list_data = self.cursor.fetchall()
        except Exception as e:
            print(e)
        return list_data

    #获取指定的数目
    def update(self,lists=[]):
        try:
            if lists:
                where_list = []
                for list in lists:
                    str1 = ' '
                    (field,value), = list.items()
                    value = self.pare(value)
                    str1 = ' ' + field + ' ' + str(value[0]) + ' ' + str(value[1])
                    where_list.append(str1)
                str1 = ' and '.join(where_list)
                self.sql = self.sql + ' where ' + str1
        except Exception as e:
            print(e)
        return self

if __name__=="__main__":
    mysql=Mysql()
    where_data=[{'id':['>',1]},{'id':['=',2]}]
    res=mysql.table('zhidao_relation').where(where_data).limit(10)
    print(res)