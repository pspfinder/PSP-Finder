#!/bin/bash


#create output directory
if [ -d $2 ]
  then
  echo 'output directory ' $2 ' already exist'
else
  echo 'create output directory ' $2 
  mkdir $2
  sudo chmod 777 $2
fi

test=0
destFileName=''
for file in ./$1/* ;do
    #echo $file
    dir=${file%/*}
    #echo $dir
    fileName=${file##*/}
    #check if it's c file
    if [[ $fileName != *'.c' ]]
    then
       echo 'not .c file' 
       continue  
    fi
    #echo $fileName
    ((test++))
    echo "compiling $file >$2/$fileName.c ......"
    echo $fileName
    destFileName=${fileName/.c/_pp.c}
    echo $destFileName
    cc -nostdinc -E -D'__attribute__(x)=' -Ipycparser/utils/fake_libc_include -Iredis/deps/lua/src -Iredis/deps/hiredis -Iredis/deps/linenoise -Iredis/complimentary $file  > $2/$destFileName

    echo "compile finished!"
    #cp -p $file > $2/$fileName
done
echo $test 'file compiled!'

