"""
Universidad Nacional de La Matanza
Catedra Lenguajes y Compiladores - 2013
Mariano Francischini, Alejandro Giorgi, Roberto Bravo

TP Compilador
Basado en PLY (Python Lex-Yacc)
    http://www.dabeaz.com/ply/
    Ej: http://www.dalkescientific.com/writings/NBN/parsing_with_ply.html
"""
from collections import OrderedDict
from lexer import Lexer, Val

"""
Sintaxis:
("<caracter>", ["<nuevo_estado>", '<token>', '<caracter_excepto>', <funcion>]),
"""
matriz = {
    "0": OrderedDict([
        ('\+', ["10", '', '', Lexer.acc_NADA]),
        ("=", ["17", '', '', Lexer.acc_NADA]),
        ("[0-9]", ["20", '', '', Lexer.acc_NADA]),
        ("[a-zA-Z]", ["1", '', '', Lexer.acc_NADA]),
        ('\n', [Val.E_FIN_LINEA, '', '', Lexer.acc_RESET_NIVEL_SENTENCIA]),
        (':', ["3", '', '', Lexer.acc_NADA]),
        ('#', ["4", '', '', Lexer.acc_NADA]),

        ('>', ["6", '', '', Lexer.acc_NADA]),
        ('<', ["7", '', '', Lexer.acc_NADA]),
        ('&', ["8", '', '', Lexer.acc_NADA]),
        ('\|', ["9", '', '', Lexer.acc_NADA]),

        ('\(', ["11", '', '', Lexer.acc_NADA]),
        ('\)', ["12", '', '', Lexer.acc_NADA]),
        (',', ["21", '', '', Lexer.acc_NADA]),
        ('\*', ["22", '', '', Lexer.acc_NADA]),
        ('/', ["23", '', '', Lexer.acc_NADA]),
        ('-', ["24", '', '', Lexer.acc_NADA]),
        ('\"', ["25", '', '', Lexer.acc_NADA]),
        ('\'', ["27", '', '', Lexer.acc_NADA]),

    ]),
    "1": OrderedDict([
        ("[a-zA-Z0-9]", ["1", '', '', Lexer.acc_NADA]),
        (Val.CUALQUIER, [Val.E_FINAL, "ID", '', Lexer.acc_NADA]),
    ]),
    "2": OrderedDict([
        (" ", [Val.E_FIN_LINEA, '', '', Lexer.acc_FIN_LINEA]),
        ("\n", [Val.E_FIN_LINEA, '', '', Lexer.acc_NADA]),
        (Val.CUALQUIER, ["X", '', '', Lexer.acc_FIN_LINEA]),  # especial, termina indentacion ".": cualquier caracter
    ]),
    "3": OrderedDict([
        (Val.CUALQUIER, [Val.E_FINAL, "DOS_PUNTOS", '', Lexer.acc_NADA]),
    ]),
    "4": OrderedDict([
        ('#', ["5", '', '', Lexer.acc_NADA]),
    ]),
    "5": OrderedDict([
        ("\n", ["5.1", "", '', Lexer.acc_NADA]),
        (Val.CUALQUIER, ["5", "", '', Lexer.acc_NADA]),
    ]),
    "5.1": OrderedDict([
        ("\n", ["5.1", "", '', Lexer.acc_NADA]),
        (Val.CUALQUIER, ["X", "COMENTARIO", '', Lexer.acc_COMENTARIO]),
    ]),
    "6": OrderedDict([
        ('=', ["6.1", "", '', Lexer.acc_NADA]),
        (Val.CUALQUIER, ["F", 'OP_MAYOR', '', Lexer.acc_NADA]),
    ]),
    "6.1": OrderedDict([
        (Val.CUALQUIER, ["F", 'OP_MAYORIGUAL', '', Lexer.acc_NADA]),
    ]),
    "7": OrderedDict([
        ('>', ["13", "", '', Lexer.acc_NADA]),
        ('=', ["14", "", '', Lexer.acc_NADA]),
        (Val.CUALQUIER, ["F", 'OP_MENOR', '', Lexer.acc_NADA]),

    ]),
    "8": OrderedDict([
        ('&', ["F", 'PR_AND', '', Lexer.acc_NADA]),
    ]),
    "9": OrderedDict([
        ('|', ["F", 'PR_OR', '', Lexer.acc_NADA]),
    ]),
    "10": OrderedDict([
        (Val.CUALQUIER, [Val.E_FINAL, "OP_SUMA", '', Lexer.acc_NADA]),
    ]),
    "11": OrderedDict([
        (Val.CUALQUIER, ["F", 'PAREN_ABRE', '', Lexer.acc_NADA]),
    ]),
    "12": OrderedDict([
        (Val.CUALQUIER, ["F", 'PAREN_CIERRA', '', Lexer.acc_NADA]),
    ]),

    "13": OrderedDict([
        (Val.CUALQUIER, ["F", 'OP_DISTINTO', '', Lexer.acc_NADA]),
    ]),

    "14": OrderedDict([
        (Val.CUALQUIER, ["F", 'OP_MENORIGUAL', '', Lexer.acc_NADA]),
    ]),
    "17": OrderedDict([
        ('=', ["18", "", '', Lexer.acc_NADA]),
        (Val.CUALQUIER, [Val.E_FINAL, "OP_AS", "=", Lexer.acc_NADA]),
    ]),
        "18": OrderedDict([
        (Val.CUALQUIER, ["F", 'OP_IGUALDAD', '', Lexer.acc_NADA]),
    ]),
    
    "20": OrderedDict([
        ("[0-9]", ["20", "", "", Lexer.acc_NADA]),
        ("\.", ["20.1", "", "", Lexer.acc_NADA]),
        (Val.CUALQUIER, [Val.E_FINAL, "CTE_ENT", "\.", Lexer.acc_NADA]),
    ]),
    "20.1": OrderedDict([
        ("[0-9]", ["20.1", "", "", Lexer.acc_NADA]),
        (Val.CUALQUIER, [Val.E_FINAL, "CTE_REAL", "\.", Lexer.acc_NADA]),
    ]),
    "21": OrderedDict([
        (Val.CUALQUIER, [Val.E_FINAL, "COMA", "", Lexer.acc_NADA]),
    ]),
    "22": OrderedDict([
        (Val.CUALQUIER, [Val.E_FINAL, "OP_MUL", "", Lexer.acc_NADA]),
    ]),
    "23": OrderedDict([
        (Val.CUALQUIER, [Val.E_FINAL, "OP_DIV", "", Lexer.acc_NADA]),
    ]),
    "24": OrderedDict([
        (Val.CUALQUIER, [Val.E_FINAL, "OP_RESTA", "", Lexer.acc_NADA]),
    ]),
    "25": OrderedDict([
        (Val.CUALQUIER, ["25", "", "\"", Lexer.acc_NADA]),
        ("\"", ["26", "", "", Lexer.acc_NADA]),
    ]),
    "26": OrderedDict([
        (Val.CUALQUIER, [Val.E_FINAL, "CTE_STRING", "", Lexer.acc_CTE_STRING]),
    ]),
    "27": OrderedDict([
        (Val.CUALQUIER, ["27", "", "\'", Lexer.acc_NADA]),
        ("\'", ["28", "", "", Lexer.acc_NADA]),
    ]),
    "28": OrderedDict([
        (Val.CUALQUIER, [Val.E_FINAL, "TEXTO", "", Lexer.acc_NADA]),
    ]),
}
