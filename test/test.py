#!/bin/env
# -*- coding: utf-8 -*-
# @website: https://loovien.github.io
# @author: luowen<bigpao.luo@gmail.com>
# @time: 2018/7/27 14:06
# @desc:

import time, os, shutil

from app.dbutils import DbUtils
from app.ftputils import FtpUtils


def maplab():
    list1 = [1, 2, 3, 4]
    y = "luowen"
    a = map(lambda x: "({},{})".format(x, int(time.time())), list1)
    print(",".join(list(a)))


def move_file():
    files = os.listdir("d:/vim")
    print(files)
    for file in files:
        absfile = os.path.join("d:/vim", file)
        a = os.path.isdir(absfile)
        print("文件%s是否是目录: %s", file, a)
        # shutil.move(file, "d:/test.py")


def sftp_download():
    FtpUtils.download_sftp()


def ftp_download():
    FtpUtils.download_ftp()


if __name__ == "__main__":
    # ftp_download()
    sftp_download()
