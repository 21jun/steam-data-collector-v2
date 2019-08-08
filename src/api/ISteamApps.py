import requests
import pymysql
import re

"""
How to use:
1. get GetAppList instance
2. call db_update_app_list method once
"""


class GetAppList:
    def __init__(self):
        connect = pymysql.connect(host='localhost', user='root', password='1qazxc', db='oasis', autocommit=True, port=3306)
        db = connect.cursor()
        self.db = db

    @staticmethod
    def api_get_app_list():
        """
        It's static because some cases use this method to get newest applist
        return all games in steam
        approximately 75000+
        :return: list of {"appid":"appid (number)" , "name":"game name"}
        """
        url = 'http://api.steampowered.com/ISteamApps/GetAppList/v0001/'
        req = requests.get(url)
        json_data = req.json()
        # print(json_data)
        applist = json_data['applist']['apps']['app']
        return applist

    def __db_insert_appid(self, sql, data):
        """
        TODO: prevent sql injection
        insert data into db
        :param sql: sql query
        :param data: data
        """
        # for app in data:
        #     appid = int(app['appid'])
        #     name = app['name'].replace('\"', "'")
        #     try:
        #         self.db.execute(sql % (appid, name))
        #     except:
        #         print("exception occur")
        #         continue
        #     # print(app)

        p = re.compile('[a-zA-z가-힣\s\w]')
        for app in data:
            appid = int(app['appid'])
            name = ''.join(p.findall(app['name']))
            try:
                self.db.execute(sql % (appid, name))
            except:
                print("db Error (maybe emoji problem)")
            print(app)

    def __db_clear_old_appid(self):
        """
        Clear exist appid table... (can be replaced with UPDATE way)
        """
        sql = '''TRUNCATE oasis.applist'''
        self.db.execute(sql)

    def db_update_app_list(self):
        """
        update applist table
        it takes 10~15 minutes...
        """
        data = self.api_get_app_list()
        print(data)
        self.__db_clear_old_appid()
        sql = '''
            INSERT INTO oasis.applist(appid, name) 
            VALUES ("%d",("%s")) '''

        self.__db_insert_appid(sql, data)
