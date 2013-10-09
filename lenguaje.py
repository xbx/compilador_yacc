"""
Universidad Nacional de La Matanza
Catedra Lenguajes y Compiladores - 2013
Mariano Francischini, Alejandro Giorgi, Roberto Bravo

TP Compilador
Basado en PLY (Python Lex-Yacc)
    http://www.dabeaz.com/ply/
    Ej: http://www.dalkescientific.com/writings/NBN/parsing_with_ply.html
"""
import ply.yacc as yacc
from lexer import Lexer, tokens

def concatena(lista):
    """
    Test. Por ahora concatena los operandos como string en vez
    de generar codigo (tercetos)
    """
    string = ""
    for item in lista[1:]:
        string += str(item)
    return string


"""
    BNF y mapeo al codigo resultado
"""
def p_programa(p):
    'programa : bloque'
    p[0] = concatena(p)

def p_bloque(p):
    """
    bloque : sentencia bloque
    bloque : sentencia
    """
    p[0] = concatena(p)

def p_sentencia(p):
    """
    sentencia : asig
    sentencia : sentencia_condicional
    sentencia : sentencia FIN_LINEA sentencia
    """
    p[0] = concatena(p)

def p_sentencia_condicional(p):
    'sentencia_condicional : PR_IF PAREN_ABRE condicion PAREN_CIERRA DOS_PUNTOS ABRE_BLOQUE bloque CIERRA_BLOQUE'
    p[0] = concatena(p)

def p_asig(p):
    """
    asig : ID OP_AS expresion
    asig : ID OP_AS asig
    """
    p[0] = concatena(p)

def p_condicion(p):
    """
    condicion : ID OP_MAYOR ID
    condicion : ID OP_MENOR ID
    condicion : condicion PR_AND condicion
    condicion : condicion PR_OR condicion
    """
    p[0] = concatena(p)

def p_expresion(p):
    'expresion : expresion OP_SUMA termino'
    # p[0] = p[1] + p[3]
    p[0] = concatena(p)

def p_expression_term(p):
    'expresion : termino'
    p[0] = concatena(p)

def p_term_factor(p):
    'termino : factor'
    p[0] = concatena(p)

def p_factor(p):
    """
    factor : CTE_ENT
    factor : ID
    """
    p[0] = concatena(p)

# Error rule for syntax errors
def p_error(p):
    raise TypeError("unknown text at %r" % (p.value,))

# Build the parser

yyparse = yacc.yacc(debug=1)
yylex = Lexer()

fuente = open("fuente.zz").read()

print "Tokens: "
result = yyparse.parse(fuente, lexer=yylex)
if result is not None:
    print "\nResultado:\n", result
else:
    print "\nError!!"

# while True:
    # s = "2+3"
#    s = raw_input("test> ")
#    result = yyparse.parse(s, lexer=yylex)
#    print "resultado: ", result

