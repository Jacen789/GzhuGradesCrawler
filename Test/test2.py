# -*- coding: utf-8 -*-

import urllib
import urllib2
import cookielib
import lxml.html
import csv


def parse_form(html):
    '''
    获取表单提交所需的所有隐藏域
    :param html: html代码
    :return: 该页面的表单提交所需的所有隐藏域
    '''
    tree = lxml.html.fromstring(html)
    data = {}
    for e in tree.cssselect('form input'):
        if e.get('name'):
            data[e.get('name')] = e.get('value').encode('utf-8')
    return data


def getRecordsHTML():
    mcj = cookielib.MozillaCookieJar()
    mcj.load('mcj.txt', ignore_discard=True, ignore_expires=True)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(mcj))
    URL3 = 'http://202.192.18.184/xscj_gc.aspx?xh=1406100037'
    html = opener.open(URL3).read()
    data = parse_form(html)
    newData = {
        '__VIEWSTATE': data['__VIEWSTATE'],
        '__VIEWSTATEGENERATOR': data['__VIEWSTATEGENERATOR'],
        'Button2': data['Button2']
    }

    encoded_data = urllib.urlencode(newData)
    request = urllib2.Request(URL3, encoded_data)
    response = opener.open(request)
    html = response.read()
    return html


def main():
    writer = csv.writer(open(u'在校学习成绩2.csv', 'wb'))
    tree = lxml.html.fromstring(getRecordsHTML())
    row = []

    for i in xrange(1, 100):
        flag = 1
        for j in xrange(15):
            try:
                row.append(tree.cssselect('#Datagrid1 > tr:nth-child(%s) > td' % i)[j].text_content().strip().encode('utf-8'))
            except Exception:
                flag = 0
        if flag == 0:
            break
        writer.writerow(row)
        row = []


if __name__ == '__main__':
    main()
