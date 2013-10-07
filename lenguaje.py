"""
Universidad Nacional de La Matanza
Catedra Lenguajes y Compiladores - 2013
Mariano Francischini, Alejandro Giorgi, Roberto Bravo
TP Compilador
"""
import re
import ply.yacc as yacc

tokens = (
   'ID',
   'OP_AS',
   'OP_SUMA',
   'CTE_ENT',
)

i = 0

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value
        self.lineno = None
        self.lexpos = i+1
    def __repr__(self):
        return "<Token: %s, %s>" % (self.type, self.value)


class Lexer(object):
    """
    YYLEX
    Analizador Lexico.
    Automata finito de Terminales
    """
    def __init__(self):
        self.texto_pos = 0
        self.estado_final = 'F'

        """
            Sintaxis:
            "<caracter>": [NUEVO_ESTADO, TOKEN, EXCEPTO]
        """
        self.matriz = {
                "0": {
                    "\+": ["9"],
                    "=": ["17"],
                    "[0-9]": ["20"],
                },
                "10": {
                    "CUALQUIER": ["F", "OP_SUMA"],
                },
                "17": {
                    "CUALQUIER": ["F", "OP_AS", "="],
                },
                "20": {
                    "[0-9]": ["20"],
                    "CUALQUIER": ["F","CTE_ENT", "\."],
                },
        }


    def input(self, text):
        self.text = text
        self.texto_pos = 0
        self.generator = self.generate()

    def generate(self):
        self.estado = "0"
        cadena = ""
        import ipdb
        ipdb.set_trace()
        for input_char in self.text[self.texto_pos:]:
            self.texto_pos += 1
            cadena += input_char
            """
            Aca hacer el automata que devuelve el token y su valor
            Por ahora esto solo reconoce numeros de 1 digito y "+"
            """
            estado_actual = self.matriz[self.estado]
            for (simbolo, accion) in estado_actual.items():
                estado_actual = self.matriz[self.estado]
                if simbolo == "CUALQIUER":
                    yield Token(accion[1], cadena)
                if re.match(simbolo, input_char) is not None:
                    self.estado = accion[0]
            """
            if input_char == '+':
                yield Token('OP_SUMA', input_char)
            elif input_char == '=':
                yield Token('OP_AS', input_char)
            elif input_char.isalpha():
                yield Token('ID', input_char)
            elif input_char.isdigit():
                yield Token('CTE_ENT', input_char)
            """

    def token(self):
        try:
            token = self.generator.next()
            print token
            return token
        except StopIteration:
            return None



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
    print "Syntax error in input!"

# Build the parser

yyparse = yacc.yacc(debug=1)
yylex = Lexer()

while True:
    s = raw_input("test> ")

    result = yyparse.parse(s, lexer=yylex)
    print "resultado: ", result

