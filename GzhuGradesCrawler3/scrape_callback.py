# -*- coding: utf-8 -*-

import csv
import codecs
import sys
from bs4 import BeautifulSoup
from grades_crawler import grades_crawler


class ScrapeCallback:
    def __init__(self):
        self.writer = csv.writer(codecs.open(u'在校学习成绩.csv', 'w', encoding='utf-8'))

    def __call__(self, html):
        soup = BeautifulSoup(html, 'html5lib')
        table = soup.find(id='Datagrid1')
        row = []
        for tr in table.find_all('tr'):
            for td in tr.find_all('td'):
                row.append(td.get_text().strip())
            self.writer.writerow(row)
            row = []
        sys.exit()


if __name__ == '__main__':
    grades_crawler('https://cas.gzhu.edu.cn/cas_server/login', scrape_callback=ScrapeCallback())
