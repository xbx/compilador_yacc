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
from tabla_sim import TablaSim
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
    ###############################
    BNF y mapeo al codigo resultado
    Start Symbol: "programa"
    ###############################
"""
def p_programa(p):
    'programa : bloque_dec main'
    p[0] = get_nro_regla()
    crea_terceto(p[1], p[2])
    print 'programa : bloque_dec main - REGLA 1'
    # Traduccion a assembler aca

def p_bloque_dec(p):
    ('bloque_dec : PR_DEC DOS_PUNTOS '
        'ABRE_BLOQUE '
            'declaraciones '
        'CIERRA_BLOQUE '
     'PR_ENDEC FIN_LINEA ')
    p[0] = p[4]
    print ('bloque_dec : PR_DEC DOS_PUNTOS '
        'ABRE_BLOQUE '
            'declaraciones '
        'CIERRA_BLOQUE '
     'PR_ENDEC FIN_LINEA - REGLA 2')

def p_declaraciones(p):
    'declaraciones : declaracion FIN_LINEA declaraciones'
    p[0] = get_nro_regla()
    # aca actualizar la tabla de simbolos
    # No habria que crear tercetos
    crea_terceto(p[1], p[3])
    print 'declaraciones : declaracion FIN_LINEA declaraciones - REGLA 3'

def p_declaraciones_simple(p):
    'declaraciones : declaracion'
    p[0] = p[1]
    print 'declaraciones : declaracion - REGLA 3'

def p_declaracion(p):
    """
    declaracion : tipo_dato DOS_PUNTOS lista_ids
    """
    p[0] = get_nro_regla()
    crea_terceto(p[1], p[3])
    print 'declaracion : tipo_dato DOS_PUNTOS lista_ids - REGLA 4'

def p_lista_ids(p):
    """
    lista_ids : ID COMA lista_ids
    """
    p[0] = get_nro_regla()
    crea_terceto(p[1], p[3])
    print 'lista_ids : ID COMA lista_ids - REGLA 5'

def p_lista_ids_simple(p):
    """
    lista_ids : ID
    """
    p[0] = p[1]
    print 'lista_ids : ID - REGLA 5'

def p_main(p):
    """
    main : main bloque
    main : main funcion
    """
    p[0] = get_nro_regla()
    crea_terceto(p[1], p[2])
    print 'main : main bloque | main funcion - REGLA 6'

def p_main_simple(p):
    """
    main : bloque
    main : funcion
    """
    p[0] = p[1]
    
    print 'main : bloque | funcion - REGLA 7'

def p_funcion(p):
    ('funcion : '
        'PR_DEF ID DOS_PUNTOS tipo_dato '
            'ABRE_BLOQUE '
                'bloque_dec '
                'bloque '
            'CIERRA_BLOQUE '
        'PR_RETURN expresion FIN_LINEA'
     )
    p[0] = get_nro_regla()
    crea_terceto(p[2], p[4], p[6])
    print ('funcion : '
        'PR_DEF ID DOS_PUNTOS tipo_dato '
            'ABRE_BLOQUE '
                'bloque_dec '
                'bloque '
            'CIERRA_BLOQUE '
        'PR_RETURN expresion FIN_LINEA - REGLA 8')

def p_tipo_dato(p):
    """
    tipo_dato : PR_INT
    tipo_dato : PR_FLOAT
    tipo_dato : PR_STRING
    """
    p[0] = p[1]
    print 'tipo_dato : PR_INT | PR_FLOAT | PR_STRING - REGLA 9'

def p_bloque(p):
    """
    bloque : sentencia bloque
    """
    p[0] = get_nro_regla()
    crea_terceto(p[1], p[2])
    print 'bloque : sentencia bloque - REGLA 10'

def p_bloque_simple(p):
    """
    bloque : sentencia
    """
    p[0] = p[1]
    print 'bloque : sentencia - REGLA 10'

def p_sentencia(p):
    """
    sentencia : asig
    sentencia : sentencia_condicional
    sentencia : sentencia_while
    sentencia : sentencia_print
    sentencia : sentencia_percent
    """
    p[0] = p[1]
    print
    """
    sentencia : asig | sentencia_condicional | sentencia_while | sentencia_print | sentencia_percent | - REGLA 11
    """

def p_sentencia_sentencia(p):
    """
    sentencia : sentencia FIN_LINEA sentencia
    """
    p[0] = get_nro_regla()
    crea_terceto(p[1], p[3])
    print 'sentencia : sentencia FIN_LINEA sentencia - REGLA 11'

def p_sentencia_print(p):
    """
    sentencia_print : PR_PRINT ID
    """
    p[0] = get_nro_regla()
    print "sentencia_print : PR_PRINT ID - REGLA 12"  
    

def p_sentencia_while(p):
    """
    sentencia_while : PR_WHILE condicion DOS_PUNTOS ABRE_BLOQUE bloque CIERRA_BLOQUE
    """
    p[0] = get_nro_regla()
    # (while, condicion, bloque)
    crea_terceto(p[1], p[2], p[5])
    print 'sentencia_while : PR_WHILE condicion DOS_PUNTOS ABRE_BLOQUE bloque CIERRA_BLOQUE - REGLA 13'

def p_sentencia_condicional(p):
    'sentencia_condicional : PR_IF condicion DOS_PUNTOS ABRE_BLOQUE bloque CIERRA_BLOQUE'
    p[0] = get_nro_regla()
    # (if, condicion, bloque)
    crea_terceto(p[1], p[2], p[5])
    print 'sentencia_condicional : PR_IF condicion DOS_PUNTOS ABRE_BLOQUE bloque CIERRA_BLOQUE - REGLA 14'
    
def p_sentencia_percent(p):
    """
    sentencia_percent : PR_PERCENT factor COMA factor
    """
    p[0] = get_nro_regla()
    # ej: (percent, expresion, expresion)
    crea_terceto(p[1], p[2], p[4])
    print 'sentencia_percent : PR_PERCENT factor COMA factor - REGLA 15'

def p_asig(p):
    """
    asig : ID OP_AS expresion
    asig : ID OP_AS asig
    asig : ID OP_AS CTE_STRING
    """
    p[0] = get_nro_regla()
    # (=, ID, exp)
    crea_terceto(p[2], p[1], p[3])
    print ' asig : ID OP_AS expresion |  ID OP_AS asig | ID OP_AS CTE_STRING - REGLA 16'

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
    print  """
    condicion : expresion OP_MAYOR expresion | 
                expresion OP_MENOR expresion | 
                expresion OP_MENORIGUAL expresion | 
                expresion OP_DISTINTO expresion |
                condicion PR_AND condicion |
                condicion PR_OR condicion - REGLA 17
            """

def p_condicion_between(p):
    """
    condicion : factor PR_BETWEEN factor PR_AND factor
    """
    p[0] = get_nro_regla()
    # ej: (<, expresion, expresion)
    crea_terceto(p[2], p[1], p[3], p[5])
    print  'condicion : factor PR_BETWEEN factor PR_AND factor - REGLA 17'
    
def p_expresion(p):
    """
    expresion : expresion OP_SUMA termino
    expresion : expresion OP_RESTA termino
    expresion : expresion OP_MUL termino
    expresion : expresion OP_DIV termino
    """
    p[0] = get_nro_regla()
    # (+, exp, ter)
    crea_terceto(p[2], p[1], p[3])
    print 'expresion: expresion + termino | expresion - termino | expresion * termino | expresion / termino - REGLA 18'
    
def p_expression_term(p):
    'expresion : termino'
    p[0] = p[1]
    print 'expresion : termino - REGLA 18'
    
def p_term_factor(p):
    'termino : factor'
    p[0] = p[1]
    print 'termino : factor - REGLA 19'

def p_factor_parentesis(p):
    """
    factor : PAREN_ABRE expresion PAREN_CIERRA
    """
    p[0] = p[2]
    print 'factor : ( expresion ) - REGLA 20'

def p_factor(p):
    """
    factor : CTE_ENT
    factor : CTE_REAL
    factor : ID
    """
    p[0] = p[1]
    print 'factor : CTE_ENT | CTE_REAL | ID - REGLA 21'

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

#print "Tokens: "
result = yyparse.parse(fuente, lexer=yylex)
#if result is not None:
#    print "\nTercetos:\n"
#    for i, terceto in enumerate(tercetos):
#        print "%s: %s" % (i, terceto)
#else:
#    print "\nError!!"

# while True:
    # s = "2+3"
#    s = raw_input("test> ")
#    result = yyparse.parse(s, lexer=yylex)
#    print "resultado: ", result

