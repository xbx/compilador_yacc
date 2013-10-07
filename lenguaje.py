"""
Universidad Nacional de La Matanza
Catedra Lenguajes y Compiladores - 2013
Mariano Francischini, Alejandro Giorgi, Roberto Bravo

TP Compilador
Basado en PLY (Python Lex-Yacc)
    http://www.dabeaz.com/ply/
    Ej: http://www.dalkescientific.com/writings/NBN/parsing_with_ply.html
"""
import re
import ply.yacc as yacc
from collections import OrderedDict

tokens = (
   'ID',
   'OP_AS',
   'OP_SUMA',
   'CTE_ENT',
   'END_LINE',
   'ABRE_BLOQUE',
   'CIERRA_BLOQUE',
   'PR_IF',
   'DOS_PUNTOS'
)

ESTADO_END_LINE = "2"

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value
        self.lineno = None
        self.lexpos = None
    def __repr__(self):
        return "<Token: %s, %s>" % (self.type, self.value.strip("\n"))


class Lexer(object):
    """
    YYLEX
    Analizador Lexico.
    Automata finito de Terminales
    """
    def __init__(self):
        self.estado_final = 'F'
        self.nivel_bloque_actual = 0  # Nivel de tab del bloque actual
        self.nivel_bloque_sentencia = 0  # Nivel de tab de la sentencia actual

        """
        Sintaxis:
        ("<caracter>", ["<nuevo_estado>", '<token>', '<caracter_excepto>', <funcion>]),
        """
        self.matriz = {
            "0": OrderedDict([
                ('\+', ["10", '', '', self.acc_NADA]),
                ("=", ["17", '', '', self.acc_NADA]),
                ("[0-9]", ["20", '', '', self.acc_NADA]),
                ("[a-zA-Z]", ["1", '', '', self.acc_NADA]),
                ('\n', [ESTADO_END_LINE, '', '', self.acc_NADA]),
                (':', ["3", '', '', self.acc_NADA]),
                ('#', ["4", '', '', self.acc_NADA]),

            ]),
            "1": OrderedDict([
                ("[a-zA-Z0-9]", ["1", '', '', self.acc_NADA]),
                ("CUALQUIER", ["F", "ID", '', self.acc_NADA]),
            ]),
            "2": OrderedDict([
                (" ", [ESTADO_END_LINE, '', '', self.acc_END_LINE]),
                (".", ["F", '', '', self.acc_END_LINE]),  # especial, termina indentacion ".": cualquier caracter
            ]),
            "3": OrderedDict([
                ("CUALQUIER", ["F", "DOS_PUNTOS", '', self.acc_NADA]),
            ]),
            "4": OrderedDict([
                ('#', ["5", '', '', self.acc_NADA]),
            ]),
            "5": OrderedDict([
                ("\n", ["F", "COMENTARIO", '\n', self.acc_COMENTARIO]),
                (".", ["5", "", '\n', self.acc_NADA]),
            ]),
            "10": OrderedDict([
                ("CUALQUIER", ["F", "OP_SUMA", '', self.acc_NADA]),
            ]),
            "17": OrderedDict([
                ("CUALQUIER", ["F", "OP_AS", "=", self.acc_NADA]),
            ]),
            "20": OrderedDict([
                ("[0-9]", ["20"]),
                ("CUALQUIER", ["F", "CTE_ENT", "\.", self.acc_NADA]),
            ]),
        }


    def input(self, text):
        """ Metodo requerido por yyparse """
        self.text = text + "\n"
        self.generate = self.generator()

    def iterar_estado(self, estado_actual, input_char):
        for (simbolo, accion) in estado_actual.items():
            if simbolo == "CUALQUIER":
                self.estado = "0"
                return Token(type=accion[1], value=self.cadena[0:-1])
            elif re.match(simbolo, input_char) is not None:
                resultado = accion[3](simbolo)
                if resultado is not None:
                    self.estado = "0"
                    return resultado
                self.estado = accion[0]
                return "NEXT"
        return  Token(type="$end", value="")

    def generator(self):
        """
            Automata
        """
        self.estado = "0"
        self.cadena = ""
        i = 0

        yield Token(type="ABRE_BLOQUE", value="0")

        while i < len(self.text):
            """ Itera caracter por caracter """
            input_char = self.text[i]
            if self.estado != ESTADO_END_LINE and input_char == " ":
                i += 1
                continue
            self.cadena += input_char
            estado_actual = self.matriz[self.estado]

            """ Avanza por la matriz de estados """
            token = self.iterar_estado(estado_actual, input_char)
            if token == "NEXT":
                i += 1
                continue

            if token == "IGNORE":
                i += 1
                self.cadena = ""
                continue

            if token.type == 'ID':
                "ID's: Casos especiales, palabras reservadas"
                if token.value == 'if':
                    token = Token(type="PR_IF", value="if")

            yield token
            self.cadena = ""
        yield Token(type="CIERRA_BLOQUE", value="0")

    def token(self):
        try:
            token = self.generate.next()
            print token
            return token
        except StopIteration:
            return None

    """
        Metodos de acciones ejecutadas en cada estado del automata
    """
    def acc_NADA(self, simbolo):
        pass
    def acc_END_LINE(self, simbolo):
        if simbolo == " ":  # Bloque (tab)
            self.nivel_bloque_sentencia += 1
        else:

            if self.nivel_bloque_actual < self.nivel_bloque_sentencia:
                self.nivel_bloque_actual = self.nivel_bloque_sentencia  # cambia bloque
                token = Token(type="ABRE_BLOQUE", value="%s" % self.nivel_bloque_actual)
            elif self.nivel_bloque_actual > self.nivel_bloque_sentencia:
                self.nivel_bloque_actual = self.nivel_bloque_sentencia  # cambia bloque
                token = Token(type="CIERRA_BLOQUE", value="%s" % self.nivel_bloque_actual)
            else:
                token = Token(type="END_LINE", value="\n")  # Se ignoran los epacios de tabulacion
                                                            # si no cambian el bloque
            self.nivel_bloque_sentencia = 0  # Reset nivel
            return token
        return None
    def acc_COMENTARIO(self, simbolo):
        return "IGNORE"

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
    'bloque : ABRE_BLOQUE sentencias CIERRA_BLOQUE'
    'bloque : END_LINE bloque'
    indent = '\n' + '>' * int(p[1])
    sentencias = indent.join(p[2].split("\n"))
    p[0] = indent + sentencias

def p_sentencias(p):
    """
    sentencias : sentencias sentencia
    sentencias : sentencia
    """
    p[0] = concatena(p)

def p_sentencia(p):
    """
    sentencia : asig
    sentencia : sentencia_condicional
    sentencia : sentencia END_LINE sentencia
    """
    p[0] = concatena(p)

def p_sentencia_condicional(p):
    'sentencia_condicional : PR_IF DOS_PUNTOS bloque'
    p[0] = concatena(p)

def p_asig(p):
    """
    asig : ID OP_AS expresion
    asig : ID OP_AS asig
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

