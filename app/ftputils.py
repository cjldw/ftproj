# -*- coding: utf-8 -*-
# website: https://loovien.github.io
# author: luowen<bigpao.luo@gmail.com>
# time: 2018/7/26 23:13
# desc:

import pysftp, logging, shutil
from .config import ftpConf
from ftplib import FTP
from  os import path


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
        user = ftpConf.get("ftpuser")
        password = ftpConf.get("ftppwd")
        ftp = FTP(host=host)
        logging.info("登入ftp服务器: host: %s user: %s password: %s", host, user, password)
        resp = ftp.login(user=user, passwd=password)
        # ftp.encoding = "utf-8"
        logging.info("ftp服务器返回: %s", resp)
        filelist = ftp.nlst()
        ftp_dir = ftpConf.get("ftp_dir")
        download_dir = ftpConf.get("download_dir")
        absdownload_dir = path.abspath(download_dir)
        for file in filelist:
            try:
                ftpfile = path.abspath(path.join(ftp_dir, file))
                logging.info("从ftp上下载文件: %s", file)
                callback = open(ftpfile, "wb+")
                ftp.retrbinary("RETR " + file, callback.write)
                callback.close()
                shutil.move(ftpfile, path.join(absdownload_dir, file))  # ftp下载成功的文件拷贝到导入目录
                ftp.delete(file)
            except Exception as e:
                logging.error("处理ftp文件: %s 失败! error: %s", file, e)

        logging.info("ftp下载文件: %s 完成", filelist)
