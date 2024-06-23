import pymssql
# import pyodbc


# server = 'sql6028.site4now.net'
# database = 'db_aa9b62_autisocietydb'
# username = 'db_aa9b62_autisocietydb_admin'
# password = 'Sonbolmyasp123'

# server = 'DESKTOP-T7CCNDN\MSSQLSERVER01'
# database = 'AutismDBNew'
# username = 'auti'
# password = '123456'

server = '.'
database = 'AutismDB'
username = 'autism'
password = '123456'

#AutismDBNew

# بناء سلسلة الاتصال
connection_string = {
    # 'Integrated_Security':True,
    'server': 'DESKTOP-T7CCNDN\MSSQLSERVER01',
    'user': 'auti',
    'password': '123456',
    'database': 'AutismDBNew',
    
    # 'port' : 1433 ,
    # 'autocommit': True,  # يمكنك تعيين هذا على True إذا كنت ترغب في تمكين التعامل مع البيانات بشكل تلقائي
    
}
print(connection_string)

connection_string['server'] = connection_string['server'].replace('\\\\','\\')
print(connection_string)
# conn = pymssql.connect(server = 'DESKTOP-T7CCNDN\MSSQLSERVER01', database = 'AutismDBNew')

class LinkDatabase:
    
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.connect()

    def connect(self):
        try:
            # self.conn = pyodbc.connect(connection_string)
            self.conn = pymssql.connect(server='DESKTOP-T7CCNDN\MSSQLSERVER01',database='AutismDBNew',user='auti',password='123456')
            # self.conn = pymssql.connect(server='.\\SQLEXPRESS2',database='BookingSystemDB',user='sa',password='123')
            self.cursor = self.conn.cursor()
            print("Connected")
        except Exception as e:
            print("Database Error:", e)

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

linkDB = LinkDatabase()
