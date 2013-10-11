"""
Universidad Nacional de La Matanza
Catedra Lenguajes y Compiladores - 2013
Mariano Francischini, Alejandro Giorgi, Roberto Bravo

TP Compilador - Analizador Lexico
"""
import re
from collections import OrderedDict

tokens = [
   'ID',
   'OP_AS',
   'OP_SUMA',
   'PR_WHILE',
   'OP_DISTINTO',
   'CTE_ENT',
   'FIN_LINEA',
   'ABRE_BLOQUE',
   'CIERRA_BLOQUE',
   'PR_IF',
   'DOS_PUNTOS',
   'OP_MAYOR',
   'OP_MENOR',
   'OP_MENORIGUAL',
   'PR_AND',
   'PR_OR',
   'PAREN_ABRE',
   'PAREN_CIERRA',
]

ESTADO_FIN_LINEA = "2"

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value
        self.lineno = None
        self.lexpos = None
    def __repr__(self):
        return "<Token: %s, %s>" % (self.type, self.value.strip("\n"))

class Val(object):
    """ Reg Exps """
    CUALQUIER = "."
    
    """ Estados automata """
    E_FINAL = "F"

class Lexer(object):
    """
    YYLEX
    Analizador Lexico.
    Automata finito de Terminales
    """
    def __init__(self):
        self.nivel_bloques = [0]  # Nivel de tab del bloque actual
        self.nivel_espacios_sentencia = 0  # Nivel de tab de la sentencia actual
        
        """Cuando se descubren varios tokens juntos se los envia \
           a esta cola para irlos devolviendo en sucesivas llamadas
        """
        self.cola_tokens = []
         
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
                ('\n', [ESTADO_FIN_LINEA, '', '', self.acc_RESET_NIVEL_SENTENCIA]),
                (':', ["3", '', '', self.acc_NADA]),
                ('#', ["4", '', '', self.acc_NADA]),
                
                ('>', ["6", '', '', self.acc_NADA]),
                ('<', ["7", '', '', self.acc_NADA]),
                ('&', ["8", '', '', self.acc_NADA]),
                ('\|', ["9", '', '', self.acc_NADA]),
                
                ('\(', ["11", '', '', self.acc_NADA]),
                ('\)', ["12", '', '', self.acc_NADA]),

            ]),
            "1": OrderedDict([
                ("[a-zA-Z0-9]", ["1", '', '', self.acc_NADA]),
                (Val.CUALQUIER, [Val.E_FINAL, "ID", '', self.acc_NADA]),
            ]),
            "2": OrderedDict([
                (" ", [ESTADO_FIN_LINEA, '', '', self.acc_FIN_LINEA]),
                (Val.CUALQUIER, ["X", '', '', self.acc_FIN_LINEA]),  # especial, termina indentacion ".": cualquier caracter
            ]),
            "3": OrderedDict([
                (Val.CUALQUIER, [Val.E_FINAL, "DOS_PUNTOS", '', self.acc_NADA]),
            ]),
            "4": OrderedDict([
                ('#', ["5", '', '', self.acc_NADA]),
            ]),
            "5": OrderedDict([
                ("\n", ["X", "COMENTARIO", '', self.acc_COMENTARIO]),
                (Val.CUALQUIER, ["5", "", '\n', self.acc_NADA]),
            ]),
                       
            "6": OrderedDict([
                (Val.CUALQUIER, ["F", 'OP_MAYOR', '', self.acc_NADA]),
            ]),
            "7": OrderedDict([
                ('>', ["13", "", '', self.acc_NADA]),
                ('=', ["14", "", '', self.acc_NADA]),
                (Val.CUALQUIER, ["F", 'OP_MENOR', '', self.acc_NADA]),

            ]),
            "8": OrderedDict([
                ('&', ["F", 'PR_AND', '', self.acc_NADA]),
            ]),
            "9": OrderedDict([
                ('|', ["F", 'PR_OR', '', self.acc_NADA]),
            ]),
                       
            "10": OrderedDict([
                (Val.CUALQUIER, [Val.E_FINAL, "OP_SUMA", '', self.acc_NADA]),
            ]),
                       
            "11": OrderedDict([
                (Val.CUALQUIER, ["F", 'PAREN_ABRE', '', self.acc_NADA]),
            ]),
            "12": OrderedDict([
                (Val.CUALQUIER, ["F", 'PAREN_CIERRA', '', self.acc_NADA]),
            ]),

            "13": OrderedDict([
                (Val.CUALQUIER, ["F", 'OP_DISTINTO', '', self.acc_NADA]),
            ]),

            "14": OrderedDict([
                (Val.CUALQUIER, ["F", 'OP_MENORIGUAL', '', self.acc_NADA]),
            ]),
                       
            "17": OrderedDict([
                (Val.CUALQUIER, [Val.E_FINAL, "OP_AS", "=", self.acc_NADA]),
            ]),
            "20": OrderedDict([
                ("[0-9]", ["20"]),
                (Val.CUALQUIER, [Val.E_FINAL, "CTE_ENT", "\.", self.acc_NADA]),
            ]),
        }


    def input(self, text):
        """ Metodo requerido por yyparse """
        self.text = text + "\n"
        self.generate = self.generator()

    def iterar_estado(self, estado_actual, input_char):
        for (simbolo, accion) in estado_actual.items():
            if accion[0] == Val.E_FINAL:
                self.estado = "0"
                return Token(type=accion[1], value=self.cadena[0:-1])
            elif re.match(simbolo, input_char) is not None:
                if accion[2] and re.match(accion[2], input_char):
                    """ es un excepto => continue """
                    continue
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

        while i < len(self.text):
            """ Primero nos fijamos si hay tokens encolados"""
            if len(self.cola_tokens):
                yield self.cola_tokens.pop()

            """ 
                Itera caracter por caracter 
            """
            input_char = self.text[i]

            if self.estado != ESTADO_FIN_LINEA\
                and input_char == " ":
                """ Ignormos espacios dentro de de las lineas """
                i += 1
                continue
            self.cadena += input_char
            estado_actual = self.matriz[self.estado]

            """ Avanza por la matriz de estados """
            token = self.iterar_estado(estado_actual, input_char)
            if token == "NEXT":
                """ Cuando se necesita consumir mas 
                    input_char para determinar el token 
                """
                i += 1
                continue
            elif token == "IGNORE":
                """ Por ej los comentarios"""
                i += 1
                self.cadena = ""
                continue
            elif token == "ENCOLADOS":
                """ Por ej cuando se encuentran 
                    varios CIERRA_BLOQUE juntos 
                """
                self.cadena = ""
                continue
            elif token.type == 'ID':
                "ID's: Casos especiales, palabras reservadas"
                if token.value == 'if':
                    token = Token(type="PR_IF", value="if")
                elif token.value == 'while':
                    token = Token(type="PR_WHILE", value="while")

            yield token
            self.cadena = ""

    def token(self):
        try:
            token = self.generate.next()
            print token
            return token
        except StopIteration:
            return None

    """
        Metodos de acciones ejecutadas en cada estado del au" " *tomata
    """
    def acc_NADA(self, simbolo):
        pass
    def acc_RESET_NIVEL_SENTENCIA(self, simbolo):
        self.nivel_espacios_sentencia = 0
    def acc_FIN_LINEA(self, simbolo):
        if simbolo == " ":  # Bloque (tab)
            self.nivel_espacios_sentencia += 1
        else:
            # [-1] es el ultimo elemento de la lista
            if self.nivel_bloques[-1] < self.nivel_espacios_sentencia:
                self.nivel_bloques.append(self.nivel_espacios_sentencia),
                token = Token(type="ABRE_BLOQUE", value=" {\n")
            elif self.nivel_bloques[-1] > self.nivel_espacios_sentencia:
                bloque = self.nivel_bloques.pop()
                while bloque != self.nivel_espacios_sentencia:
                    token = Token(type="CIERRA_BLOQUE", value="}\n")
                    self.cola_tokens.append(token)
                    bloque = self.nivel_bloques.pop()
                    """ Si consumio todos, agregamos el nivel 0"""
                self.nivel_bloques.append(bloque)  # Agrego el ultimo bloque
                return "ENCOLADOS"
            else:
                token = Token(type="FIN_LINEA", value="\n")  # Se ignoran los epacios de tabulacion
                                                            # si no cambian el bloque
            self.nivel_espacios_sentencia = 0  # Reset nivel
            return token
        return None
    def acc_COMENTARIO(self, simbolo):
        return "IGNORE"
