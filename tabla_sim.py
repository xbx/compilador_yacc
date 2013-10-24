# coding=utf8
from collections import OrderedDict

class Val():
    """ Tipos de simbolos """
    S_TIPO_INT = 'int'
    S_TIPO_FLOAT = 'float'
    S_TIPO_FUNCION = 'funcion'

class Simbolo():
    def __init__(self):
        self.id = None
        self.nombre = None
        self.tipo = None
        self.ambito = None
    def __str__(self):
        return "%s   | %s   | %s   | %s " % (self.id, self.nombre, self.tipo, self.ambito)
    def __repr__(self):
        return "sim[%s]" % self.id

class TablaSim():
    def __init__(self):
        self.tabla = OrderedDict()
        self.declaraciones = {}
        self.ambito_actual = None
        self.ultimo_id = 0

    def declarar_variable(self, tipo, lista_ids):
        """
         TODO: cuando se declaran varias variables juntas (con ","), no llega
               esta lista con coma sino algo como "[2]" (la ref al terceto)
        """
        lista_ids = lista_ids.split(',')
        for nombre in lista_ids:
            simbolo = Simbolo()
            simbolo.id = self.ultimo_id
            self.ultimo_id = self.ultimo_id + 1
            simbolo.nombre = nombre
            simbolo.tipo = tipo
            simbolo.ambito = self.ambito_actual

            if self.ambito_actual == 'main':
                self.tabla[nombre] = simbolo
            else:
                # Lo ponemos en otra lista provisoriamente porque
                # "todavia" no sabemos de qué ambito se trata
                self.declaraciones[nombre] = simbolo

        return simbolo

    def declarar_funcion(self, nombre):
        # Agregamos el simbolo 'funcion'
        simbolo = Simbolo()
        simbolo.id = self.ultimo_id
        self.ultimo_id = self.ultimo_id + 1
        simbolo.nombre = nombre
        simbolo.tipo = Val.S_TIPO_FUNCION
        simbolo.ambito = 'main'  # Toda funcion esta en ambito main
        self.tabla[nombre] = simbolo

        # Agregamos sus declaraciones que hasta el momento no se sabia
        # de que funcion eran:
        for nombre_variable, simbolo in self.declaraciones.items():
            simbolo.ambito = nombre
            self.tabla[nombre_variable] = simbolo
        self.declaraciones = {}

    def obtener_variable(self, nombre):
        if nombre in self.declaraciones:
            return self.declaraciones[nombre]
        if nombre in self.tabla and self.tabla[nombre].ambito == 'main':
            return self.tabla[nombre]

        raise TypeError("Error: Variable '%s' no declarada en ambito actual." % nombre)


    def __str__(self):
        string = "Id Nombre Tipo Ambito\n"
        for _, simbolo in self.tabla.items():
            string = string + str(simbolo) + "\n"
        return string
