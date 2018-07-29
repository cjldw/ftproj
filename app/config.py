#!/bin/env
# -*- coding: utf-8 -*-
# @website: https://loovien.github.io
# @author: luowen<bigpao.luo@gmail.com>
# @time: 2018/7/27 12:36
# @desc: 配置文件

ftpConf = {
    "logpath": "./logs",
    "logfile": "app.log",
    "import_db_time": "10",  # 每隔多少分钟将文件导入
    "dump_db_time": "20",  # 每隔多少分钟将数据库的文件导出
    "ftp_download_time": "1000010", # 每隔多少时间从ftp服务器下载文件
    "ftp_dir": "./tmp/ftp",  # ftp目录
    "download_dir": "./tmp/import",  # 下载目录
    "dist_dir": "./tmp/dump",  # 目标移动的目录
    "dbhost": "localhost",
    "dbname": "test",
    "dbuser": "root",
    "dbpwd": "111111",
    "dbport": 3306,
    "dbcharset": "utf8",
    "ftphost": "localhost",
    "ftptype": "ftp",
    "ftpuser": "luowen",
    "ftppwd": "123456",
    "ftpport": "22",
}
