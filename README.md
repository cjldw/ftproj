# FTP 小需求 (热成狗)

实现了一个简单的需求:

1、每2s从某个远程ftp上面的文件夹里面读取所有文件 然后按文件逐个写到数据库（数据库格式 就一个自增字段一个文件名字段跟一个内容字段就好了）中，然后清空文件夹里面的数据
2、每2s从数据库中读取所有数据，然后写到固定目录中，清空数据库


### 配置信息

编辑 `app/config.py`, 填写关键的配置项

1. 下载目录, 导出目录
2. 数据库密码
3. ftp账号密码


## 安装部署

1. 安装 python3.x, python2不支持！ 推荐virtualenv
2. 安装 mysql5.5 或以上
3. 安装所需要的依赖库 `pip install -r requirements.txt`
4. 创建MySQL数据表 `mysql -uroot -ppwd < db.sql`
5. `./run.sh {start, stop, status}`





