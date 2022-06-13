import requests


HEADERS = {
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
  }


def is_continue(url):
    try:
        temp = url
        url = 'https://api.remanga.org/api/titles' + temp[temp.rfind('/'):]

        response = requests.get(url=url, headers=HEADERS)
        status = response.json()['content']['status']['name']
        if status != "Продолжается":
            return 0
        return 1
    except Exception as ex:
        print(ex)
        return 2



