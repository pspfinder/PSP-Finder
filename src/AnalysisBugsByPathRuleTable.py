
from __future__ import print_function
import sys, os, copy

# This is not required if you've installed pycparser into
# your site-packages/ with setup.py
#
sys.path.extend(['.', '..'])


#reduce association rules by supportCount_w and confidence_w
def reduceRules(fileList,FPRuleList,minSup,minConf):
   ruleCount=str(len(FPRuleList))#number of association rules
   funcSet=set([])
   for line in fileList:
      funcElement=line[len(line)-1]
      funcName=funcElement[0:funcElement.rfind('@')]
      funcName=funcElement[0:funcName.rfind('@')]
      funcSet.add(funcName)
   funcCount=len(funcSet)
   w=1
   minSupCount=minSup*funcCount*w

   trvailRuleCount=0
   reducedFPRuleList=[]#the list of rules reduced
   lineCount=str(len(fileList))#number of lines, also number of paths
   for rule in FPRuleList:
      ruleLeftSet=set(rule[0])
      confirmCount=0
      againstCount=0
      totalCount=0
      functionaAnalyzedForConfirm=set([])#only count w times in one fuction for supportCount
      functionaAnalyzedForTotal=set([])#only count w times in one fuction for supportCount
      functionaAnalyzedForAgainst=set([])#only count w times in one fuction for againt count
      leftCount=dict()#map from function name to number, count the times left part contain in the paths of the function 
      wholeCount=dict()#map from function name to number, count the times left and right parts contain in the paths of the function 
      for line in fileList:
         lineSet=set(line[0:len(line)-1])#the set composed by all the func call statements in one line
         funcElement=line[len(line)-1]
         funcName=funcElement[0:funcElement.rfind('@')]
         funcName=funcElement[0:funcName.rfind('@')]
         #print(lineSet)
         leftContain=True
         for rls in ruleLeftSet:
            if(rls not in line):#ruleLeftSet is not included in the line, continue without analysis
               leftContain=False
               break
         if(leftContain == True):#check if the left part of rule contains in the line, check right part
            if(funcName not in leftCount.keys()):
               leftCount[funcName]=1
            else:
               if(leftCount[funcName]<w):
                  leftCount[funcName]=leftCount[funcName]+1

            rightContain=True
            ruleRightSet=set(rule[1])
            for rrs in ruleRightSet:
               if(rrs not in lineSet):#right item not contain in  rule
                  rightContain=False
                  break
            if(rightContain==True):#confirm rule 
               if(funcName not in wholeCount.keys()):
                  wholeCount[funcName]=1
               else:
                  if(wholeCount[funcName]<w):
                     wholeCount[funcName]=leftCount[funcName]+1
      
      totalCount=0
      for k in leftCount.keys():
          totalCount=totalCount+leftCount[k]
      confirmCount=0
      for k in wholeCount.keys():
          confirmCount=confirmCount+leftCount[k]
      
      if(totalCount>minSupCount and confirmCount/totalCount>minConf and confirmCount!=totalCount):
      #if(confirmCount/totalCount>minConf and confirmCount!=totalCount):
         reducedFPRuleList.append(rule)
         print(rule)
         print('conf:'+str(confirmCount/totalCount)+','+str(confirmCount)+'/'+str(totalCount))  

   
   print('Input '+str(len(FPRuleList))+' rules, reduce rule finished! analysis '+lineCount+' function call paths(in '+str(funcCount)+'functions), generate '+str(len(reducedFPRuleList))+' rules, including '+str(trvailRuleCount)+' rules with confidence 1.')

   return reducedFPRuleList

#find bugs by assocation fules, only count w times in one function for a rule
def findBugsByFPRules(fileList,FPRuleList):
   bugList=[]
   bugCount=0
   ruleCount=str(len(FPRuleList))#the number of rules need to be analyzed
   trvailRuleCount=0#rules with conf=1
   lineCount=str(len(fileList))#the number of functions
   for rule in FPRuleList:
      dicFuncBugCount=dict()

      ruleLeftSet=set(rule[0])
      confirmCount=0
      againstCount=0
      totalCount=0
      functionaFoundBugForCurrentRule=set([])#in one function, only need to find one bug for one rule
      for line in fileList:
         lineSet=set(line[0:len(line)-1])#the set composed by all the func call statements in one line
         funcElement=line[len(line)-1]
         funcName=funcElement[0:funcElement.rfind('@')]
         funcName=funcElement[0:funcName.rfind('@')]
         if(funcName in functionaFoundBugForCurrentRule):
            continue
         #print(lineSet)
         leftContain=True
         for rls in ruleLeftSet:
            if(rls not in line):#ruleLeftSet is not included in the line, continue without analysis
               leftContain=False
               break
         if(leftContain == True):#check if the left part of rule contains in the line, check right part
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


#read the file generated by FPGrowth     
def loadFPGReslut(fileName):
   FPRuleList=[]#save the list of association rules, one rule in FPRulelist composed by 2 elements, the first elment is the left part of association rule, the second element is the right part of association rule
   FPGFile = open(fileName,'r')
   for line in FPGFile:
      if (line.find(' = T')==-1):#not a association rule
         continue
      line=line[line.find('	')+1:]
      line=line[0:line.rfind(' = T')+4]
      preLine=line[0:line.find('	')]
      subLine=line[line.find('	')+1:]#the right side of association rules
      preLine=preLine.replace(' ', '')#eliminate space
      subLine=subLine.replace(' ', '')#eliminate space
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
fileList=[]#save all lines in fileList, one line in a lineList
for line in mappingFile:
   lineList=[]#one line save as a list, the first element is funcs, the second element is position info
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





