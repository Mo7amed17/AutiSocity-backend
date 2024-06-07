import pymssql

server = 'sql8006.site4now.net'
database = 'db_aa9adb_autisociety17'
username = 'db_aa9adb_autisociety17_admin'
password = 'Mo7amedatef17'

# server = '.'
# database = 'AutismDB'
# username = 'autism'
# password = '123456'

# بناء سلسلة الاتصال
connection_string = {
    'server': server,
    'user': username,
    'password': password,
    'database': database,
    'autocommit': True  # يمكنك تعيين هذا على True إذا كنت ترغب في تمكين التعامل مع البيانات بشكل تلقائي
}

class LinkDatabase:
    
    def __init__(self):
        try:
            self.conn = pymssql.connect(**connection_string)
            self.cursor = self.conn.cursor()
            print("Connected")
            
        except Exception as e:
            print("Database Error:", e)

linkDB = LinkDatabase()