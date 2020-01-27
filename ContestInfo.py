# coding=utf-8
import requests
import json
import datetime as dt
from dotenv import load_dotenv
import os
from os.path import join

load_dotenv(verbose=True)
dotenv_path = join('./', '.env')
load_dotenv(dotenv_path)

reserved_list = set()
post_interval = 60 * 60 * 2


class ContestInfo:

    def __init__(self, time, name, url):
        base_url = 'https://atcoder.jp'

        self.time = dt.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
        self.name = name
        self.url = base_url + url
        self.posted = False

        is_reserved = False
        # reserved_listが空の時は無条件に入れる
        if len(reserved_list) == 0:
            is_reserved = False
        else:
            # classを格納しているので一つずつ取り出して確認する
            for r in list(reserved_list):
                if (r.time == self.time) and (r.name == self.name) and (r.url == self.url):
                    is_reserved = True

        # reverved_listと重複していなければ追加する
        if not is_reserved:
            reserved_list.add(self)

    # 指定時間内のコンテストがあるかどうか
    def judge(self):
        can_post = False

        diff = (self.time - dt.datetime.today())
        # diff = (dt.datetime.today() - self.time)

        # 2時間以内のコンテストがあるなら通知を許可する
        if (not self.posted) and (0 <= diff.days) and (diff.seconds <= post_interval):
            can_post = True
        # コンテストの開催時間が過ぎていたら配列から削除する
        elif diff.days < 0:
            reserved_list.remove(self)

        print(reserved_list)
        return can_post

    # slackに通知を出す
    def post(self):
        if self.judge():
            webhook_url = os.environ.get('WEBHOOK_URL')
            requests.post(
                webhook_url,
                json.dumps({'text': '{}\n{}\n{}'.format(self.time, self.name, self.url)}),
                headers={'Content-Type': 'application/json'}
            )
            self.posted = True
