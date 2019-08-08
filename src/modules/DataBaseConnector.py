import pymysql

class DataBaseConnector:

    def __init__(self):
        connect = pymysql.connect(host='localhost', user='root', password='1qazxc', db='oasis', port=3306)
        db = connect.cursor()
        self.db = db

    def db_reconnect(self):
        connect = pymysql.connect(host='localhost', user='root', password='1qazxc', db='oasis', port=3306)
        db = connect.cursor()
        self.db = db

    def test(self):
        print("test")
