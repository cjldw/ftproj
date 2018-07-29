# -*- coding: utf-8 -*-
# website: https://loovien.github.io
# author: luowen<bigpao.luo@gmail.com>
# time: 2018/7/26 23:13
# desc:

import pymysql, logging, time, shutil
from .config import ftpConf


class DbUtils(object):
    """

        create table if not exists files (
            id int unsigned not null auto_increment,
            filename varchar(255) not null default '' comment '文件名称',
            is_dump tinyint(3) not null default '0' comment '是否到处到文件',
            content blob not null comment '文件内容',
            created_at int unsigned not null default '0' comment '创建时间',
            primary key (id),
            index index_created_at (created_at),
            index index_is_dump(is_dump)
        ) engine innodb charset utf8 comment '文件信息';


    """

    def get_conn(self):
        kwargs = {
            "host": ftpConf.get("dbhost", 'localhost'),
            "user": ftpConf.get("dbuser", "root"),
            "password": ftpConf.get("dbpwd", "111111"),
            "db": ftpConf.get("dbname", "test"),
            "charset": ftpConf.get("dbcharset", 'utf8_bin'),
            "port": ftpConf.get("dbport", 3306),
            "binary_prefix": True,
            "cursorclass": pymysql.cursors.DictCursor,
        }
        return pymysql.connect(**kwargs)

    def record_files(self, filename="", content=""):
        if filename == "":
            logging.info("导入文件名为空!")
            return True
        conn = self.get_conn()
        try:
            unixtime = int(time.time())
            with conn.cursor() as cursor:
                record_sql = 'INSERT INTO files (filename, content, created_at) VALUES (%s,%s,%s)'
                logging.info("execute record filename: %s time: %s, content: %s", filename, unixtime, content)
                cursor.execute(record_sql, (filename, content, unixtime))
                conn.commit()
        except Exception as e:
            logging.error("record file error: %s", e)
        finally:
            conn.close()

    def delete_file(self, fd_list):
        conn = self.get_conn()
        try:
            with conn.cursor() as cursor:
                delete_sql = 'DELETE FROM files WHERE id in ({})'.format(fd_list)
                logging.info("删除文件: %s", delete_sql)
                conn.execute(delete_sql)
                conn.commit()
        except Exception as e:
            logging.error("删除数据记录发生错误: %s", e)
        finally:
            conn.close()

    def mark_file(self, id):
        conn = self.get_conn()
        try:
            with conn.cursor() as cursor:
                update_sql = 'UPDATE files SET is_dump = 1 WHERE id = %s'
                logging.info("标记文件迁移: %s : 参数: %s", update_sql, id)
                cursor.execute(update_sql, (id,))
            conn.commit()
        except Exception as e:
            logging.error("删除数据记录发生错误: %s", e)
        finally:
            conn.close()

    def flush_files(self):
        conn = self.get_conn()
        try:
            with conn.cursor() as cursor:
                flush_sql = "UPDATE files SET is_move = 1"
                logging.info("execute flush sql: %s", flush_sql)
                cursor.execute(flush_sql)
            conn.commit()

        except Exception as e:
            logging.error("update files sql error: %s", e)
        finally:
            conn.close()

    def get_files(self):
        conn = self.get_conn()
        try:
            with conn.cursor() as cursor:
                # 2分钟后再导出数据库中的文件
                file_sql = "SELECT * FROM files WHERE is_dump = 0 AND created_at <= unix_timestamp() - 120"
                cursor.execute(file_sql)
                result = cursor.fetchall()
                return result
        except Exception as e:
            logging.error("fetch all files error: %s", e)

        finally:
            conn.close()
