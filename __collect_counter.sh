# This should contains 2 parts
# part one concern all files at /dev/shm/gproxy that is not today
# part 2 concern all files that not related to the running pids
# 
# This file will run as a schedual job that copy all files at /dev/shm and process it to gproxy/counters and delete old files from shm 



before_today_counters=$(find /dev/shm/gproxy/counters -mtime +1 )
for file in before_today_counters
do
	python collect_coutner.py file
done 

