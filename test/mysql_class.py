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
        self.sqltable = ''
        self.sqlfields = '*'
        self.sqlwhere=''
        self.sqlorder=''
        self.sqllimit = ''
        self.sqlupdatefields = ''
        self.sqlinsert = ''
        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()
    #操作的表名字
    def table(self,table=''):
        self.sqltable = ''
        self.sqlfields = '*'
        self.sqlwhere = ''
        self.sqlorder = ''
        self.sqllimit = ''
        self.sqlupdatefields = ''
        self.sqlinsert = ''
        try:
            if table:
                self.sqltable=table
        except Exception as e:
            print(e)
        return self
    #解析操作 = like in 等有待完善
    def pare(self,op=[]):
        try:
            if op:
                if op[0]=='=':
                    pass
                elif op[0]=='like':
                    op[1]= "%"+str(op[1])+"%"
                elif op[0]=='not like':
                    op[1]= "%"+str(op[1])+"%"
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
                    if isinstance(value[1],int):
                        value[1] = str(value[1])
                    elif isinstance(value[1],str):
                        value[1] = '"'+str(value[1])+ '"'
                    str1 =' '+ field + ' ' + str(value[0]) + ' ' + value[1]
                    where_list.append(str1)
                str1=' and '.join(where_list)
                if self.sqlwhere=='':
                    self.sqlwhere=self.sqlwhere+' where '+str1
                else:
                    self.sqlwhere=self.sqlwhere+' and  '+str1
        except Exception as e:
            print(e)
        return self

    #获取数据表中的字段 注意里面必须是字符串不能是其他类型的数据
    def field(self,fields='*'):
        try:
            if fields != '*':
                self.sqlfields=','.join(fields)
        except Exception as e:
            print(e)
        return self
    #获取其中一条记录
    def find(self, sql='', params=()):
        result = None
        if sql=='':
            sql=self.makesql()
        try:
            # print(sql)
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
        except Exception as e:
            print(e)
        return result
    #获取所有的记录
    def select(self,sql='',params=()):
        list_data = ()
        try:
            if sql=='':
                sql=self.makesql()
            # print(sql)
            self.cursor.execute(sql)
            list_data = self.cursor.fetchall()
        except Exception as e:
            # print('出错了')
            print(e)
        return list_data

    #获取所有的记录
    def count(self,sql='',params=()):
        list_data = ()
        try:
            if sql == '':
                sql = self.makesql('count')
            # print(sql)
            self.cursor.execute(sql)
            list_data = self.cursor.fetchone()
        except Exception as e:
            # print('出错了')
            print(e)
        return list_data

    #获取指定的数目
    def limit(self,param=10):
        try:
            if param>0:
                self.sqllimit = ' limit ' + str(param)
            else:
                self.sqllimit = ' limit ' + str(10)
        except Exception as e:
            print(e)
        return self

    #组装sql语句
    def makesql(self,type='select'):
        try:
            if type=='select':
                self.sql='select '+self.sqlfields+' from '+self.sqltable+self.sqlwhere+self.sqlorder+self.sqllimit
            elif type=='update':
                self.sql = 'update ' + self.sqltable + self.sqlupdatefields + self.sqlwhere + self.sqlorder + self.sqllimit
            elif type=='insert':
                self.sql = 'insert into ' + self.sqltable + self.sqlinsert
            elif type=='count':
                self.sql = 'select count(*) as num from ' + self.sqltable + self.sqlwhere + self.sqlorder + self.sqllimit
            # print(self.sql)
            return self.sql
        except Exception as e:
            print(e)
        return self

    #更新指定的数据记录 lists[{'id':5},{'name':'abc'}]
    def update(self,lists=[]):
        try:
            if lists:
                fields_list = []
                for list in lists:
                    str1 = ' '
                    (field,value), = list.items()
                    if isinstance(value,int):
                        str1 = ' '+ field + '=' + str(value)
                    elif isinstance(value,str):
                        str1 = ' '+ field + '=' + '"'+str(value)+ '"'
                    else:
                        str1 = ' '+ field + '=' + '"'+str(value)+ '"'
                    fields_list.append(str1)
                str1 = ' , '.join(fields_list)
                self.sqlupdatefields = ' set '+str1
            sql=self.makesql('update')
            # print(sql)
            self.cursor.execute(sql)
            self.connect.commit()
            return self.connect.affected_rows()
        except Exception as e:
            print(e)
            self.connect.rollback()
            return self
    #更新指定的数据记录 lists=[{'id':5},{'name':'abc'}]
    def insert(self,lists=[]):
        try:
            if lists:
                fields_name = []
                fields_value = []
                str1 = ' '
                for list in lists:
                    (field,value), = list.items()
                    fields_name.append(field)
                    if isinstance(value,str):
                        fields_value.append('"'+str(self.filter_str(value))+ '"')
                    elif isinstance(value,int):
                        fields_value.append(str(value))
                    else:
                        fields_value.append('"'+str(value)+ '"')
                self.sqlinsert = ' ('+' , '.join(fields_name)+') values ('+' , '.join(fields_value)+')'
            # print(self.sqlinsert)
            sql=self.makesql('insert')
            # print(sql)
            self.cursor.execute(sql)
            self.connect.commit()
            return self.connect.affected_rows()
        except Exception as e:
            print(e)
            self.connect.rollback()
            return self
    def filter_str(self,str=''):
        str=str.strip().replace("'",'').replace('"','')
        return str
if __name__=="__main__":
    pass
    mysql=Mysql()
    # where_data=[{'id':['=',2]}]
    # update_data=[{'catname':"we"}]
    insert_data=[{'keyword':"we"},{'title':"we"},{'answer':"wsssse"},{'uid':6}]
    # res=mysql.table('category').where(where_data).update(update_data)
    res=mysql.table('zhidao_scrapy_test').where([{'translate':['=',0]}]).count()
    insert_data=[{'title': '破碎机P0701"0"00是啥意思？'}, {'answer': '破碎机p0701000是啥意思？就是这个破碎机的型号，这个型号就是这个，以后东西坏了啥？这个型号买就行'}, {'uid': 3}]
    res=mysql.table('zhidao_scrapy_en').insert(insert_data)
    update_data = [{'keyword':'破碎机有哪几种？'}]
    # res=mysql.table('zhidao_scrapy_test').where([{'id':['=',1]}]).update(update_data)
    print(res)
