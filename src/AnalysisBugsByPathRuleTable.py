
from __future__ import print_function
import sys, os, copy

# This is not required if you've installed pycparser into
# your site-packages/ with setup.py
#
sys.path.extend(['.', '..'])


#筛选rules，出现在一个函数中计算support count时只计算一次
def reduceRules(fileList,FPRuleList,minSup,minConf):
   ruleCount=str(len(FPRuleList))#分析规则数
   funcSet=set([])
   for line in fileList:
      funcElement=line[len(line)-1]
      funcName=funcElement[0:funcElement.rfind('@')]
      funcName=funcElement[0:funcName.rfind('@')]
      funcSet.add(funcName)
   funcCount=len(funcSet)
   minSupCount=minSup*funcCount

   trvailRuleCount=0#conf=1的规则数量
   reducedFPRuleList=[]#约减后到规则
   lineCount=str(len(fileList))#分析文件行数，即路径数
   for rule in FPRuleList:
      ruleLeftSet=set(rule[0])
      confirmCount=0
      againstCount=0
      totalCount=0
      functionaAnalyzedForConfirm=set([])#出现在一个函数中计算support count时只计算一次
      functionaAnalyzedForTotal=set([])#出现在一个函数中计算support count时只计算一次
      functionaAnalyzedForAgainst=set([])#出现在一个函数中计算Against count时只计算一次
      for line in fileList:
         lineSet=set(line[0:len(line)-1])#每一行所有函数调用组成到集合
         funcElement=line[len(line)-1]
         funcName=funcElement[0:funcElement.rfind('@')]
         funcName=funcElement[0:funcName.rfind('@')]
         #print(lineSet)
         leftContain=True
         for rls in ruleLeftSet:
            if(rls not in line):#ruleLeftSet不在该行中，不需要分析该rule
               leftContain=False
               break
         if(leftContain == True):#rule 左边包含在line中，检查右边是否包含
            if(funcName not in functionaAnalyzedForTotal):
               functionaAnalyzedForTotal.add(funcName)
               totalCount=totalCount+1

            rightContain=True
            ruleRightSet=set(rule[1])
            for rrs in ruleRightSet:
               if(rrs not in lineSet):#right item not contain in  rule
                  rightContain=False
                  break
            if(rightContain==True and funcName not in functionaAnalyzedForConfirm):#confirm rule 
               functionaAnalyzedForConfirm.add(funcName)
               confirmCount=confirmCount+1
            else:#against rule
               functionaAnalyzedForAgainst.add(funcName)
               againstCount=againstCount+1
      if(confirmCount==totalCount and totalCount>minSupCount):
         trvailRuleCount=trvailRuleCount+1 
      if(totalCount>minSupCount and confirmCount/totalCount>minConf and confirmCount!=totalCount):
         reducedFPRuleList.append(rule)
         print(rule)
         print('conf:'+str(confirmCount/totalCount)+','+str(confirmCount)+'/'+str(totalCount))  

   
   print('Input '+str(len(FPRuleList))+' rules, reduce rule finished! analysis '+lineCount+' function call paths(in '+str(funcCount)+'functions), generate '+str(len(reducedFPRuleList))+' rules, including '+str(trvailRuleCount)+' rules with confidence 1.')

   return reducedFPRuleList

#根据FPRules 查找bug，出现在一个函数中计算support count时只计算一次
def findBugsByFPRules(fileList,FPRuleList):
   bugList=[]
   bugCount=0
   ruleCount=str(len(FPRuleList))#分析规则数
   trvailRuleCount=0#conf=1的规则书
   lineCount=str(len(fileList))#分析文件行数，即函数数
   for rule in FPRuleList:
      dicFuncBugCount=dict()

      ruleLeftSet=set(rule[0])
      confirmCount=0
      againstCount=0
      totalCount=0
      functionaFoundBugForCurrentRule=set([])#一个规则在一个函数中找到bug即可
      for line in fileList:
         lineSet=set(line[0:len(line)-1])#每一行所有函数调用组成到集合
         funcElement=line[len(line)-1]
         funcName=funcElement[0:funcElement.rfind('@')]
         funcName=funcElement[0:funcName.rfind('@')]
         if(funcName in functionaFoundBugForCurrentRule):
            continue
         #print(lineSet)
         leftContain=True
         for rls in ruleLeftSet:
            if(rls not in line):#ruleLeftSet不在该行中，不需要分析该rule
               leftContain=False
               break
         if(leftContain == True):#rule 左边包含在line中，检查右边是否包含
            rightContain=True
            ruleRightSet=set(rule[1])
            for rrs in ruleRightSet:
               if(rrs not in lineSet):#right item not contain in  rule
                  rightContain=False
                  break
            if(rightContain==False):#against rule ,find a bug
               if(funcName in dicFuncBugCount.keys()):
                  dicFuncBugCount[funcName]=dicFuncBugCount[funcName]+1
               else:
                  dicFuncBugCount[funcName]=1
                  bugCount=bugCount+1

               functionaFoundBugForCurrentRule.add(funcName)
               bugStr=str(bugCount)+'.'+str(dicFuncBugCount[funcName])+', Find a bug in: '+str(line)+', against rule: '+str(rule)
               bugList.append(bugStr)
   print('findBugsByFPRules finished! analysis '+lineCount+' function calls for '+ruleCount+' rules, find '+str(len(bugList))+' Bugs.')
   return bugList


#读取FPGrowth生成文件     
def loadFPGReslut(fileName):
   FPRuleList=[]#存放FPRule的list，每一条rule为一个两个元素的list，第二个元素是‘=>’右边，第一个为‘=>’左边的元素
   FPGFile = open(fileName,'r')
   for line in FPGFile:
      if (line.find(' = T')==-1):#该行不是关联规则格式
         continue
      line=line[line.find('	')+1:]
      line=line[0:line.rfind(' = T')+4]
      preLine=line[0:line.find('	')]
      subLine=line[line.find('	')+1:]#关联规则后半部分
      preLine=preLine.replace(' ', '')#去掉空格
      subLine=subLine.replace(' ', '')#去掉空格
      #print(line)
      #print(preLine)
      #print(subLine)
      #exit()
      FPRule=[]
      
      preLine=preLine.replace('=T', '')
      FPRuleLeft=preLine.split(',') 
      subLine=subLine.replace('=T', '')
      FPRuleRight=subLine.split(',') 

      FPRule.append(FPRuleLeft) 
      FPRule.append(FPRuleRight) 
      FPRuleList.append(FPRule)

   return FPRuleList

mappingFileName=sys.argv[1] 
mappingFile = open(mappingFileName,'r')
fileList=[]#所有行存到fileList中，每一个元素为一个lineList
for line in mappingFile:
   lineList=[]#每一行存一个list 前面为func 信息 最后一个元素为位置信息
   preLine=line[0:line.find('@')]
   lineList = preLine.split(',')  
   subLine=line[line.find('@'):len(line)-1]
   lineList.append(subLine)
   temp=copy.deepcopy(lineList)
   fileList.append(temp)

ruleFileName=sys.argv[2] 
FPRuleList=loadFPGReslut(ruleFileName)

reducedFPRuleList=reduceRules(fileList,FPRuleList,0.01,0.9)

FPbugList=findBugsByFPRules(fileList,reducedFPRuleList)
for bug in FPbugList:
   print(bug)





