#-----------------------------------------------------------------
# pycparser: explore_ast.py
#

from __future__ import print_function
import sys

sys.path.extend(['.', '..'])

from pycparser import c_parser, c_ast, parse_file


def visitSubBloc(sbloc):
    if (sbloc is None):
       return
    sblocTyp = type(sbloc)
    #print(sblocTyp)
    if(sblocTyp == c_ast.Compound and sbloc.block_items is not None):
       for ssbloc in sbloc.block_items:
          recursiveVist(ssbloc)
    else:
       recursiveVist(sbloc)

#traverse inside the bloc
def recursiveVist(bloc):
    if (bloc is None):
       return
    #print('begin current block...')
    #bloc.show()
    #print('end current block...')
    blocTyp = type(bloc)
    #print(blocTyp)
     
    if(blocTyp == c_ast.FuncCall):
       nameBloc = bloc.name
       nameTyp=type(nameBloc)
       #bloc.show()
       if(nameTyp == c_ast.StructRef):
          subNameBloc = bloc.name.field
          subNameTyp=type(subNameBloc)
          if(subNameTyp == c_ast.StructRef):
             print('Funcation Call: %s() at %s, nameTyp %s' % (subNameBloc.field.name, bloc.coord, str(nameTyp)))     
          else:
             print('Funcation Call: %s() at %s, nameTyp %s' % (bloc.name.field.name, bloc.coord, str(nameTyp)))       
       elif(nameTyp!=c_ast.UnaryOp and nameTyp!= c_ast.Cast):#pointer of function
          print('Funcation Call: %s() at %s, nameTyp %s' % (bloc.name.name, bloc.coord, str(nameTyp)))
       #if(str(bloc.coord).find('redis/src/object.c')>-1):
       #   bloc.show()

    #if
    elif (blocTyp == c_ast.If):
       #print('begin show if block...')
       #bloc.show()
       #print('begin cond block...')
       visitSubBloc(bloc.cond)  
       #print('begin iftrue block...')
       visitSubBloc(bloc.iftrue)
       #print('begin iffalse block...')
       visitSubBloc(bloc.iffalse)  
       #print('end iffalse block...')
      
    #binary op
    elif (blocTyp == c_ast.BinaryOp):  
       visitSubBloc(bloc.left)  
       visitSubBloc(bloc.right)
      

    #for
    elif (blocTyp == c_ast.For):    
       visitSubBloc(bloc.init)
       visitSubBloc(bloc.cond)
       visitSubBloc(bloc.next)
       visitSubBloc(bloc.stmt)

    #Assignment
    elif (blocTyp == c_ast.Assignment):
       #print('begin Assignment block...')
       #bloc.show()    
       #print('end Assignment block...')
       visitSubBloc(bloc.lvalue)
       #print('begin Assignment lvalue block...')
       #bloc.lvalue.show()    
       #print('end Assignment lvalue block...')
       visitSubBloc(bloc.rvalue)
       #print('begin Assignment rvalue block...')
       #bloc.rvalue.show()    
       #print('end Assignment rvalue block...')
    
    #While
    elif (blocTyp == c_ast.While):    
       visitSubBloc(bloc.cond)
       visitSubBloc(bloc.stmt)
    
    #DoWhile
    elif (blocTyp == c_ast.DoWhile):    
       visitSubBloc(bloc.cond)
       visitSubBloc(bloc.stmt)

    #UnaryOp
    elif (blocTyp == c_ast.UnaryOp):
      visitSubBloc(bloc.expr)
     
    #StructRef
    elif (blocTyp == c_ast.StructRef):
      visitSubBloc(bloc.name)
      visitSubBloc(bloc.field)
     
    #StructRef
    elif (blocTyp == c_ast.Decl):
      visitSubBloc(bloc.init)

    #Return
    elif (blocTyp == c_ast.Return):
      visitSubBloc(bloc.expr)

    #Cast
    elif (blocTyp == c_ast.Cast):
      visitSubBloc(bloc.expr)

    #Switch
    elif (blocTyp == c_ast.Switch):
      visitSubBloc(bloc.cond)
      visitSubBloc(bloc.stmt)

    #Case
    elif (blocTyp == c_ast.Case):
      visitSubBloc(bloc.expr)
      visitSubBloc(bloc.stmts)

    #ExprList
    elif (blocTyp == c_ast.ExprList):
      visitSubBloc(bloc.exprs)
       
    #TernaryOp
    elif (blocTyp == c_ast.TernaryOp):
       #print('begin TernaryOp block...')
       #bloc.show()    
       #print('end TernaryOp block...')
       visitSubBloc(bloc.cond)  
       visitSubBloc(bloc.iftrue)
       visitSubBloc(bloc.iffalse) 

    #InitList
    elif (blocTyp == c_ast.InitList):
      visitSubBloc(bloc.exprs)

    #Label
    elif (blocTyp == c_ast.Label):
      visitSubBloc(bloc.stmt)

     
    #Typename
    elif (blocTyp == c_ast.Typename):
      visitSubBloc(bloc.name)

    #Default
    elif (blocTyp == c_ast.Default):
      visitSubBloc(bloc.stmts)


    elif (blocTyp == c_ast.ID or blocTyp == c_ast.Constant or blocTyp == c_ast.ArrayRef or str(blocTyp) == "<class 'NoneType'>" or blocTyp == c_ast.Continue or str(blocTyp) == "<class 'list'>" or blocTyp == c_ast.Goto or blocTyp == c_ast.Break or blocTyp == c_ast.EmptyStatement):
      temp=1
    
    else:
       print('unknow...')
       print(str(blocTyp))
       #bloc.show()

#traverse inside function body
def insideFunc(func):
     #func.show()
     funcContent = func.body
     if (funcContent.block_items is None):
         return
     i=0
     for bloc in funcContent.block_items:
         #print('block %d' % (i))
         recursiveVist(bloc)
         i=i+1
     #firstBloc = funcContent.block_items[0]
     #firstBlocTyp = type(firstBloc)
     #print(firstBlocTyp)
     #print(firstBloc.children())
     #for bloc in firstBloc.children():
     #    bloc.show()
     #if(firstBlocTyp==c_ast.Decl):
         #childrenList = firstBloc.children()
         #childrenList.show()
         #for child in childrenList:
          #   child.show()

def traverseFuc(func):
     #check if the function is contained in this file
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
        insideFunc(func)
        print('---------------finish-------------------------------')




if len(sys.argv) > 1:
        filename  = sys.argv[1]
        #print(filename)
else:
        print('input file is not provided')

#get the file name of c programs
print('filename:'+filename)
dashPos = filename.rfind('_')
fullFileName = 'lua/src/'+filename[0:dashPos]+'.c'
slashPos = fullFileName.rfind('/')
fullFileName = fullFileName[slashPos+1:]

print('fullFileName:'+fullFileName)
ast = parse_file(filename, use_cpp=True, cpp_args=r'-Iutils/fake_libc_include')
#ast.show()

for decl in ast.ext:
  typ = type(decl)
  if(typ==c_ast.FuncDef):
     traverseFuc(decl)



