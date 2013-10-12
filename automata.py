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

    ]),
    "1": OrderedDict([
        ("[a-zA-Z0-9]", ["1", '', '', Lexer.acc_NADA]),
        (Val.CUALQUIER, [Val.E_FINAL, "ID", '', Lexer.acc_NADA]),
    ]),
    "2": OrderedDict([
        (" ", [Val.E_FIN_LINEA, '', '', Lexer.acc_FIN_LINEA]),
        (Val.CUALQUIER, ["X", '', '', Lexer.acc_FIN_LINEA]),  # especial, termina indentacion ".": cualquier caracter
    ]),
    "3": OrderedDict([
        (Val.CUALQUIER, [Val.E_FINAL, "DOS_PUNTOS", '', Lexer.acc_NADA]),
    ]),
    "4": OrderedDict([
        ('#', ["5", '', '', Lexer.acc_NADA]),
    ]),
    "5": OrderedDict([
        ("\n", ["X", "COMENTARIO", '', Lexer.acc_COMENTARIO]),
        (Val.CUALQUIER, ["5", "", '\n', Lexer.acc_NADA]),
    ]),

    "6": OrderedDict([
        (Val.CUALQUIER, ["F", 'OP_MAYOR', '', Lexer.acc_NADA]),
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
        (Val.CUALQUIER, [Val.E_FINAL, "OP_AS", "=", Lexer.acc_NADA]),
    ]),
    "20": OrderedDict([
        ("[0-9]", ["20"]),
        (Val.CUALQUIER, [Val.E_FINAL, "CTE_ENT", "\.", Lexer.acc_NADA]),
    ]),
}
