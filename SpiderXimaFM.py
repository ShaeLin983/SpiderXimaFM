"""
分页爬取喜马拉雅《万物简史》音频
可指定爬取的初始页码和结束页码
"""

import requests
import json


class SpiderXimaFM(object):

    def __init__(self):
        self.base_url = "https://www.ximalaya.com/revision/play/album?albumId=6210975&pageNum={}&sort=0&pageSize=30"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
        }
        self.audio_list = []

    def get_response(self, url):
        response = requests.get(url, headers=self.headers)
        data = response.content
        dict_data = json.loads(data)['data']['tracksAudioPlay']
        return dict_data

    def parse_data(self, dict_data):

        for audio_data in dict_data:

            # audio不能放在for循环外面，因为append添加的是对象的引用，不是对象的值
            # audio放在外面的话，一直是一个对象一个地址，audio值刷新的话，前面append的值都会刷新
            # 放在for循环里面，才能创建新的audio对象，前面创建的audio才不会被刷新

            audio = {}
            audio["name"] = audio_data['trackName']
            audio["src"] = audio_data['src']
            self.audio_list.append(audio)

            print(self.audio_list)

    def save_data(self):
        for audio in self.audio_list:
            file_name = audio['name']
            file_url = audio['src']
            print(file_name)
            with open("audio/{}.m4a".format(file_name), "wb")as f:
                 f.write(requests.get(file_url, headers=self.headers).content)

    # 指定爬取的页码（起始页-结束页）
    def run(self, page_start=1, page_end=2):
        for i in range(page_start, page_end + 1):
            url = self.base_url.format(str(i))
            print(url)
            response = self.get_response(url)
            self.parse_data(response)
        self.save_data()


SpiderXimaFM().run()
