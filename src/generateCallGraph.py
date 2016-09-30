
from __future__ import print_function
import sys

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
       elif(nameTyp!=c_ast.UnaryOp and nameTyp!= c_ast.Cast):#pointer of function
          next=bloc.name.name+'()'+str(bloc.coord)
          #print('from:'+brother+',to:'+next)
          #print('Funcation Call: %s() at %s, nameTyp %s' % (bloc.name.name, bloc.coord, str(nameTyp)))
       elif(nameTyp==c_ast.UnaryOp or nameTyp== c_ast.Cast):
          next=''
       
       if(len(next)>0):
          for pre in precessors:
             print('from:'+pre+',to:'+next)
          #clear
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


    #binary op
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

#traverse the body of function
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
     #link to exit point
     for pre in precessors:
         print('from:'+pre+',to:f_exit()')


def traverseFuc(func):
     #check if the function is contained in the file
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



#the first argument is the input folder
if len(sys.argv) > 1:
   filename  = sys.argv[1]
        #print(filename)
else:
   filename = 'server_pp.c'

#get the name of c file
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



