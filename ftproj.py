# -*- coding: utf-8 -*-
# website: https://loovien.github.io
# author: luowen<bigpao.luo@gmail.com>
# time: 2018/7/26 21:15
# desc:  ftp project every two minute download files from ftp server. and record to db.

import os, logging

class Ftproj(object):
    def __init__(self, download_dir, dist_dir):
        self.download_dir = download_dir
        self.dist_dir = dist_dir

    def init_dir(self):
        if not os.path.isdir("./logs", 0777):
            os.mkdir("./logs", 0777)

        if not os.path.isdir(self.download_dir):
            os.makedirs(self.download_dir, 0777)
        if not os.path.isdir(self.dist_dir):
            os.makedirs(self.dist_dir, 0777)

    def init_log(self):
        format =

