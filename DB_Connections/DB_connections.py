import pyodbc

server = 'sql5088.site4now.net'
database = 'db_aa6e06_autismdb'
username = 'db_aa6e06_autismdb_admin'
password = 'Mo7amedatef17'

# بناء سلسلة الاتصال
connection_string = 'DRIVER={SQL SERVER};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password

class LinkDatabase:
    # Try-Catch بنستعملها دايما عشان لو في ايرور الكود يطلع الايرور ويكمل
    # try هيجرب الكود ولو ظبط يكمل ماظبطش يطلع ايرور 
    # catch هنا بيستقبل الايرور ويقولك في ايرور ويروح يكمل باقي ويقفل نفسه ويروح يكمل باقي الكود عادي بدون مايقف 
    def __init__(self):
        try:
            self.conn = pyodbc.connect(connection_string)            

            self.conn.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
            self.conn.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
            self.conn.setencoding(encoding='utf-8')

            self.cursor = self.conn.cursor()
            print("Conected")
            
        except Exception as e:
            print("Data Base Error", e)