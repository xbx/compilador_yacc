from collections import OrderedDict

class Simbolo():
    def __init__(self):
        self.id = None
        self.nombre = None
        self.tipo = None
        self.ambito = None

class TablaSim():
    def __init__(self):
        self.tabla = OrderedDict()

