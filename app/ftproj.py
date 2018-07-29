# -*- coding: utf-8 -*-
# website: https://loovien.github.io
# author: luowen<bigpao.luo@gmail.com>
# time: 2018/7/26 21:15
# desc:  ftp project every two minute download files from ftp server. and record to db.

import os, logging, sys, time, schedule
from logging.handlers import TimedRotatingFileHandler
from .config import ftpConf
from .cronjob import CronJob
from .ftputils import FtpUtils
from pathlib import Path
from os import path


class Ftproj(object):
    def __init__(self):
        self.init_log()
        self.init_dir()

    def init_dir(self):
        """
        初始化运行时所需要的目录
        :return:
        """
        # initial log_dir
        logpath = ftpConf.get("logpath", "./logs")
        if not path.isabs(logpath):
            logpath = path.abspath(logpath)
        if not path.isdir(logpath):
            Path(logpath).mkdir(parents=True, exist_ok=True)

        # initial download_dir
        download_dir = ftpConf.get("download_dir")
        if not path.isabs(download_dir):
            download_dir = path.abspath(download_dir)
        if not path.isdir(download_dir):
            Path(download_dir).mkdir(parents=True, exist_ok=True)

        # initial dist_dir
        dist_dir = ftpConf.get("dist_dir")
        if not path.isabs(dist_dir):
            dist_dir = path.abspath(dist_dir)
        if not path.isdir(dist_dir):
            Path(dist_dir).mkdir(parents=True, exist_ok=True)

        # initial ftp_dir
        ftp_dir = ftpConf.get("ftp_dir")
        if not path.isabs(ftp_dir):
            ftp_dir = path.abspath(ftp_dir)
        if not path.isdir(ftp_dir):
            Path(ftp_dir).mkdir(parents=True, exist_ok=True)

    def init_log(self):
        """
        初始化日志文件
        :return:
        """
        root_logger = logging.getLogger(None)
        root_logger.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s %(filename)s[%(lineno)d] %(levelname)s: %(message)s')

        console = logging.StreamHandler(sys.stdout)
        console.setLevel(logging.INFO)
        console.setFormatter(formatter)
        root_logger.addHandler(console)

        logpath = ftpConf.get("logpath", "./logs")
        logfile = ftpConf.get("logfile", "app.log")
        abslogfile = os.path.join(logpath, logfile)
        rhandler = TimedRotatingFileHandler(abslogfile, when='D', backupCount=30)
        rhandler.setLevel(logging.INFO)
        rhandler.setFormatter(formatter)
        root_logger.addHandler(rhandler)
        logging.info("init log success.")

    def import_to_db(self):
        """
        定时将文件写入到数据库中
        :return:
        """
        CronJob.import_to_db()

    def dump_from_db(self):
        """
        定时从数据库导出数据文件
        :return:
        """
        CronJob.dump_from_db()

    def download_ftp(self):
        """
        定时下载ftp文件
        :return:
        """
        FtpUtils.download_ftp()

    def run(self):
        """
        程序运行入口
        :return:
        """
        import_db_time = int(ftpConf.get("import_db_time", 10))
        dump_db_time = int(ftpConf.get("dump_db_time", 5))
        ftp_download_time = int(ftpConf.get("ftp_download_time", 10))
        schedule.every(import_db_time).seconds.do(self.import_to_db)
        schedule.every(dump_db_time).seconds.do(self.dump_from_db)
        schedule.every(ftp_download_time).seconds.do(self.download_ftp)
        while True:
            schedule.run_pending()
            time.sleep(1)
