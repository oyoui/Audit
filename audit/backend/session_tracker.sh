#!/bin/bash


#for loop 30.get process id by  random tag 
#if got the process id , start strace command 

path=$0
echo $0
path_start=${path%audit/*}
path_end=log/ssh_audit_$2.log


for i  in $(seq 1 30);do
   #echo $i $1
   process_id=`ps -ef |grep $1 |grep -v sshpass |grep -v grep | grep -v 'session_tracker.sh' |awk '{print $2}'` # run cmd and set the result to variable cmd
   #echo "process:  $process_id"
   if [ ! -z "$process_id"  ];then
	echo 'start run strace....'
        #strace -fp $process_id -t -o $path_objlog/ssh_audit_$2.log;
        strace -fp $process_id -t -o $path_start$path_end;
        break;
   fi

   sleep 1 
done;

 
