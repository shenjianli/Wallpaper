# -*- coding: UTF-8 -*-
import os
import re

import requests
from bs4 import BeautifulSoup


class StudyTest(object):
    def __init__(self):
        self.tag = "WallPaper"
        self.url = "https://www.tt98.com/pcbz/yingshi/"
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

    def test(self):
        self.log("--------------- start --------------------")
        response = requests.get(self.url, headers=self.head)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, "html.parser")
        # self.log(soup)
        self.log(soup.prettify())
        self.log(soup.title)
        self.log(soup.a)
        self.log(soup.a.name)
        self.log(soup.a.parent.name)
        self.log(soup.a.parent.parent.name)

        self.log(soup.a.attrs)
        self.log(soup.a.attrs['class'])
        self.log(soup.a.attrs['href'])

        self.log(soup.find_all("a"))
        self.log(soup.find_all("a"))

        matcher = re.compile(r'<a href="(.*?)" target="_blank"', re.S)
        datas = re.findall(matcher, str(soup))
        self.log(datas)

        div_box = re.compile(r'<div class="image-box .*?">(.*?)</div>\n<div class="page"', re.S)
        div_boxs = re.findall(div_box, str(soup))
        self.log(div_boxs)
        div_content = div_boxs[0]
        soup = BeautifulSoup(div_content, "html.parser")
        self.log(soup.prettify())
        # result = soup.find('div', class_="image-box .*?")
        # self.log(result)
        datas = soup.find_all("div", class_="fleximage-item")
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
        self.log("--------------- end --------------------")

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