#!/bin/bash

#sudo ./run_PSP-Finder.sh projectName folderOfSourceCode
#sudo ./run_PSP-Finder.sh redis redis/src
#sudo ./run_PSP-Finder.sh lua lua/src
#sudo ./run_PSP-Finder.sh sqlite sqlite

if [ $1 = 'redis' ]
   then
   complier=compile_redis.sh
else
   complier=compile.sh
fi

echo 'compile files under folder with compile.sh, the first parameter is input floder, the second parameter is output folder.....'
START=`date +%s%N`
echo "sudo ./$complier $2 $1_pp >InfoCompile_$1"
sudo ./$complier $2 $1_pp >InfoCompile_$1
if [ $1 = 'redis' ]
   then
   echo "sudo ./compile_redis.sh redis/src/modules $1_pp >InfoCompile_$1"
   sudo ./$complier $2/modules $1_pp >InfoCompile_$1
fi
END=`date +%s%N`
costTime=$((($END-$START)/1000000))
echo 'complie finished, cost time: '$costTime 'ms'

#for project redis, exculde file: cluster.c
cd $1_pp
rm -rf cluster_pp.c
cd ..


echo 'Generat function call information with GetFuncCalls.sh, the first parameter is input floder, the second parameter is output folder.....'
START=`date +%s%N`
echo "sudo ./GetFuncCalls.sh $1_pp $1_Funcs >infoGenerateFuncCall_$1"
sudo ./GetFuncCalls.sh $1_pp $1_Funcs >infoGenerateFuncCall_$1
END=`date +%s%N`
costTime=$((($END-$START)/1000000))
echo 'Function call information generated, cost time:'$costTime 'ms'


echo 'Generete function call set with GenerateFuncData.py, generate file: *.arff and *.setMapping, the first parameter is input floder, the second parameter is output folder.....'
START=`date +%s%N`
echo "python GenerateFuncData.py $1_Funcs/ >InfoFuncSet_$1"
python GenerateFuncData.py $1_Funcs/ >InfoFuncSet_$1
END=`date +%s%N`
costTime=$((($END-$START)/1000000))
echo 'Function call sets generated, cost time: '$costTime 'ms'


echo 'Finding bugs with path-insenitive association rules....'
START=`date +%s%N`
echo "python AnalysisBugsBySetRuleTable.py $1_Funcs.setMapping FuncResult_$1 >InfoBugBySet_$1"
python AnalysisBugsBySetRuleTable.py $1_Funcs.setMapping FuncResult_$1 >InfoBugBySet_$1
END=`date +%s%N`
costTime=$((($END-$START)/1000000))
echo 'Found bugs with path-insensitive association rules, cost time:'$costTime 'ms'


echo 'Generate function call graph with GetFuncGraphs.py, the first parameter is input folder.....'
START=`date +%s%N`
echo "./GetFuncGraphs.sh $1_pp $1_Graphs >InfoPathSet_$1"
sudo ./GetFuncGraphs.sh $1_pp $1_Graphs >InfoPathSet_$1
END=`date +%s%N`
costTime=$((($END-$START)/1000000))
echo 'Function call graphs generated, cost time: '$costTime 'ms'



echo 'Generate function call paths with GeneratePath.py, the first parameter is the input folder.....'
START=`date +%s%N`
echo "python GeneratePath.py $1_Graphs/ >$1Path"
python GeneratePath.py $1_Graphs/ >$1Path
END=`date +%s%N`
costTime=$((($END-$START)/1000000))
echo 'Function call paths generated, cost time: '$costTime 'ms'


echo "Finding bugs with path-sensitive association rules...."
START=`date +%s%N`
echo "python AnalysisBugsByPathRuleTable.py $1_Graphs.pathMapping PathResult_$1 >InfoBugByPath_$1"
python AnalysisBugsByPathRuleTable.py $1_Graphs.pathMapping PathResult_$1 >InfoBugByPath_$1
END=`date +%s%N`
costTime=$((($END-$START)/1000000))
echo 'Found bugs with path-sensitive association rules, cost time: '$costTime 'ms'

