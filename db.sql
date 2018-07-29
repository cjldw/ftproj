-- 创建数据库
create database if not exists test;

-- 切换数据
use test;

-- 数据存储表
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
