import pyodbc
import os
import platform
import pymssql


server = 'sql5088.site4now.net'
database = 'db_aa6e06_autismdb'
username = 'db_aa6e06_autismdb_admin'
password = 'Mo7amedatef17'


os.environ["ODBCSYSINI"] = "/home/AutiSociety"

# بناء سلسلة الاتصال
# connection_string = 'DRIVER={SQL SERVER};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password+';Connection Timeout=30'

class LinkDatabase:
    # Try-Catch بنستعملها دايما عشان لو في ايرور الكود يطلع الايرور ويكمل
    # try هيجرب الكود ولو ظبط يكمل ماظبطش يطلع ايرور 
    # catch هنا بيستقبل الايرور ويقولك في ايرور ويروح يكمل باقي ويقفل نفسه ويروح يكمل باقي الكود عادي بدون مايقف 
    def __init__(self):
        # print(pyodbc.drivers())
        # print(os.name)
        # print(platform.system())
        try:
            # self.conn = pyodbc.connect(connection_string)   
            self.conn = pyodbc.connect('DSN=sqlserverdatasource;Uid=db_aa6e06_autismdb_admin;Pwd=Mo7amedatef17;Encrypt=yes;Connection Timeout=30;')
         

            self.conn.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
            self.conn.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
            self.conn.setencoding(encoding='utf-8')

            self.cursor = self.conn.cursor()
            print("Conected")
            
        except Exception as e:
            print("Data Base Error", e)