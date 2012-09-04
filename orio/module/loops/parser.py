#!/usr/bin/env python

import sys, os
import orio.tool.ply.lex, orio.tool.ply.yacc
import orio.main.util.globals as g
import orio.module.loops.ast as ast

#----------------------------------------------------------------------------------------------------------------------
class LoopsLexer:

    def __init__(self):
        pass

    keywords = [
        'if', 'else', 'for', 'transform',
        'and', 'or', 'not'
    ]

    reserved = {}
    for k in keywords:
        reserved[k] = k.upper()
    
    tokens = list(reserved.values()) + [
        # literals (identifier, integer, float, string)
        'ID', 'ICONST', 'FCONST', 'SCONST',
        
        # operators (+,-,*,/,%,||,&&,!,<,<=,>,>=,==,!=)
        'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD',
        'LOR', 'LAND', 'LNOT',
        'LT', 'LE', 'GT', 'GE', 'EQ', 'NE',
    
        # assignment (=, *=, /=, %=, +=, -=)
        'EQUALS', 'TIMESEQUAL', 'DIVEQUAL', 'MODEQUAL', 'PLUSEQUAL', 'MINUSEQUAL',
    
        # increment/decrement (++,--)
        'PLUSPLUS', 'MINUSMINUS',
    
        # delimeters ( ) [ ] { } , ; :
        'LPAREN', 'RPAREN',
        'LBRACKET', 'RBRACKET',
        'LBRACE', 'RBRACE',
        'COMMA', 'SEMI', 'COLON', 'PERIOD',
        'LINECOMMENT'
    ]


    # A string containing ignored characters (spaces and tabs)
    t_ignore = ' \t'
    t_LINECOMMENT = r'[\#!][^\n\r]*'
    
    # operators
    t_LOR     = r'\|\|'
    t_LAND    = r'&&'
    t_LNOT    = r'!'
    t_LT      = r'<'
    t_GT      = r'>'
    t_LE      = r'<='
    t_GE      = r'>='
    t_EE      = r'=='
    t_NE      = r'!='
    
    # assignment operators
    t_EQ      = r'='
    t_MULTEQ  = r'\*='
    t_DIVEQ   = r'/='
    t_MODEQ   = r'%='
    t_PLUSEQ  = r'\+='
    t_MINUSEQ = r'-='
    
    # increment/decrement
    t_PP      = r'\+\+'
    t_MM      = r'--'
    
    literals = "+-*/%()[]{},;:'."

    # integer literal
    t_ICONST  = r'\d+'
    
    # floating literal
    t_FCONST  = r'((\d+)(\.\d*)([eE](\+|-)?(\d+))? | (\d+)[eE](\+|-)?(\d+))'
    
    # string literal
    t_SCONST  = r'\"([^\\\n]|(\\.))*?\"'
    
    def t_ID(self, t):
        r'[A-Za-z_]([A-Za-z0-9_\.]*[A-Za-z0-9_]+)*'
        t.type = self.reserved.get(t.value, 'ID')
        return t
    
    def t_NEWLINE(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)
    
    def t_error(self, t):
        g.err('orio.module.loops.lexer: illegal character (%s) at line %s' % (t.value[0], t.lexer.lineno))
    
    def build(self, **kwargs):
        self.lexer = orio.tool.ply.lex.lex(module=self, **kwargs)
    
    def test(self, data):
        self.lexer.input(data)
        while 1:
            tok = self.lexer.token()
            if not tok: break
            print tok
    
    def input(self, data):
        return self.lexer.input(data)
    
    def token(self):
        return self.lexer.token()
#----------------------------------------------------------------------------------------------------------------------



#----------------------------------------------------------------------------------------------------------------------
tokens = LoopsLexer.tokens
start = 'annotation'
__start_line_no = 1
#----------------------------------------------------------------------------------------------------------------------
def p_annotation(p):
    '''annotation : statements'''
    p[0] = p[1]

def p_statements_1(p):
    'statements : empty'
    p[0] = [p[1]]
    
def p_statements_2(p):
    '''statements : statements statement'''
    p[1].append(p[2])
    p[0] = p[1]
    
def p_statement(p):
    '''statement : line_comment
                 | expression_statement
                 | compound_statement
                 | conditional_statement
                 | iteration_statement
                 | transform_statement '''
    p[0] = p[1]

def p_line_comment(p):
    'line_comment : LINECOMMENT'
    p[0] = ast.Comment(p[1], p.lineno(1))

def p_expression_statement(p):
    '''expression_statement : expression_opt ';' '''
    p[0] = ast.ExpStmt(p[1], p.lineno(1))

def p_compound_statement(p):
    '''compound_statement : '{' statements '}' '''
    p[0] = ast.CompStmt(p[2], p.lineno(1))

def p_conditional_statement_1(p):
    '''conditional_statement : IF '(' expression ')' statement'''
    p[0] = ast.IfStmt(p[3], p[5], None, p.lineno(1))
    
def p_conditional_statement_2(p):
    '''conditional_statement : IF '(' expression ')' statement ELSE statement'''
    p[0] = ast.IfStmt(p[3], p[5], p[7], p.lineno(1))

def p_iteration_statement(p):
    '''iteration_statement : FOR '(' expression_opt ';' expression_opt ';' expression_opt ')' statement'''
    p[0] = ast.ForStmt(p[3], p[5], p[7], p[9], p.lineno(1))

def p_transform_statement(p):
    '''transform_statement : TRANSFORM ID '(' transform_args ')' statement'''
    p[0] = ast.TransformStmt(p[2], p[4], p[6], p.lineno(1))

def p_transform_args_1(p):
    '''transform_args : empty'''
    p[0] = [p[1]]

def p_transform_args_2(p):
    '''transform_args : transform_args ',' transform_arg'''
    p[1].append(p[3])
    p[0] = p[1]

def p_transform_arg(p):
    '''transform_arg : ID '=' expression'''
    p[0] = [p[1], p[3], p.lineno(1)]


#------------------------------------------------------------------------------
precedence = (
    ('left', ','),
    # throw
    ('left', 'EQ', 'EQPLUS', 'EQMINUS', 'EQMULT', 'EQDIV', 'EQMOD'), # <<, >>, &, |, ^
    # ?:
    ('left', 'LOR'),
    ('left', 'LAND'),
    # |
    # ^
    # &
    ('left', 'EE', 'NE'),
    ('left', 'LT', 'GT', 'LE', 'GE'),
    # <<, >>
    ('left', '+', '-'),
    ('left', '*', '/', '%'),
    ('right', 'LNOT', 'PP', 'MM', '+', '-', ), # ~, &, 
)

#------------------------------------------------------------------------------
def p_expression_opt_1(p):
    'expression_opt :'
    p[0] = None

def p_expression_opt_2(p):
    'expression_opt : expr'
    p[0] = p[1]

def p_expr_seq(p):
    '''expr : expr ',' expr'''
    p[0] = ast.BinOpExp(p[1], p[3], ast.BinOpExp.COMMA, p.lineno(1))

def p_expr_assign1(p):
    '''expr : expr '=' expr'''
    p[0] = ast.BinOpExp(ast.BinOpExp.EQ, p[1], p[3], p.lineno(1))

def p_expr_assign2(p):
    '''expr : expr MULTEQ expr'''
    p[0] = ast.BinOpExp(ast.BinOpExp.EQMULT, p[1], p[3], p.lineno(1))

def p_expr_assign3(p):
    '''expr : expr DIVEQ expr'''
    p[0] = ast.BinOpExp(ast.BinOpExp.EQDIV, p[1], p[3], p.lineno(1))

def p_expr_assign4(p):
    '''expr : expr MODEQ expr'''
    p[0] = ast.BinOpExp(ast.BinOpExp.EQMOD, p[1], p[3], p.lineno(1))

def p_expr_assign5(p):
    '''expr : expr PLUSEQ expr'''
    p[0] = ast.BinOpExp(ast.BinOpExp.EQPLUS, p[1], p[3], p.lineno(1))

def p_expr_assign6(p):
    '''expr : expr MINUSEQ expr'''
    p[0] = ast.BinOpExp(ast.BinOpExp.EQMINUS, p[1], p[3], p.lineno(1))

#------------------------------------------------------------------------------
def p_expr_log1(p):
    'expr : expr LOR expr'
    p[0] = ast.BinOpExp(ast.BinOpExp.LOR, p[1], p[3], p.lineno(1))

def p_expr_log2(p):
    'expr : expr LAND expr'
    p[0] = ast.BinOpExp(ast.BinOpExp.LAND, p[1], p[3], p.lineno(1))

#------------------------------------------------------------------------------
def p_expr_rel1(p):
    'expr : expr EE expr'
    p[0] = ast.BinOpExp(ast.BinOpExp.EE, p[1], p[3], p.lineno(1))

def p_expr_rel2(p):
    'expr : expr NE expr'
    p[0] = ast.BinOpExp(ast.BinOpExp.NE, p[1], p[3], p.lineno(1))

def p_expr_rel3(p):
    'expr : expr LT expr'
    p[0] = ast.BinOpExp(ast.BinOpExp.LT, p[1], p[3], p.lineno(1))

def p_expr_rel4(p):
    'expr : expr GT expr'
    p[0] = ast.BinOpExp(ast.BinOpExp.GT, p[1], p[3], p.lineno(1))

def p_expr_rel5(p):
    'expr : expr LE expr'
    p[0] = ast.BinOpExp(ast.BinOpExp.LE, p[1], p[3], p.lineno(1))

def p_expr_rel6(p):
    'expr : expr GE expr'
    p[0] = ast.BinOpExp(ast.BinOpExp.GE, p[1], p[3], p.lineno(1))

#------------------------------------------------------------------------------
def p_expr_add1(p):
    '''expr : expr '+' expr'''
    p[0] = ast.BinOpExp(ast.BinOpExp.PLUS, p[1], p[3], p.lineno(1))

def p_expr_add2(p):
    '''expr : expr '-' expr'''
    p[0] = ast.BinOpExp(ast.BinOpExp.MINUS, p[1], p[3], p.lineno(1))

#------------------------------------------------------------------------------
def p_expr_mult1(p):
    '''expr : expr '*' expr'''
    p[0] = ast.BinOpExp(ast.BinOpExp.MULT, p[1], p[3], p.lineno(1))

def p_expr_mult2(p):
    '''expr : expr '/' expr'''
    p[0] = ast.BinOpExp(ast.BinOpExp.DIV, p[1], p[3], p.lineno(1))

def p_expr_mult3(p):
    '''expr : expr '%' expr'''
    p[0] = ast.BinOpExp(ast.BinOpExp.MOD, p[1], p[3], p.lineno(1))

#------------------------------------------------------------------------------
def p_expr_pre1(p):
    'expr : PP expr'
    p[0] = ast.UnaryExp(ast.UnaryExp.PRE_INC, p[2], p.lineno(1))

def p_expr_pre2(p):
    'expr : MM expr'
    p[0] = ast.UnaryExp(ast.UnaryExp.PRE_DEC, p[2], p.lineno(1))

def p_expr_pre3(p):
    '''expr : '+' expr'''
    p[0] = ast.UnaryExp(ast.UnaryExp.PLUS, p[2], p.lineno(1))

def p_expr_pre4(p):
    '''expr : '-' expr'''
    p[0] = ast.UnaryExp(ast.UnaryExp.MINUS, p[2], p.lineno(1))

def p_expr_pre5(p):
    '''expr : LNOT expr'''
    p[0] = ast.UnaryExp(ast.UnaryExp.LNOT, p[2], p.lineno(1))

#------------------------------------------------------------------------------
def p_expr_arrayref(p):
    '''expr : expression '[' expression ']' '''
    p[0] = ast.ArrayRefExp(p[1], p[3], p.lineno(1))

def p_expr_funcall(p):
    '''expr : expression '(' arg_exprs ')' '''
    p[0] = ast.CallExp(p[1], p[3], p.lineno(1))

def p_arg_exprs_1(p):
    'arg_exprs : empty' 
    p[0] = [p[1]]

def p_arg_exprs_2(p):
    '''arg_exprs : arg_exprs ',' expr''' 
    p[1].append(p[3])
    p[0] = p[1]

#------------------------------------------------------------------------------
def p_expr_post1(p):
    'expr : expression PP'
    p[0] = ast.UnaryExp(ast.UnaryExp.POST_INC, p[1], p.lineno(1))

def p_expr_post2(p):
    'expr : expression MM'
    p[0] = ast.UnaryExp(ast.UnaryExp.POST_DEC, p[1], p.lineno(1))

def p_expr_primary1(p):
    'expr : ID'
    p[0] = ast.IdentExp(p[1], p.lineno(1))

def p_expr_primary2(p):
    'expr : ICONST'
    p[0] = ast.LitExp(ast.LitExp.INT, int(p[1]), p.lineno(1))

def p_expr_primary3(p):
    'expr : FCONST'
    p[0] = ast.LitExp(ast.LitExp.FLOAT, float(p[1]), p.lineno(1))

def p_expr_primary4(p):
    'expr : SCONST'
    p[0] = ast.LitExp(ast.LitExp.STRING, p[1], p.lineno(1))

def p_expr_primary5(p):
    '''expr : '(' expression ')' '''
    p[0] = ast.ParenExp(p[2], p.lineno(1))


#----------------------------------------------------------------------------------------------------------------------
# utility funs
# Compute column. 
#     input is the input text string
#     token is a token instance
def find_column(inputtxt,token):
    last_cr = inputtxt[:token.lexpos].rfind('\n') # count backwards until you reach a newline
    if last_cr < 0:
        last_cr = 0
    column = (token.lexpos - last_cr) + 1
    return column

def p_empty(p):
    'empty :'
    p[0] = []
#----------------------------------------------------------------------------------------------------------------------



#----------------------------------------------------------------------------------------------------------------------
def parse(start_line_no, text):

    # set the starting line number
    global __start_line_no
    __start_line_no = start_line_no

    l = LoopsLexer()
    l.build(debug=0, optimize=0)
    
    # Remove the old parse table
    parsetabfile = os.path.join(os.path.abspath('.'), 'parsetab_loops.py')
    try: os.remove(parsetabfile)
    except: pass
    
    parser = orio.tool.ply.yacc.yacc(debug=0, optimize=0, tabmodule='parsetab_loops', write_tables=0,
                                     outputdir=os.path.abspath('.'))
    theresult = parser.parse(text, lexer=l, debug=0)
    return theresult



#----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    for i in range(1, len(sys.argv)):
        #print "About to lex %s" % sys.argv[i]
        f = open(sys.argv[i], "r")
        s = f.read()
        f.close()
        #print "Contents of %s:\n%s" % (sys.argv[i], s)
        # Test the lexer; just print out all tokens founds
        #l.test(s)
        
        parse(s)
        print >>sys.stderr, '[parser] Successfully parsed %s' % sys.argv[i]


