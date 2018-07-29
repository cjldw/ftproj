#!/bin/env
# -*- coding: utf-8 -*-
# @website: https://loovien.github.io
# @author: luowen<bigpao.luo@gmail.com>
# @time: 2018/7/27 16:00
# @desc:

from .dbutils import DbUtils
import os, pysftp, logging, shutil
from .config import ftpConf
from ftplib import FTP
from  os import path


class CronJob(object):
    @staticmethod
    def dump_from_db():
        dbutil = DbUtils()
        file_rows = dbutil.get_files()
        dist_dir = ftpConf.get("dist_dir")
        for row in file_rows:
            distfile = path.abspath(path.join(dist_dir, row["filename"]))
            logging.info("写入文件: %s", distfile)
            fd = open(distfile, 'ab+')
            fd.write(row['content'])
            fd.close()
            dbutil.mark_file([row['id']])

    @staticmethod
    def import_to_db():
        dbutil = DbUtils()
        download_dir = path.abspath(ftpConf.get("download_dir"))
        files = os.listdir(download_dir)
        for file in files:
            absfile = path.abspath(path.join(download_dir, file))
            if path.isdir(absfile):
                logging.info("下载目录文件: %s 是目录", absfile)
                continue
            if not path.isfile(absfile):
                logging.error("文件异常: %s", absfile)
                continue
            fd = open(absfile, "rb+")
            # content = base64.encodebytes(b"".join(fd.readlines()))
            content = b"".join(fd.readlines())
            logging.info("记录文件:%s 到数据库", absfile)
            dbutil.record_files(file, content)
            fd.close()
            os.remove(absfile)
            logging.info("删除文件: %s", absfile)
        logging.info("处理目录:%s 文件数: %s 完成", download_dir, files)

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
        ftp.quit()
        logging.info("ftp下载文件: %s 完成", filelist)
