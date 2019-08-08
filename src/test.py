import pymysql


connect = pymysql.connect(host='localhost', user='root', password='1qazxc', db='oasis', charset='utf8mb4',
                          autocommit=True, cursorclass=pymysql.cursors.DictCursor, port=3306)
db = connect.cursor()
# sql = 'SELECT * from oasis.app_info2 limit 10'
sql = 'INSERT INTO oasis.new_table(idnew_table) VALUE(%d)'
db.execute(sql % (1))

