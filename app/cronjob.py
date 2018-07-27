#!/bin/env
# -*- coding: utf-8 -*-
# @website: https://loovien.github.io
# @author: luowen<bigpao.luo@gmail.com>
# @time: 2018/7/27 16:00
# @desc:

from .config import ftpConf
from os import path
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
