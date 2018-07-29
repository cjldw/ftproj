#!/bin/sh
# @author: luowen<loovien@163.com>
# @time: 2018-07-28 10:00:03
# @desc: 服务启动脚本

pscmd=/bin/ps

getpid() {
    pid=$($pscmd -ef | grep -v grep | grep hot2dog.py | awk '{print $2}')
    echo $pid
}

start() {
    nohup python hot2dog.py > /dev/null &
    printf "hot2dog.py startup: %s\n" `getpid`
}

stop() {
    pid=`getpid`
    if [ !-z $pid ]
    then
        $(kill -9 $pid)
    fi
}

status() {
    pid=`getpid`
    if [ -z $pid ]; then
        echo "hot2dog.py is not running"
        exit 0
    fi
    printf "hot2dog.py is running. pid[%s]\n" $pid
}



case "$1" in
    start)
        start
    ;;
    stop)
        stop
    ;;
    status)
        status
    ;;
    *)
    echo $"Usage: $0 {start | stop | status}"
    exit 1
    ;;
esac

exit 0

