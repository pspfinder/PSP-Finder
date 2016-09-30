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
for file in ./$1/* ;do
    #((test++))
    #if ((test>50)); then continue
    #fi
    echo $file
    dir=${file%/*}
    fileName=${file##*/}
    echo "python AnylysisFuncs.py $file >$2/$fileName.result"
    python AnylysisFuncs.py $file >$2/$fileName.result
    #cp -p $file ./$2
done

