import pymssql

server = 'sql6028.site4now.net'
database = 'db_aa9b62_autisocietydb'
username = 'db_aa9b62_autisocietydb_admin'
password = 'Sonbolmyasp123'

# بناء سلسلة الاتصال
connection_string = {
    'server': server,
    'user': username,
    'password': password,
    'database': database,
    'autocommit': True
}

class LinkDatabase:
    
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.connect()

    def connect(self):
        try:
            print("Attempting to connect to database...")
            self.conn = pymssql.connect(**connection_string)
            self.cursor = self.conn.cursor()
            print("Connected to database successfully.")
        except Exception as e:
            print("Database connection error:", e)

    def close(self):
        if self.cursor:
            print("Closing cursor...")
            self.cursor.close()
        if self.conn:
            print("Closing connection...")
            self.conn.close()

linkDB = LinkDatabase()
