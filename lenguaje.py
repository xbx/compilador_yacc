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
import sys

def concatena(lista):
    """
    Test. Por ahora concatena los operandos como string en vez
    de generar codigo (tercetos)
    """
    string = ""
    for item in lista[1:]:
        string += str(item)
    return string

tercetos = []

def crea_terceto(*args):
    """ Crea y agrega un terceto (string) a la lista """
    tercetos.append("(%s)" % ", ".join(args))

nro_regla = 0
def get_nro_regla():
    """ Contador de numero de regla 'actual'. Incrementa a medida que se crean"""
    global nro_regla
    regla = "[%s]" % nro_regla
    nro_regla += 1
    return regla

"""
    BNF y mapeo al codigo resultado
"""
def p_programa(p):
    'programa : bloque'
    p[0] = get_nro_regla()
    crea_terceto(p[1])

def p_bloque(p):
    """
    bloque : sentencia bloque
    """
    p[0] = get_nro_regla()
    crea_terceto(p[1], p[2])

def p_bloque_simple(p):
    """
    bloque : sentencia
    """
    p[0] = get_nro_regla()
    crea_terceto(p[1])

def p_sentencia(p):
    """
    sentencia : asig
    sentencia : sentencia_condicional
    sentencia : sentencia_while
    """
    p[0] = get_nro_regla()
    crea_terceto(p[1])

def p_sentencia_sentencia(p):
    """
    sentencia : sentencia FIN_LINEA sentencia
    """
    p[0] = get_nro_regla()
    crea_terceto(p[1], p[3])

def p_sentencia_while(p):
    'sentencia_while : PR_WHILE PAREN_ABRE condicion PAREN_CIERRA DOS_PUNTOS ABRE_BLOQUE bloque CIERRA_BLOQUE'
    p[0] = get_nro_regla()
    # (while, condicion, bloque)
    crea_terceto(p[1], p[3], p[7])


def p_sentencia_condicional(p):
    'sentencia_condicional : PR_IF PAREN_ABRE condicion PAREN_CIERRA DOS_PUNTOS ABRE_BLOQUE bloque CIERRA_BLOQUE'
    p[0] = get_nro_regla()
    # (if, condicion, bloque)
    crea_terceto(p[1], p[3], p[7])

def p_asig(p):
    """
    asig : ID OP_AS expresion
    asig : ID OP_AS asig
    """
    p[0] = get_nro_regla()
    # (=, ID, exp)
    crea_terceto(p[2], p[1], p[3])

def p_condicion(p):
    """
    condicion : expresion OP_MAYOR expresion
    condicion : expresion OP_MENOR expresion
    condicion : expresion OP_MENORIGUAL expresion
    condicion : expresion OP_DISTINTO expresion
    condicion : condicion PR_AND condicion
    condicion : condicion PR_OR condicion
    """
    p[0] = get_nro_regla()
    # ej: (<, expresion, expresion)
    crea_terceto(p[2], p[1], p[3])

def p_expresion(p):
    'expresion : expresion OP_SUMA termino'
    p[0] = get_nro_regla()
    # (+, exp, ter)
    crea_terceto(p[2], p[1], p[3])

def p_expression_term(p):
    'expresion : termino'
    p[0] = get_nro_regla()
    crea_terceto(p[1])

def p_term_factor(p):
    'termino : factor'
    p[0] = get_nro_regla()
    crea_terceto(p[1])

def p_factor(p):
    """
    factor : CTE_ENT
    factor : ID
    """
    p[0] = get_nro_regla()
    crea_terceto(p[1])

# Error rule for syntax errors
def p_error(p):
    raise TypeError("Syntax error: %s" % str(p))

# Build the parser

yyparse = yacc.yacc(debug=1)
yylex = Lexer()

try:
    filename = sys.argv[1]
except:
    filename = "fuente.zz"
fuente = open(filename).read()

print "Tokens: "
result = yyparse.parse(fuente, lexer=yylex)
if result is not None:
    print "\nTercetos:\n"
    for i, terceto in enumerate(tercetos):
        print "%s: %s" % (i, terceto)
else:
    print "\nError!!"

# while True:
    # s = "2+3"
#    s = raw_input("test> ")
#    result = yyparse.parse(s, lexer=yylex)
#    print "resultado: ", result

