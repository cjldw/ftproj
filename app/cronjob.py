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
