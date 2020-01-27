# coding=utf-8
import requests
from bs4 import BeautifulSoup
import schedule
import time
from ContestInfo import ContestInfo


# 空白があるので調整して一行の文字列にする
def ajust_one_message(message):
    line = message.text.rsplit()
    return ' '.join(line)


# コンテスト情報をスクレイピングする
def scraping_contest_info():
    url = 'https://atcoder.jp/home'
    html = requests.get(url).text
    # html = open('atcoder.html')

    soup = BeautifulSoup(html, 'html.parser')
    div = soup.find('div', attrs={'id': 'contest-table-upcoming'})
    content = div.find_all('a')

    contest_list = []

    # コンテスト開始時間とコンテスト名がバラバラになっているので2つずつ回して1つにまとめる
    for i in range(0, len(content), 2):
        # タイムゾーン(%z)が+でついているので省く
        time = ajust_one_message(content[i]).split('+')[0]
        name = ajust_one_message(content[i + 1])
        # urlはダブルクォーテーションで区切られている
        url = str(content[i + 1]).replace(' ', '').split('\"')[1]

        contest_list.append(ContestInfo(time, name, url))

    return contest_list


# 定期実行
def job():
    contest_list = scraping_contest_info()
    for c in contest_list:
        c.post()


if __name__ == '__main__':
    # 設定時間ごとにjob関数を実行する
    schedule.every(1).hours.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)
