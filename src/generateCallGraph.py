#-----------------------------------------------------------------
# pycparser: explore_ast.py
#
# This example demonstrates how to "explore" the AST created by
# pycparser to understand its structure. The AST is a n-nary tree
# of nodes, each node having several children, each with a name.
# Just read the code, and let the comments guide you. The lines
# beginning with #~ can be uncommented to print out useful
# information from the AST.
# It helps to have the pycparser/_c_ast.cfg file in front of you.
#
# Copyright (C) 2008-2015, Eli Bendersky
# License: BSD
#-----------------------------------------------------------------
from __future__ import print_function
import sys

# This is not required if you've installed pycparser into
# your site-packages/ with setup.py
#
sys.path.extend(['.', '..'])

from pycparser import c_parser, c_ast, parse_file

def visitSubBlocWithPre(sbloc, precessors):
    if (sbloc is None):
       return  precessors
    sblocTyp = type(sbloc)
    #print(sblocTyp)


    if(sblocTyp == c_ast.Compound and sbloc.block_items is not None):
       for ssbloc in sbloc.block_items:
          precessors=recursiveVistWithPre(ssbloc, precessors)
    else:
       precessors=recursiveVistWithPre(sbloc, precessors)
    return precessors


def recursiveVistWithPre(bloc,precessors):
    if (bloc is None):
       return (father, brothers)
    blocTyp = type(bloc)

    preCount=len(precessors)
    if(preCount==0):
       print('error: precessors empty!')

    if(blocTyp == c_ast.FuncCall):
       nameBloc = bloc.name
       nameTyp=type(nameBloc)
       if(nameTyp == c_ast.StructRef):
          subNameBloc = bloc.name.field
          subNameTyp=type(subNameBloc)
          if(subNameTyp == c_ast.StructRef):
             next=subNameBloc.field.name+'()'+str(bloc.coord)
             #print('Funcation Call: %s() at %s, nameTyp %s' % (subNameBloc.field.name, bloc.coord, str(nameTyp)))     
          else:
             next=bloc.name.field.name+'()'+str(bloc.coord)
             #print('from:'+brother+',to:'+next)
             #print('Funcation Call: %s() at %s, nameTyp %s' % (bloc.name.field.name, bloc.coord, str(nameTyp)))       
       #else:   
       elif(nameTyp!=c_ast.UnaryOp and nameTyp!= c_ast.Cast):#函数指针
          next=bloc.name.name+'()'+str(bloc.coord)
          #print('from:'+brother+',to:'+next)
          #print('Funcation Call: %s() at %s, nameTyp %s' % (bloc.name.name, bloc.coord, str(nameTyp)))
       elif(nameTyp==c_ast.UnaryOp):
          next=''
       
       if(len(next)>0):
          for pre in precessors:
             print('from:'+pre+',to:'+next)
          #清空
          precessors=[]
          precessors.append(next)

    #if
    elif (blocTyp == c_ast.If):
       #print('c_ast.If father:'+father) 
       #for bro in brothers:
       #   print('brother:'+bro)
       #bloc.show()
       #print('begin show if block...')
       #bloc.show()
       #print('begin cond block...')
       precessors=visitSubBlocWithPre(bloc.cond,precessors)  
       #print('begin iftrue block...')
       truePre=visitSubBlocWithPre(bloc.iftrue,precessors)
       #print('begin iffalse block...')
       falsePre=visitSubBlocWithPre(bloc.iffalse,precessors)  
       #print('end iffalse block...')
       precessors=list(set(truePre)|set(falsePre))


    #二元操作
    elif (blocTyp == c_ast.BinaryOp):  
        precessors=visitSubBlocWithPre(bloc.left,precessors)  
        precessors=visitSubBlocWithPre(bloc.right,precessors)
      

    #for
    elif (blocTyp == c_ast.For):    
        precessors=visitSubBlocWithPre(bloc.init,precessors)
        precessors=visitSubBlocWithPre(bloc.cond,precessors)
        nextPre=visitSubBlocWithPre(bloc.next,precessors)
        stmtPre=visitSubBlocWithPre(bloc.stmt,precessors)
        precessors=list(set(precessors)|set(nextPre)|set(stmtPre))

    #Assignment
    elif (blocTyp == c_ast.Assignment):   
        precessors=visitSubBlocWithPre(bloc.lvalue,precessors)
        precessors=visitSubBlocWithPre(bloc.rvalue,precessors)
    
    #While
    elif (blocTyp == c_ast.While):    
        precessors=visitSubBlocWithPre(bloc.cond,precessors)
        stmtPre=visitSubBlocWithPre(bloc.stmt,precessors)
        precessors=list(set(precessors)|set(stmtPre))
    
    #DoWhile
    elif (blocTyp == c_ast.DoWhile):    
        precessors=visitSubBlocWithPre(bloc.stmt,precessors)
        precessors=visitSubBlocWithPre(bloc.cond,precessors)

    #UnaryOp
    elif (blocTyp == c_ast.UnaryOp):
       precessors=visitSubBlocWithPre(bloc.expr,precessors)
     
    #StructRef
    elif (blocTyp == c_ast.StructRef):
       precessors=visitSubBlocWithPre(bloc.name,precessors)
       precessors=visitSubBlocWithPre(bloc.field,precessors)
     
    #StructRef
    elif (blocTyp == c_ast.Decl):
       precessors=visitSubBlocWithPre(bloc.init,precessors)

    #Return
    elif (blocTyp == c_ast.Return):
       precessors=visitSubBlocWithPre(bloc.expr,precessors)

    #Cast
    elif (blocTyp == c_ast.Cast):
       precessors=visitSubBlocWithPre(bloc.expr,precessors)

    #Switch
    elif (blocTyp == c_ast.Switch):
       precessors=visitSubBlocWithPre(bloc.cond,precessors)
       precessors=visitSubBlocWithPre(bloc.stmt,precessors)

    #Case
    elif (blocTyp == c_ast.Case):
       precessors=visitSubBlocWithPre(bloc.expr,precessors)
       stmtPre=visitSubBlocWithPre(bloc.stmts,precessors)
       precessors=list(set(precessors)|set(stmtPre))

    #ExprList
    elif (blocTyp == c_ast.ExprList):
       precessors=visitSubBlocWithPre(bloc.exprs,precessors)
       
    #TernaryOp
    elif (blocTyp == c_ast.TernaryOp):
        precessors=visitSubBlocWithPre(bloc.cond,precessors)  
        truePre=visitSubBlocWithPre(bloc.iftrue,precessors)
        flasePre=visitSubBlocWithPre(bloc.iffalse,precessors) 
        precessors=list(set(precessors)|set(truePre)|set(flasePre))

    #InitList
    elif (blocTyp == c_ast.InitList):
       precessors=visitSubBlocWithPre(bloc.exprs,precessors)

    #Label
    elif (blocTyp == c_ast.Label):
       precessors=visitSubBlocWithPre(bloc.stmt,precessors)

     
    #Typename
    elif (blocTyp == c_ast.Typename):
       precessors=visitSubBlocWithPre(bloc.name,precessors)

    #Default
    elif (blocTyp == c_ast.Default):
       precessors=visitSubBlocWithPre(bloc.stmts,precessors)

    elif (blocTyp == c_ast.ID or blocTyp == c_ast.Constant or blocTyp == c_ast.ArrayRef or str(blocTyp) == "<class 'NoneType'>" or blocTyp == c_ast.Continue or str(blocTyp) == "<class 'list'>" or blocTyp == c_ast.Goto or blocTyp == c_ast.Break or blocTyp == c_ast.EmptyStatement):
       temp=1
    


    else:
       print('unknow...')
       print(str(blocTyp))

    return precessors

#遍历函数体内部
def insideFunc(func):
     #func.show()
     funcContent = func.body
     if (funcContent.block_items is None):
         return
     i=0
     precessors=['f_entry()']
     for bloc in funcContent.block_items:
         #print('block %d' % (i))
         #print('pre:'+current)
         #bloc.show()
         #current = recursiveVistWithPrecessor(bloc,current)
         #print('father:'+father)
         #for bro in brothers:
         #   print('brother:'+bro)
         #bloc.show()
         precessors=recursiveVistWithPre(bloc,precessors)
         i=i+1
     #最后都链接到出口节点
     for pre in precessors:
         print('from:'+pre+',to:f_exit()')


def traverseFuc(func):
     #检查是否本文件内的函数
     fucPos = str(func.decl.coord)
     linePos = fucPos.find(':')
     fucFile = fucPos[0:linePos]
     lineNo = fucPos[linePos+1:]
     slashPos = fucFile.rfind('/')
     fucFile = fucFile[slashPos+1:]
     #if(fucFile=='<none>'):
     #print('fucFile:'+fucFile)
     if(fucFile==fullFileName):
        print('--------------Analysis-%s-@%s@line: %s.....' % (func.decl.name, fucFile, lineNo))
        #print('--------------Analysis %s at %s, line: %s.....' % (func.decl.name, fucFile, lineNo))
        insideFunc(func)
        print('---------------finish-------------------------------')



#参数1为要遍历到文件夹
if len(sys.argv) > 1:
   filename  = sys.argv[1]
        #print(filename)
else:
   filename = 'server_pp.c'

#获取原C程序文件名
dashPos = filename.rfind('_')
fullFileName = 'redis/src/'+filename[0:dashPos]+'.c'
slashPos = fullFileName.rfind('/')
fullFileName = fullFileName[slashPos+1:]

print('fullFileName:'+fullFileName)
ast = parse_file(filename, use_cpp=True, cpp_args=r'-Iutils/fake_libc_include')
#ast.show()

for decl in ast.ext:
  typ = type(decl)
  if(typ==c_ast.FuncDef):
     traverseFuc(decl)



