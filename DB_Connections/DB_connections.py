# import pymssql
import pyodbc


server = 'sql6028.site4now.net'
database = 'db_aa9b62_autisocietydb'
username = 'db_aa9b62_autisocietydb_admin'
password = 'Sonbolmyasp123'

# بناء سلسلة الاتصال
# connection_string = {
#     'server': server,
#     'user': username,
#     'password': password,
#     'database': database,
#     'autocommit': True  # يمكنك تعيين هذا على True إذا كنت ترغب في تمكين التعامل مع البيانات بشكل تلقائي
# }

connection_string = 'DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password


class LinkDatabase:
    
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.connect()

    def connect(self):
        try:
            self.conn = pyodbc.connect(connection_string)
            # self.conn = pymssql.connect(**connection_string)
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
