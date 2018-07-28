# -*- coding: utf-8 -*-
# website: https://loovien.github.io
# author: luowen<bigpao.luo@gmail.com>
# time: 2018/7/26 23:13
# desc:

import pymysql, logging, time, shutil
from os import path
from .config import ftpConf


class DbUtils(object):
    """

        create table if not exists files (
            id int unsigned not null auto_increment,
            filename varchar(255) not null default '' comment '文件名称',
            content blob not null comment '文件内容',
            created_at int unsigned not null default '0' comment '创建时间',
            primary key (id),
            index index_created_at (created_at)
        ) engine innodb charset utf8 comment '文件信息';


    """

    def get_conn(self):
        kwargs = {
            "host": ftpConf.get("dbhost", 'localhost'),
            "user": ftpConf.get("dbuser", "root"),
            "password": ftpConf.get("dbpwd", "111111"),
            "db": ftpConf.get("dbname", "test"),
            "charset": ftpConf.get("dbcharset", 'utf8'),
            "port": ftpConf.get("dbport", 3306),
            "cursorclass": pymysql.cursors.DictCursor,
        }
        return pymysql.connect(**kwargs)

    def record_files(self, files=[]):
        if len(files) == 0:
            logging.info("计入文件数量为空!")
            return True
        conn = self.get_conn()
        try:
            unixtime = int(time.time())
            for file in files:
                if not path.isabs(file):
                    absfile = path.abspath(file)
                if not path.isfile(absfile):
                    logging.error("文件:%s 不存在!", absfile)
                    continue
                fd = open(absfile, 'rb+')
                content = b"".join(fd.readlines())
                fd.close()
                with conn.cursor() as cursor:
                    record_sql = "INSERT INTO files (filename, content, created_at) VALUES {}".format(file, content,
                                                                                                      unixtime)
                    logging.info("execute record file SQL: ", record_sql)
                    cursor.execute(record_sql)
                    conn.commit()
        except Exception as e:
            logging.error("record file error", e)
        finally:
            conn.close()

    def flush_files(self):
        conn = self.get_conn()
        try:
            with conn.cursor() as cursor:
                flush_sql = "UPDATE files SET is_move = 1"
                logging.info("execute flush sql:", flush_sql)
                cursor.execute(flush_sql)
                conn.commit()

        except Exception as e:
            logging.error("update files sql error: ", e)
        finally:
            conn.close()

    def get_files(self):
        conn = self.get_conn()
        try:
            with conn.cursor() as cursor:
                file_sql = "SELECT * FROM files WHERE is_move = 0"
                cursor.execute(file_sql)
                result = cursor.fetchall()
                return result
        except Exception as e:
            logging.error("fetch all files error:", e)

        finally:
            conn.close()
