#!/bin/bash

#sudo ./GetFuncCalls.sh infolder outfolder,like:
#under dir redis_ppc sudo ./GetFuncCalls.sh ppc outpput
#for var in A B C ; do
#   echo "var is $var"
#done

#创建输出目录
mkdir $2
echo "sudo chmod 777 $2"
test=0
for file in ./$1/* ;do
    ((test++))
    #echo $file
    #dir=${file%/*}
    #fileName=${file##*/}
    #echo "python explore_ast_redis.py $file >$2/$fileName.result"
    #python explore_ast_redis.py $file >$2/$fileName.result
    echo $test 'file compiled!'
    #cp -p $file ./$2
done

