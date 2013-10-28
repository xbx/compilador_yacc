# coding=utf8
from collections import defaultdict

class Val():
    """ Tipos de simbolos """
    S_TIPO_INT = 'int'
    S_TIPO_FLOAT = 'float'
    S_TIPO_FUNCION = 'funcion'
    S_TIPO_CTE_STRING = 'cte_string'

class Simbolo():
    def __init__(self):
        self.id = None
        self.nombre = None
        self.tipo = None
        self.ambito = None
        self.offset = None # Para la generacion de Asm
        self.valor = None # Para la generacion de Asm (cte string)
    def __repr__(self):
        return "%s   | %s   | %s   | %s   |  %s" % (self.id, self.nombre, self.tipo, self.ambito, self.offset)
    def __str__(self):
        return "sim%s[%s:%s]" % (self.id, self.tipo, self.nombre)

class TablaSim():
    def __init__(self):
        lista = lambda:defaultdict(lista)
        self.tabla = lista()
        self.declaraciones = {}
        self.ambito_actual = None
        self.ultimo_id = 0

    def declarar_variable(self, tipo, nombre):
        """
         TODO: cuando se declaran varias variables juntas (con ","), no llega
               esta lista con coma sino algo como "ter[2]" (la ref al terceto)
        """
        simbolo = Simbolo()
        simbolo.id = self.ultimo_id
        self.ultimo_id = self.ultimo_id + 1
        simbolo.nombre = nombre
        simbolo.tipo = tipo
        simbolo.ambito = self.ambito_actual

        if self.ambito_actual == 'main':
            self.insertar_en_tabla(simbolo)
        else:
            # Lo ponemos en otra lista provisoriamente porque
            # "todavia" no sabemos de qué ambito se trata
            self.declaraciones[simbolo.nombre] = simbolo

        return simbolo

    def declarar_cte_string(self, string):
        simbolo = Simbolo()
        simbolo.id = self.ultimo_id
        self.ultimo_id = self.ultimo_id + 1
        simbolo.nombre = '_CTE_STRING_' + str(simbolo.id)
        simbolo.tipo = Val.S_TIPO_CTE_STRING
        simbolo.ambito = self.ambito_actual or "main"
        simbolo.valor = string

        self.insertar_en_tabla(simbolo)
        return simbolo

    def declarar_funcion(self, nombre):
        # Agregamos el simbolo 'funcion'
        simbolo = Simbolo()
        simbolo.id = self.ultimo_id
        self.ultimo_id = self.ultimo_id + 1
        simbolo.nombre = nombre
        simbolo.tipo = Val.S_TIPO_FUNCION
        simbolo.ambito = 'main'  # Toda funcion esta en ambito main
        self.insertar_en_tabla(simbolo)

        # Agregamos sus declaraciones que hasta el momento no se sabia
        # de que funcion eran:
        for _, item in self.declaraciones.items():
            item.ambito = nombre
            self.insertar_en_tabla(item)
        self.declaraciones = {}
        return simbolo

    def obtener_variable(self, nombre):
        if nombre in self.declaraciones:
            return self.declaraciones[nombre]
        if 'main' in self.tabla and nombre in self.tabla['main']:
            return self.tabla['main'][nombre]

        raise TypeError("Error: Variable '%s' no declarada en ambito actual." % nombre)

    def insertar_en_tabla(self, simbolo):
        self.tabla[simbolo.ambito][simbolo.nombre] = simbolo

    def __iter__(self):
        for _, simbolo in self.tabla.items():
            if isinstance(simbolo, Simbolo):
                yield simbolo
            else:
                for _, simbolo2 in simbolo.items():
                    yield simbolo2

    def __str__(self):
        string = "Id   Nombre Tipo   Ambito  Offset stack\n"
        for simbolo in self:
            string = string + repr(simbolo) + "\n"
        return string
