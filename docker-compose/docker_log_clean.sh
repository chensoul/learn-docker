# 在执行过程中若遇到使用了未定义的变量或命令返回值为非零，将直接报错退出
set -eu

logs=$(find /var/lib/docker/containers/ -name '*-json.log*')

for log in $logs
do
    echo "clean $log"
    cat /dev/null > $log
done
