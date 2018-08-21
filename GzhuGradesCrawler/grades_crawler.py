# -*- coding: utf-8 -*-

import urlparse
import urllib
import urllib2
import cookielib
import re
import sys
import lxml.html
from bs4 import BeautifulSoup
from downloader import Downloader

DEFAULT_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'


def grades_crawler(login_url, username='1406100037', password='******', delay=5, user_agent=DEFAULT_AGENT,
                   proxies=None, num_retries=1, scrape_callback=None, cache=None):
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

    html = opener.open(login_url).read()
    data = parse_form(html)
    data['username'] = username
    data['password'] = password
    encoded_data = urllib.urlencode(data)
    request = urllib2.Request(login_url, encoded_data)
    response = opener.open(request)
    url1 = response.geturl()
    print('url1: ' + url1)
    if url1 == login_url:
        print('无法登录数字广大！')
        print('用户名或者密码错误！')
        sys.exit()

    html1 = response.read()
    # tree = lxml.html.fromstring(html1)
    # url2 = tree.cssselect('#layout_63 > a')[0].get('href')
    soup = BeautifulSoup(html1, 'lxml')
    url2 = soup.find('a', text=re.compile(u'教务系统'))['href']
    print('url2: ' + url2)

    D = Downloader(delay=delay, user_agent=user_agent, proxies=proxies, num_retries=num_retries, opener=opener,
                   cache=cache)
    html2 = D(url2)
    tree = lxml.html.fromstring(html2)
    url3 = tree.cssselect('#embeddedIframe')[0].get('src')
    print('url3: ' + url3)

    request = urllib2.Request(url3)
    response = opener.open(request)
    url4 = response.geturl()
    print('url4: ' + url4)

    html4 = response.read()
    soup = BeautifulSoup(html4, 'lxml')
    path = soup.find('a', text=u'成绩查询')['href']
    components = urlparse.urlsplit(url4)
    scheme = components.scheme
    netloc = components.netloc
    query = urllib.quote(path.encode('gbk'), safe='?=&')
    url5 = scheme + '://' + netloc + '/' + query
    print('url5: ' + url5)

    html5 = D(url5).decode('gbk')
    data = parse_form(html5)
    data1 = {
        '__VIEWSTATE': data['__VIEWSTATE'],
        '__VIEWSTATEGENERATOR': data['__VIEWSTATEGENERATOR'],
        'Button2': data['Button2']
    }
    encoded_data = urllib.urlencode(data1).encode('utf-8')
    grade = ''
    while grade == '':
        request = urllib2.Request(url5, encoded_data)
        response = opener.open(request)
        html5 = response.read().decode('gbk')
        tree = lxml.html.fromstring(html5)
        xftj = tree.cssselect('#xftj > b')[0].text_content()
        matchObj = re.match(ur'.*获得学分(.*?)；.*', xftj)
        if matchObj:
            grade = matchObj.group(1)
    print(u'获得学分:' + grade)
    if scrape_callback:
        scrape_callback(html5)


def parse_form(html):
    """
    获取表单提交所需的所有隐藏域
    :param html: html代码
    :return: 该页面的表单提交所需的数据
    """
    tree = lxml.html.fromstring(html)
    data = {}
    for e in tree.cssselect('form input'):
        if e.get('name'):
            data[e.get('name')] = e.get('value').encode('utf-8')
    return data


if __name__ == '__main__':
    grades_crawler('https://cas.gzhu.edu.cn/cas_server/login', delay=0, num_retries=1, user_agent=DEFAULT_AGENT)
