# -*- coding: utf-8 -*-

import urllib
import urllib2
import cookielib
import lxml.html
import csv
import sys

# 用户名、密码
# LOGIN_USERNAME = '1406100037'
# LOGIN_PASSWORD = '******'
LOGIN_USERNAME = raw_input("输入用户名：")
LOGIN_PASSWORD = raw_input("输入密码：")

LOGIN_URL1 = 'https://cas.gzhu.edu.cn/cas_server/login'
LOGIN_URL2 = 'http://202.192.18.189/login_gzdx.aspx'


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
    '''
    发送POST请求提交表单
    使用cookie登录数字广大
    再次使用cookie登录"http://202.192.18.189/login_gzdx.aspx"
    然后再次发送POST请求提交表单查询成绩
    :return:查询成绩的html
    '''
    mcj = cookielib.MozillaCookieJar('mcj.txt')
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(mcj))
    html = opener.open(LOGIN_URL1).read()
    data = parse_form(html)
    data['username'] = LOGIN_USERNAME
    data['password'] = LOGIN_PASSWORD
    encoded_data = urllib.urlencode(data)
    request = urllib2.Request(LOGIN_URL1, encoded_data)
    response = opener.open(request)
    print(response.geturl())
    if (response.geturl() == LOGIN_URL1):
        print("无法登录数字广大！")
        print("帐号或者密码错误！")
        sys.exit()

    request = urllib2.Request(LOGIN_URL2, encoded_data)
    response = opener.open(request)
    print(response.geturl())

    html = opener.open(response.geturl()).read()
    tree = lxml.html.fromstring(html)
    path = tree.cssselect('#headDiv > ul > li:nth-child(6) > ul > li:nth-child(4) > a')[0].get('href')
    URL3 = 'http://202.192.18.184/' + \
           urllib.quote(path.encode('gbk'), safe='?=&')
    print(URL3)

    html = opener.open(URL3).read()
    data = parse_form(html)
    newData = {
        '__VIEWSTATE': data['__VIEWSTATE'],
        '__VIEWSTATEGENERATOR': data['__VIEWSTATEGENERATOR'],
        'Button2': data['Button2']
    }
    # print('data=', newData)

    encoded_data = urllib.urlencode(newData)
    request = urllib2.Request(URL3, encoded_data)
    response = opener.open(request)
    mcj.save(ignore_discard=True, ignore_expires=True)
    html = response.read()
    return html


def main():
    '''
    提取并保存成绩到“在校学习成绩.csv”文件中
    '''
    writer = csv.writer(open(u'在校学习成绩.csv', 'wb'))
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
