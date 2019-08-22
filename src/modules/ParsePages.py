import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from src.utills.UrlGenerator import url_generator
from src.crawler import SteamAppParser


def page_parser(data_base, table):
    apps = data_base.db_get_apps(table)
    data_base.db_reconnect()
    crawler = SteamAppParser.HeadlessChrome('C:/chromedriver_win32/chromedriver')

    for idx, app in enumerate(apps):

        # headless chrome 이 도중 연결이 끊길때를 대비하여 30번마다 재접속
        # 만약 스케쥴러로 이 작업을 반복한다면 db_reconnect 도 고려해야함 (loop 밖에서)
        if idx % 30 == 0:
            crawler.reconnect()

        info = {
            'appid': int(app[0]),
            'name': app[1]
        }

        print("currently working on:", info['appid'], info['name'])

        try:
            # Soup Process
            soup = crawler.parse_url(url_generator(info['appid']))
            if soup == None:
                print(f"can't soup this app{info['appid']}")
                continue

            # Parsing Process
            result = SteamAppParser.GetAppInfo(soup, info).get_info()
            if result == None:
                print(f"can't get result this app{info['appid']}")
                continue

            print(result)
            # DB insert Process
            data_base.db_update_app_data(result)

        except:
            continue


if __name__ == "__main__":
    # initialize
    data_base = SteamAppParser.SP_DataBaseConnector()

    # 3700+ 개의 게임을 한번에 수집시키면 도중에 web driver 가 멈추곤함
    # 크롤러는 700개정도의 게임을 연속으로 수집한 후에 에러 발생 (재접속등을 고려해야함)
    # 추후에 연속으로 수집할 방법을 찾으면 params 으로 'watching_games' 넘겨주고 연속으로 실행 시켜야함
    page_parser(data_base, 'watching_games')
