# import pymssql
import pyodbc


# server = 'sql6028.site4now.net'
# database = 'db_aa9b62_autisocietydb'
# username = 'db_aa9b62_autisocietydb_admin'
# password = 'Sonbolmyasp123'

server = 'DESKTOP-T7CCNDN\MSSQLSERVER01'
database = 'AutismDB3'
username = 'salam'
password = '0123'

# بناء سلسلة الاتصال
connection_string = {
    'server': server,
    'user': username,
    'password': password,
    'database': database,
    # 'port' : 1433 ,
    # 'autocommit': True  # يمكنك تعيين هذا على True إذا كنت ترغب في تمكين التعامل مع البيانات بشكل تلقائي
}
class LinkDatabase:
    
    def __init__(self):
        self.conn = None
        self.cursor = None
        # print(pyodbc.drivers())
        self.connect()

    def connect(self):
        try:
            self.conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-T7CCNDN\MSSQLSERVER01;DATABASE=AutismDB3;UID=salam;PWD=0123')

            # self.conn = pyodbc.connect(connection_string)
            # self.conn = pymssql.connect(**connection_string)
            # self.conn = pymssql.connect(server=r'.\MSSQLSERVER01:1433', 
            #            user=r'salam', password=r'0123', database=r'AutismDB3')
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