import requests
import datetime
from parsel import Selector


"""
    Homework#6
    1.0. Создать свой собственный скрапер для любого сайта из которого вы хотите парсить данные для пользователя
"""


class MyParsel:
    URL = "https://tproger.ru/"
    XPATH = '//article'
    link = '//h2[@class="article__title article__title--icon"]/a/@href'
    article = '//h2[@class="article__title article__title--icon"]/a/text()'

    def parse_data(self,):
        try:
            response = requests.request("GET", self.URL).text
            tree = Selector(response)
            article = tree.xpath(self.article).extract()
            link = tree.xpath(self.link).extract()
            post_data = tree.xpath(self.XPATH).extract()
            data = []
            for i in zip(article[:5], link, post_data):
                art = {}
                art['date'] = datetime.datetime.now().strftime('%Y-%m-%d')
                art['title'] = i[0].strip()
                art['link'] = i[1]
                art['post_data'] = i[2][19:27].replace('"', '')
                data.append(art)

            return data

        except:
            print('except')
            return []


pars = MyParsel()
for res in pars.parse_data():
    print(res)