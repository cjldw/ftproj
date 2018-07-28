# -*- coding: utf-8 -*-
# website: https://loovien.github.io
# author: luowen<bigpao.luo@gmail.com>
# time: 2018/7/26 23:13
# desc:

#import pysftp
from .config import ftpConf
from ftplib import FTP


class FtpUtils(object):
    @staticmethod
    def download_sftp():
        kwargs = {
            "host": ftpConf.get("ftphost"),
            "username": ftpConf.get("ftpuser"),
            "password": ftpConf.get("password"),
        }
        conn = pysftp.Connection(**kwargs)
        files = conn.listdir()
        print(files)

    @staticmethod
    def download_ftp():
        host = ftpConf.get("ftphost")
        user = ftpConf.get("user")
        password = ftpConf.get("password")
        ftp = FTP(host=host)
        resp = ftp.login(user=user, passwd=password)
        print(resp)

