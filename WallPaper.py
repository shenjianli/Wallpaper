# -*- coding: UTF-8 -*-
import os
import requests
from bs4 import BeautifulSoup


class WallPaper(object):
    def __init__(self):
        self.tag = "StudyTest"
        self.url = "https://www.tt98.com/pcbz/mm/"
        self.head = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/106.0.0.0 Safari/537.36 "
        }

    def log(self, content):
        print(self.tag, content)

    def get_file_name(self, url):
        index = str(url).rfind('/')
        return str(url)[index:]

    def download_wall_img(self, url):
        self.download_img(self.get_file_name(url), url)

    def download_img(self, img_name, img_url):
        os.makedirs('./img/', exist_ok=True)
        r = requests.get(img_url, headers=self.head)
        with open('./img/{}'.format(img_name), "wb") as f:
            f.write(r.content)

    def down_res(self):
        response = requests.get(self.url, headers=self.head)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, "html.parser")
        datas = soup.find_all("div", class_="fleximage-item")
        # self.log(datas)
        net_url = []
        titles = []
        for i in datas:
            net_url.append(i.find('a').get("href"))
            titles.append(i.find('a').find('p').text)
        self.log(net_url)
        self.log(titles)
        index = 0
        for sub_net in net_url:
            title = titles[index]
            page_url = "https://www.tt98.com{}".format(sub_net)
            res = requests.get(page_url, headers=self.head)
            self.log(f"开始{title}系列图片")
            self.log(f"第1页地址{page_url}")
            index = index + 1
            if res.status_code == 200:
                res.encoding = "utf-8"
                soup = BeautifulSoup(res.text, "html.parser")
                img_url = soup.find("a", class_="photo-a").find("img").get("src").strip()
                total_pages = soup.find("a", class_="photo-a").get("data-total").strip()
                self.log("图片地址 {}".format(img_url))
                self.log("页数{}".format(total_pages))
                self.download_wall_img(img_url)
                for i in range(1, int(total_pages)):
                    next_url = "https://www.tt98.com{}_{}.html".format(sub_net[:sub_net.rfind('.')], i)
                    self.log("第{}页地址 {}".format(i + 1, next_url))
                    res = requests.get(next_url, headers=self.head)
                    if res.status_code == 200:
                        res.encoding = 'utf-8'
                        soup = BeautifulSoup(res.text, "html.parser")
                        img_url = soup.find("a", class_="photo-a").find("img").get("src").strip()
                        self.log("图片地址 {}".format(img_url))
                        self.download_wall_img(img_url)