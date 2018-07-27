# -*- coding: utf-8 -*-
# website: https://loovien.github.io
# author: luowen<bigpao.luo@gmail.com>
# time: 2018/7/26 21:15
# desc:  ftp project every two minute download files from ftp server. and record to db.

import os, logging, sys, time, schedule
from logging.handlers import TimedRotatingFileHandler
from .config import ftpConf
from .cronjob import CronJob


class Ftproj(object):
    def __init__(self):
        self.init_log()
        self.init_dir()

    def init_dir(self):
        logpath = ftpConf.get("logpath", "./logs")
        if not os.path.isdir(logpath):
            os.mkdir(logpath, 777)

    def init_log(self):
        rootLogger = logging.getLogger(None)
        rootLogger.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s %(filename)s[%(lineno)d] %(levelname)s: %(message)s')

        console = logging.StreamHandler(sys.stdout)
        console.setLevel(logging.INFO)
        console.setFormatter(formatter)
        rootLogger.addHandler(console)

        logpath = ftpConf.get("logpath", "./logs")
        logfile = ftpConf.get("logfile", "app.log")
        abslogfile = os.path.join(logpath, logfile)
        rhandler = TimedRotatingFileHandler(abslogfile, when='D', backupCount=30)
        rhandler.setLevel(logging.INFO)
        rhandler.setFormatter(formatter)
        rootLogger.addHandler(rhandler)
        logging.info("init log success.")

    def ftp_job(self):
        print("download from ftp")
        pass

    def local_job(self):
        CronJob.local_job()

    def run(self):
        schedule.every(2).minutes.do(self.ftp_job)
        schedule.every(2).seconds.do(self.local_job)
        while True:
            schedule.run_pending()
            time.sleep(1)
