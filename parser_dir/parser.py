import requests
import logging
from fake_useragent import UserAgent

Log_Format = "%(levelname)s %(asctime)s - %(message)s"

logging.basicConfig(filename = "logfile.log",
                    filemode = "w",
                    format = Log_Format,
                    level = logging.ERROR)

logger = logging.getLogger()


HEADERS = {
    "User-Agent": UserAgent().chrome
  }


def is_continue(url):
    try:
        temp = url
        url = 'https://api.remanga.org/api/titles' + temp[temp.rfind('/'):]

        response = requests.get(url=url, headers=HEADERS)
        with open('headers.txt', 'w') as f:
            f.write(str(response.headers))
        status = response.json()['content']['status']['name']
        if status != "Продолжается":
            return 0
        return 1
    except Exception as ex:
        logger.error(ex)
        print(ex)
        return ex



