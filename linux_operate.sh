#查询内存消耗
df -h 
#查询所有线程
ps -aux
#将进程按运行时间排序，看哪个进程消耗的cpu时间最多
ps -ef | sort -k7
#看看有多少进程处于 Running 状态
top -i