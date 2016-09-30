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

# This is some C source to parse. Note that pycparser must begin
# at the top level of the C file, i.e. with either declarations
# or function definitions (this is called "external declarations"
# in C grammar lingo)
#
# Also, a C parser must have all the types declared in order to
# build the correct AST. It doesn't matter what they're declared
# to, so I've inserted the dummy typedef in the code to let the
# parser know Hash and Node are types. You don't need to do it
# when parsing real, correct C code.
#
'''
text = r"""
    typedef int Node, Hash;

    void HashPrint2(Hash* hash, void (*PrintFunc)(char*, char*))
    {
        unsigned int i;

        if (hash == NULL || hash->heads == NULL)
            return;

        for (i = 0; i < hash->table_size; ++i)
        {
            Node* temp = hash->heads[i];

            while (temp != NULL)
            {
                PrintFunc(temp->entry->key, temp->entry->value);
                temp = temp->next;
            }
        }
    }
"""
'''

text = r"""
    typedef int Node, Hash;

    void HashPrint2(Hash* hash, void (*PrintFunc)(char*, char*))
    {
        unsigned int i;
        i=i+1;

        if (printf("ddd") == printf("aaa") ){
           printf("adf");
           hash++;
        }
        else
           printf("bcd");
        

        for (i = 1; i < hash->table_size; ++i)
        {
            Node* temp = hash->heads[i];
            Node* temp2 = PrintFunc("adf");
            printf("adf");

            while (entry != NULL)
            {
                PrintFunc(temp->entry->key, temp->entry->value);
                temp = temp->next;
            }
        }
    }
"""

# Create the parser and ask to parse the text. parse() will throw
# a ParseError if there's an error in the code
#
parser = c_parser.CParser()
#filename = 'server_pp.c'
ast = parser.parse(text, filename='<none>')
#ast = parse_file(filename, use_cpp=True, cpp_args=r'-Iutils/fake_libc_include')

# Uncomment the following line to see the AST in a nice, human
# readable way. show() is the most useful tool in exploring ASTs
# created by pycparser. See the c_ast.py file for the options you
# can pass it.
#
#~ ast.show()
ast.show()
print('----------------------------------------------')

# OK, we've seen that the top node is FileAST. This is always the
# top node of the AST. Its children are "external declarations",
# and are stored in a list called ext[] (see _c_ast.cfg for the
# names and types of Nodes and their children).
# As you see from the printout, our AST has two Typedef children
# and one FuncDef child.
# Let's explore FuncDef more closely. As I've mentioned, the list
# ext[] holds the children of FileAST. Since the function
# definition is the third child, it's ext[2]. Uncomment the
# following line to show it:
#
#~ print('ast.ext[2].show()')
#~ ast.ext[2].show()

def visitSubBloc(sbloc):
    sblocTyp = type(sbloc)
    #print('block cond')
    #cond.show()
    if(sblocTyp == c_ast.Compound):
       for ssbloc in sbloc.block_items:
          recursiveVist(ssbloc)
    else:
       recursiveVist(sbloc)

#递归遍历bloc内部

def recursiveVist(bloc):
    #bloc.show()
    blocTyp = type(bloc)
    #print(blocTyp)
     
    if(blocTyp == c_ast.FuncCall):
       print('Funcation Call: %s() at %s' % (bloc.name.name, bloc.coord))

    elif (blocTyp == c_ast.If):
       visitSubBloc(bloc.cond)  
       visitSubBloc(bloc.iftrue)
       visitSubBloc(bloc.iffalse)  
       '''
       #条件分支
       cond = bloc.cond
       condTyp = type(cond)
       #print('block cond')
       #cond.show()
       if(condTyp == c_ast.Compound):
          for ssbloc in cond.block_items:
             recursiveVist(ssbloc)
       else:
          recursiveVist(cond)

       #true分支
       iftrue = bloc.iftrue
       trueTyp = type(iftrue)
       #print('block true')
       #iftrue.show()
       if(trueTyp == c_ast.Compound):
          for ssbloc in iftrue.block_items:
             recursiveVist(ssbloc)
       else:
          recursiveVist(iftrue)

       #false分支
       iffalse = bloc.iffalse
       falseTyp = type(iffalse)
       #print('block false')
       #iffalse.show()
       if(falseTyp == c_ast.Compound):
          for ssbloc in iffalse.block_items:
             recursiveVist(ssbloc)
       else:
          recursiveVist(iffalse)
       '''

    #二元操作
    elif (blocTyp == c_ast.BinaryOp):  
       visitSubBloc(bloc.left)  
       visitSubBloc(bloc.right)
       '''
       #左边
       left = bloc.left
       leftTyp = type(left)
       #print('block left')
       #left.show()
       if(leftTyp == c_ast.Compound):
          for ssbloc in left.block_items:
             recursiveVist(left)
       else:
          recursiveVist(left)
       #右边
       right = bloc.right
       rightTyp = type(right)
       #print('block right')
       #right.show()
       if(rightTyp == c_ast.Compound):
          for ssbloc in right.block_items:
             recursiveVist(right)
       else:
          recursiveVist(right)
      '''

    #for
    elif (blocTyp == c_ast.For):    
       visitSubBloc(bloc.init)
       visitSubBloc(bloc.cond)
       visitSubBloc(bloc.next)
       visitSubBloc(bloc.stmt)

    #Assignment
    elif (blocTyp == c_ast.Assignment):    
       visitSubBloc(bloc.lvalue)
       visitSubBloc(bloc.rvalue)
    
    #While
    elif (blocTyp == c_ast.While):    
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
       

    elif (blocTyp == c_ast.ID or blocTyp == c_ast.Constant or blocTyp == c_ast.ArrayRef or str(blocTyp) == "<class 'NoneType'>"):
      temp=1
    
    else:
       print('unknow...')
       print(str(blocTyp))
       bloc.show()


#遍历函数体内部
def insideFunc(func):
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
     #检查是否本文件内的函数
     fucPos = str(func.decl.coord)
     linePos = fucPos.find(':')
     fucFile = fucPos[0:linePos]
     lineNo = fucPos[linePos+1:]
     if(fucFile=='<none>'):
        print('Analysis %s at %s, line: %s' % (func.decl.name, fucFile, lineNo))
        insideFunc(func)
        print('----------------------------------------------')


#sast.ext[0].type.show()
#print(ast.ext[0].type)

for decl in ast.ext:
  typ = type(decl)
  if(typ==c_ast.FuncDef):
     traverseFuc(decl)


# A FuncDef consists of a declaration, a list of parameter
# declarations (for K&R style function definitions), and a body.
# First, let's examine the declaration.
#
#---function_decl = ast.ext[2].decl

# function_decl, like any other declaration, is a Decl. Its type child
# is a FuncDecl, which has a return type and arguments stored in a
# ParamList node
#~ print('function_decl.type.show()')
#~ function_decl.type.show()
#~ print('function_decl.type.args.show()')
#~ function_decl.type.args.show()

# The following displays the name and type of each argument:
#
#~ for param_decl in function_decl.type.args.params:
    #~ print('Arg name: %s' % param_decl.name)
    #~ print('Type:')
    #~ param_decl.type.show(offset=6)

# The body is of FuncDef is a Compound, which is a placeholder for a block
# surrounded by {} (You should be reading _c_ast.cfg parallel to this
# explanation and seeing these things with your own eyes).
# Let's see the block's declarations:
#
#---function_body = ast.ext[2].body

# The following displays the declarations and statements in the function
# body
#
#~ for decl in function_body.block_items:
    #~ decl.show()

# We can see a single variable declaration, i, declared to be a simple type
# declaration of type 'unsigned int', followed by statements.

# block_items is a list, so the third element is the For statement:
#
#---for_stmt = function_body.block_items[2]
#~ for_stmt.show()

# As you can see in _c_ast.cfg, For's children are 'init, cond,
# next' for the respective parts of the 'for' loop specifier,
# and stmt, which is either a single stmt or a Compound if there's
# a block.
#
# Let's dig deeper, to the while statement inside the for loop:
#
#---while_stmt = for_stmt.stmt.block_items[1]
#~ while_stmt.show()

# While is simpler, it only has a condition node and a stmt node.
# The condition:
#
#---while_cond = while_stmt.cond
#~ while_cond.show()

# Note that it's a BinaryOp node - the basic constituent of
# expressions in our AST. BinaryOp is the expression tree, with
# left and right nodes as children. It also has the op attribute,
# which is just the string representation of the operator.
#
#~ print(while_cond.op)
#~ while_cond.left.show()
#~ while_cond.right.show()

#
# That's it for the example. I hope you now see how easy it is to explore the
# AST created by pycparser. Although on the surface it is quite complex and has
# a lot of node types, this is the inherent complexity of the C language every
# parser/compiler designer has to cope with.
# Using the tools provided by the c_ast package it's easy to explore the
# structure of AST nodes and write code that processes them.
# Specifically, see the cdecl.py example for a non-trivial demonstration of what
# you can do by recursively going through the AST.
#


