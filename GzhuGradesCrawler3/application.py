# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import *
from grades_crawler import grades_crawler
from scrape_callback import ScrapeCallback
from disk_cache import DiskCache


class App(QDialog):

    def __init__(self):
        self.qt_app = QApplication(sys.argv)
        QDialog.__init__(self, None)

        self.setWindowTitle(u"教务系统成绩查询")
        self.setMinimumSize(300, 200)

        self.vbox = QVBoxLayout()

        self.label1 = QLabel(u"用户名", self)
        self.edit1 = QLineEdit(self)
        self.label2 = QLabel(u"密码", self)
        self.edit2 = QLineEdit(self)
        self.button = QPushButton(u"登录")
        self.button.clicked.connect(self.crawler)

        self.vbox.addWidget(self.label1)
        self.vbox.addWidget(self.edit1)
        self.vbox.addWidget(self.label2)
        self.vbox.addWidget(self.edit2)
        self.vbox.addStretch(100)
        self.vbox.addWidget(self.button)
        self.setLayout(self.vbox)

    def crawler(self):
        login_url = 'https://cas.gzhu.edu.cn/cas_server/login'
        username = self.edit1.text()
        password = self.edit2.text()
        grades_crawler(login_url, username=username, password=password,
                       scrape_callback=ScrapeCallback(), cache=DiskCache())
        sys.exit()

    def run(self):
        self.show()
        self.qt_app.exec_()


if __name__ == '__main__':
    app = App()
    app.run()
