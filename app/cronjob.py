#!/bin/env
# -*- coding: utf-8 -*-
# @website: https://loovien.github.io
# @author: luowen<bigpao.luo@gmail.com>
# @time: 2018/7/27 16:00
# @desc:

from .config import ftpConf
from .dbutils import DbUtils
from os import path
import base64
import os, shutil, logging


class CronJob(object):
    @staticmethod
    def local_job():
        dist_dir = ftpConf.get("dist_dir", None)
        download_dir = ftpConf.get("download_dir", None)
        if dist_dir is None or download_dir is None:
            raise Exception("本地或下载目录不存在")
        if not os.path.isabs(dist_dir):
            dist_dir = path.abspath(path.join(path.curdir, dist_dir))
        if not os.path.isabs(download_dir):
            download_dir = path.abspath(path.join(path.curdir, download_dir))
        logging.info("download dir: %s dist dir: %s", download_dir, dist_dir)
        files = os.listdir(download_dir)
        for file in files:
            absfile = path.abspath(path.join(download_dir, file))
            if os.path.isdir(absfile):
                logging.info("下载目录文件: %s 是目录", absfile)
                continue
            dist_file = path.abspath(path.join(dist_dir, file))
            shutil.move(absfile, dist_file)
            logging.info("移动文件: %s : %s", file, dist_file)

    @staticmethod
    def ftp_job():
        pass

    @staticmethod
    def dump_from_db():
        dbutil = DbUtils()
        file_rows = dbutil.get_files()
        dist_dir = ftpConf.get("dist_dir")
        print(file_rows)
        print(dist_dir)
        for row in file_rows:
            distfile = path.abspath(path.join(dist_dir, row["filename"]))
            print(distfile)
            logging.info("写入文件: %s", distfile)
            fd = open(distfile, 'ab+')
            print(row['content'])
            fd.write(base64.decodebytes(row['content']))
            fd.close()

    @staticmethod
    def import_to_db():
        dbutil = DbUtils()
        download_dir = path.abspath(ftpConf.get("download_dir"))
        files = os.listdir(download_dir)
        for file in files:
            absfile = path.abspath(file)
            if path.isdir(absfile):
                logging.info("下载目录文件: %s 是目录", absfile)
                continue
            if not path.isfile(absfile):
                logging.error("文件异常: %s", absfile)
            try:
                fd = open(absfile, "rb")
                content = base64.encodebytes(b"".join(fd.readlines()))
                logging.info("记录文件:%s 到数据库", absfile)
                dbutil.record_files(file, content)
                fd.close()
            except Exception as e:
                logging.error("读取文件发生异常: %s", e)

        logging.info("处理目录:%s 完成", download_dir)
