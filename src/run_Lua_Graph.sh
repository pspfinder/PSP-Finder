#!/bin/bash

echo 'sudo ./compile.sh lua/src lua_pp >InfoCompile'
echo '使用compile.sh批量编译，第一个参数为输入文件夹路径，第二个参数为输出文件路径.....'
START=`date +%s%N`
sudo ./compile.sh lua/src lua_pp >InfoCompile
END=`date +%s%N`
costTime=$((($END-$START)/1000000))
echo '编译完成，耗时：'$costTime 'ms'


echo 'sudo ./GetFuncCalls.sh lua_pp lua_Funcs >infoGenerateFuncCall'
echo '使用GetFuncCalls.sh 批量生成函数调用信息，第一个参数为输入文件夹路径，第二个参数为输出文件路径.....'
START=`date +%s%N`
sudo ./GetFuncCalls.sh lua_pp lua_Funcs >infoGenerateFuncCall
END=`date +%s%N`
costTime=$((($END-$START)/1000000))
echo '函数调用信息生成完成，耗时：'$costTime 'ms'


echo 'python GenerateFuncData.py lua_Funcs/ >InfoFuncSet'
echo '使用GenerateFuncData.py生成函数调用集，生成*.arff和×.setMapping文件,第一个参数为输入文件夹路径，第二个参数为输出文件路径.....'
START=`date +%s%N`
python GenerateFuncData.py lua_Funcs/ >InfoFuncSet
END=`date +%s%N`
costTime=$((($END-$START)/1000000))
echo '函数调用集生成完成，耗时：'$costTime 'ms'


echo 'python AnalysisBugsBySetRuleTable.py lua_Funcs.setMapping FuncResult_lua >InfoBugBySet'
echo '使用关联规则查找bug....'
START=`date +%s%N`
python AnalysisBugsBySetRuleTable.py lua_Funcs.setMapping FuncResult_lua >InfoBugBySet
END=`date +%s%N`
costTime=$((($END-$START)/1000000))
echo '使用关联规则查找bug完成，耗时：'$costTime 'ms'


echo 'sudo ./GetFuncGraphs.sh lua_pp lua_Graphs >InfoGraph'
echo 'GetFuncGraphs.py生成函数调用图，第一个参数为输入文件夹路径.....'
START=`date +%s%N`
sudo ./GetFuncGraphs.sh lua_pp lua_Graphs >InfoGraph
END=`date +%s%N`
costTime=$((($END-$START)/1000000))
echo '函数调用图生成完成，耗时：'$costTime 'ms'


echo 'python GeneratePath.py lua_Graphs/ >InfoPath'
echo 'GeneratePath.py生成函数调用路径，第一个参数为输入文件夹路径.....'
START=`date +%s%N`
python GeneratePath.py lua_Graphs/ >InfoPath
END=`date +%s%N`
costTime=$((($END-$START)/1000000))
echo '函数调用路径生成完成，耗时：'$costTime 'ms'


echo 'python AnalysisBugsByPathRuleTable.py lua_Graphs.pathMapping PathResult_lua >InfoBugByPath'
echo '使用路径查找bug....'
START=`date +%s%N`
python AnalysisBugsByPathRuleTable.py lua_Graphs.pathMapping PathResult_lua >InfoBugByPath
END=`date +%s%N`
costTime=$((($END-$START)/1000000))
echo '使用路径查找bug完成，耗时：'$costTime 'ms'



