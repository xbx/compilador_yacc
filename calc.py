# Yacc example
tokens = (
   'NUMBER',
   'PLUS',
   'MINUS',
   'TIMES',
   'DIVIDE',
   'LPAREN',
   'RPAREN',
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
    def input(self, text):
        self.text = text
        self.generator = self.generate()

    def generate(self):
        for input_char in self.text:


            """
            Aca hacer el automata que devuelve el token y su valor
            Por ahora esto solo reconoce numeros de 1 digito y "+"
            """
            if input_char == '+':
                yield Token('PLUS', input_char)
            elif input_char.isdigit:
                yield Token('NUMBER', int(input_char))
            """
            """

    def token(self):
        try:
            token = self.generator.next()
            print token
            return token
        except StopIteration:
            return None


import ply.yacc as yacc


"""
    BNF y mapeo al codigo resultado
"""
def p_expression_plus(p):
    'expression : expression PLUS term'
    p[0] = p[1] + p[3]

def p_expression_minus(p):
    'expression : expression MINUS term'
    p[0] = p[1] - p[3]

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_times(p):
    'term : term TIMES factor'
    p[0] = p[1] * p[3]

def p_term_div(p):
    'term : term DIVIDE factor'
    p[0] = p[1] / p[3]

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_num(p):
    'factor : NUMBER'
    p[0] = p[1]

def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]

# Error rule for syntax errors
def p_error(p):
    print "Syntax error in input!"

# Build the parser

yyparse = yacc.yacc()
yylex = Lexer()

while True:
    s = raw_input("calc> ")

    result = yyparse.parse(s, lexer=yylex)
    print "resultado: ", result

