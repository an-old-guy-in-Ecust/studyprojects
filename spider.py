import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


class Spider(object):
    def __init__(self, url):
        self.url = url

    @staticmethod
    def get_html(url: str) -> str:
        """
        发出请求并得到网页源代码
        :param url: 网址
        :return: 网站源代码
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/107.0.0.0 Safari/537.36'}
        req = requests.get(url, headers=headers)
        while req.status_code != 200:  # 服务器不稳定, 可能会502
            req = requests.get(url, headers=headers)
        html = req.content.decode('utf-8')
        return html

    def parse_html(self, path: str, prefix: str, f):
        """
        给出小说的目录页，返回整本小说的内容
        :param path: 在网站源代码中查找文字的路径
        :param prefix: 每个网站的前缀
        :param f: 文件
        :return:
        """
        html = self.get_html(self.url)
        soup = BeautifulSoup(html, 'lxml')
        list_name = soup.select(path)
        for item in tqdm(list_name):
            href = prefix + item['href']
            text = self.get_text(href)
            for t in text:
                f.write(t.text + '\n')

    def get_text(self, href) -> list:
        """
        返回该网页里的小说章节文字
        :param href:网址
        :return:网址里的小说内容
        """
        html = self.get_html(href)
        soup = BeautifulSoup(html, 'lxml')
        content = soup.select('#content>p')
        return content

    def run(self, filename):
        with open(filename, 'a+', encoding='utf-8') as f:
            f.truncate(0)
            self.parse_html(".list3>li>a", 'http://www.quanben.io/', f)


if __name__ == '__main__':
    S = Spider('http://www.quanben.io/n/jingyanmingmenshaoyeyeqianjin/list.html')
    S.run("惊艳！名门少爷拽千金")
