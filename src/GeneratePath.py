
from __future__ import print_function
import sys, os,copy

# This is not required if you've installed pycparser into
# your site-packages/ with setup.py
#
sys.path.extend(['.', '..'])


functionSet=set()
fileCount=0
funcCount=0
funcDefCount=0
funcList=list(functionSet)

#analysis each line
def analysisLine(line):
   #print(line)
   global funcCount 
   global funcDefCount 
   if('--------------Analysis' in line):
       funcDefCount = funcDefCount+1
   if('from:' in line):
      pos = line.find('()')
      rpos = line.rfind('()')
      fromFunc=line[line.find('from:')+5:pos+2]
      inFunc=line[line.find('to:')+3:rpos+2]
      #print(fromFunc)
      #print(inFunc)
      funcCount=funcCount+1
      functionSet.add(fromFunc)   
      functionSet.add(inFunc)   

#read reulst file
def readResultFile(file):
   input = open(file, 'r')
   for line in input:
     analysisLine(line)

#输出functioncallDef for weka
def outputFuncCallDefs():
   global funcList 
   funcList = list(functionSet)
   funcList.remove('f_entry()')
   funcList.remove('f_exit()')
   print("@relation 'FunctionCalls'")
   for func in funcList:
      print(str(funcList.index(func))+','+str(func))   
      arffFile.write('@attribute '+str(func)+' {F, T}\n')

#generate and output function call paths
index=1#record lines outputed
def outputPathsInGraph(dic,posStr):
    global funcList,index

    threshold=0#when number of threshold paths are generated, only generate paths with uncover elements
    pathCount=0
    totalPathCount=0#the number of all the paths
    completePath=[]
    path=['f_entry()']
    visited=set()

    segList=[]
    if ('f_entry()' in dic):
       entry=dic['f_entry()']
       #print(entry)
    else:
       return
    for e in entry:
       tempPath = copy.deepcopy(path)
       tempPath.append(e)
       #for p in tempPath:
       #    print('temp:'+p)
       segList.append(tempPath)
    
    while (len(segList)>0):
       segPath=segList.pop()
       tail=segPath[-1]
       #print('tail:'+tail)
       if (tail in dic):
             if((totalPathCount>threshold) and (tail in visited)):
                segPath.append(dic[tail][0])
                segList.append(segPath)
                continue
             next=dic[tail]
             for n in next:
                if(n in segPath):
                   continue
                else:
                   #if((pathCount>threshold) and (n in visited)):
                   #  continue
                   tempPath = copy.deepcopy(segPath)
                   tempPath.append(n)
                   segList.append(tempPath)
             visited.add(tail)
       elif (tail =='f_exit()'):
          totalPathCount=totalPathCount+1
          #visited=visited|set(tempPath)
          funcInPath=[]
          for t in tempPath:
              t=t[0:t.find(')')+1]
              if t not in funcInPath:
                 funcInPath.append(t)
          tempPath=sorted(funcInPath)
          #tempPath=(list(tempPathSet)).sort()
          if (tempPath not in completePath): 
             print(tempPath)
             completePath.append(tempPath)
             pathCount=pathCount+1
          #print('Generating '+str(len(completePath))+'Paths!')
    
    print(str(len(completePath))+'Paths generated!')
    #func=set([])
    for p in completePath:
       fIndexList=[]
       for f in p: 
          f=f[0:f.find(')')+1]
          #outFile.write(f+'\n')
          if(f in funcList):
             fIndex = funcList.index(f)
             #outFile.write(str(fIndex)+'\n')
             fIndexList.append(fIndex)

       fIndexList=list(set(fIndexList))
       fIndexList.sort()
       #   if (f=='f_entry()'or f=='f_exit()'):
       #       continue
       
       dataStr=''
       mappingStr=''
       for fi in fIndexList:
          #dataStr=dataStr+funcList[fi]+","
          mappingStr=mappingStr+str(funcList[fi])+',' 
          dataStr=dataStr+str(fi)+' T,' 
          #print('func:'+f[0:f.find(')')+1])
       if (len(dataStr)>0):
          #outFile.write(''+dataStr[:len(dataStr)-1]+'\n')
          #arffFile.write(dataStr[:len(dataStr)-1]+'@'+posStr+'@index:'+str(index)+'\n')
          mappingFile.write(mappingStr[:len(mappingStr)-1]+'@'+posStr+'@index:'+str(index)+'\n')
          arffFile.write('{'+dataStr[:len(dataStr)-1]+'}\n')
          index=index+1
    #for f in func:
    #    print('func:'+f)
    #for v in visited:
    #    print('visit:'+v)
    


#load function call graph
def loadGraph(file):
   dic={'':['']}
   del dic['']
   posStr=''
   input = open(file, 'r')

   for line in input:
      if('--------------Analysis' in line):
         posStr=line[line.find('Analysis-'):len(line)-1]
         print(line)
      elif('---------------finish' in line):  
         #print('finish load ')
         #for (k, v) in dic.items():
         #   print ("dic[%s] =" % k, v)
         outputPathsInGraph(dic,posStr)
         dic.clear()
      elif('from:' in line):
         pos = line.find('()')
         rpos = line.rfind('()')
         fromFunc=line[line.find('from:')+5:line.find(',')]
         toFunc=line[line.find('to:')+3:len(line)-1]
         if fromFunc==toFunc:
            continue
         if fromFunc in dic:
            dic[fromFunc].append(toFunc)
         else:
            dic[fromFunc]=[toFunc]
         #print(' load... '+fromFunc+'--->'+toFunc)


   #for path in paths:
   #   for func in path
   #outFile.write('{'+dataStr[:len(dataStr)-1]+'}\n')



outputFileDic = os.getcwd()
arffFileName=''
mappingFileName=''
if (len(sys.argv)>1):
   outputFileDic = os.path.join(outputFileDic,sys.argv[1])
   #outputFileName=sys.argv[2]

   preName=sys.argv[1][0:len(sys.argv[1])-1]
   arffFileName=preName+'.arff'
   mappingFileName=preName+'.pathMapping'

else:
   print('error: parameter less than 2')
   exit()
print(outputFileDic)




#currentDir = sys.path[0]
dirlist = os.listdir(outputFileDic)
for line in dirlist:
   #if (os.path.isfile(line)):
   fileString = str(line)
   dotPos = fileString.rfind('.') 
   fileType = fileString[dotPos:]
   #print(fileType)
   if(fileType=='.result'):#result file
      #print(line)
      fileCount=fileCount+1
      fullPathFile = os.path.join(outputFileDic,line)
      readResultFile(fullPathFile)

funcList = list(functionSet)
print('read '+str(fileCount)+' files, '+str(funcDefCount)+' Function Defs, '+str(funcCount)+' function calls, contain  '+str(len(functionSet))+' unrepeat function calls')


#outFile=open('outputGraph.arff','w') 
arffFile=open(arffFileName,'w') 
mappingFile=open(mappingFileName,'w') 

funcList.remove('f_entry()')
funcList.remove('f_exit()')
arffFile.write("@relation 'FunctionCallsInPaths'\n")
outputFuncCallDefs()
arffFile.write("@data\n")

#generate paths by graphs
arffFile
for line in dirlist:
   fileString = str(line)
   dotPos = fileString.rfind('.') 
   fileType = fileString[dotPos:]
   #print(fileType)
   if(fileType=='.result'):#result file
      #print(line)
      fileCount=fileCount+1
      fullPathFile = os.path.join(outputFileDic,line)
      loadGraph(fullPathFile)

arffFile.close()

