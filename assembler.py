from os import system
from collections import OrderedDict
from tabla_sim import Simbolo
from asm_template import Asm

class TraductorAsm:
    id_etiqueta = 0

    def __init__(self, tercetos, tabla_sim):
        self.tercetos = tercetos
        self.tabla_sim = tabla_sim
        self.asm = Asm.base

    def traducir(self, filename):
        """ Traduce la notacion intermedia a texto assembler """

        # declaraciones de tabla de simbolos
        self.declaraciones_main()

        self.asm_terceto = OrderedDict()

        for terceto in self.tercetos:
            if terceto.tipo == "programa":
                asm = self.asm_terceto[terceto.items[0].id]
                # Print hola mundo
                # asm = asm + "\n" + Asm.print_.replace("%string", "str")
                # asm = asm.replace("%len", "str_len")
                self.asm = self.asm.replace('%main', asm)
            elif terceto.tipo == "main":
                self.asm_terceto[terceto.id] = ""
                for item in [item for item in terceto.items if item.tipo == 'bloque']:
                    # Salteo las funciones porque no son parte de la rutina main
                    self.asm_terceto[terceto.id] += self.asm_terceto[item.id]
            elif terceto.tipo == "condicion":
                asm = ""
                if terceto.items[0] in ["<", "<=", ">", ">=", '==']:
                    izq = self.representar_operando(terceto.items[1])
                    der = self.representar_operando(terceto.items[2])
                    asm = "movl    %s, %%eax\n" % der
                    asm += "        movl    %s, %%edx\n" % izq
                    asm += "        cmpl    %eax, %edx"
                self.asm_terceto[terceto.id] = asm
            elif terceto.tipo == "while":
                pass
            elif terceto.tipo == "if":
                condicion = terceto.items[0]
                tipo_condicion = condicion.items[0]
                bloque = self.asm_terceto[terceto.items[1].id]
                if tipo_condicion == '&':
                    # condicion compleja: a > b & b < c
                    izq = condicion.items[1]
                    der = condicion.items[2]

                    asm_condicion = self.obtener_asm_condicion_and_or(condicion_izq=izq, condicion_der=der)

                    asm = Asm.if_and_or
                    asm = asm.replace("%condicion_and_or", asm_condicion)
                    asm = asm.replace('%etiqueta_end', self.inventar_etiqueta(prefijo='ENDIF'))
                else:
                    # condicion simple: a > b
                    asm_tipo = self.obtener_jump(tipo_condicion)
                    asm_condicion = Asm.condicion_simple
                    asm_condicion = asm_condicion.replace('%condicion', self.asm_terceto[terceto.items[0].id])
                    asm_condicion = asm_condicion.replace('%tipo_condicion', asm_tipo)
                    asm = Asm.if_
                    asm = asm.replace('%condicion_simple', asm_condicion)
                    asm = asm.replace('%etiqueta_end', self.inventar_etiqueta(prefijo='ENDIF'))


                asm = asm.replace('%bloque', bloque)
                self.asm_terceto[terceto.id] = asm
            elif terceto.tipo == "bloque":
                asm = ""
                for item in terceto.items:
                    asm = asm + self.asm_terceto[item.id]
                self.asm_terceto[terceto.id] = asm
            elif terceto.tipo == "expresion":
                asm = ""
                operando1 = self.representar_operando(terceto.items[1])
                operando2 = self.representar_operando(terceto.items[2])
                asm = asm + "\n# suma\n"
                asm = asm + "        fld    %s\n" % operando1
                asm = asm + "        fld    %s\n" % operando2
                if terceto.items[0] == '+':
                    asm = asm + "        fadd\n"
                elif terceto.items[0] == '-':
                    asm = asm + "        fsub\n"
                asm = asm + "        fst    %eax\n"
                asm = asm + "        ffree\n"
                self.asm_terceto[terceto.id] = asm
            elif terceto.tipo == "sentencia":
                asm = ""
                for item in terceto.items:
                    try:  # TODO: hardcode, hay que soportar todas las sentencias
                        asm = asm + self.asm_terceto[item.id]
                    except:
                        pass
                self.asm_terceto[terceto.id] = asm
            elif terceto.tipo == "asig":
                asm = ""
                if isinstance(terceto.items[1], terceto.__class__):
                    # Un terceto, ej el resultado de una suma
                    # TODO: hardcode, por ahora todos los resultados a eax
                    asm = asm + self.asm_terceto[terceto.items[1].id]
                    valor = '%eax'
                else:
                    # Valor literal, ej "123"
                    valor = terceto.items[1]
                    if isinstance(valor, Simbolo):
                        # Nombre de la constante
                        valor = self.representar_operando(valor)
                asm += "        movl    %s, %%eax\n" % valor
                asm = asm + "        movl    %%eax, -%s(%%ebp) # asig\n" % terceto.items[0].offset
                self.asm_terceto[terceto.id] = asm
            elif terceto.tipo == "print":
                asm = Asm.print_
                simbolo = terceto.items[0]
                asm = asm.replace('%string', self.representar_operando(simbolo))  # TODO: hardcode string
                asm = asm.replace('%len', '5')  # TODO: hardcode len
                self.asm_terceto[terceto.id] = asm
            elif terceto.tipo == 'funcion':
                simbolo = terceto.items[0]

                asm = Asm.funcion
                offset_declaraciones = self.declaraciones_funcion(simbolo_funcion=simbolo)

                asm = asm.replace('%offset_declaraciones', offset_declaraciones)
                asm = asm.replace('%nombre', simbolo.nombre)

                # cuerpo de la funcion
                terceto_id = terceto.items[2].id

                # TODO: hardcode. Deberia siempre encontrarse el ASM expandido
                #        para el cuerpo de la funcion
                try:
                    asm = asm.replace('%bloque', self.asm_terceto[terceto_id])
                except KeyError:
                    asm = asm.replace('%bloque', '')

                a_retornar = self.representar_operando(terceto.items[3])
                asm_return = "    movl    %s, %%eax" % a_retornar
                asm = asm.replace('%return', asm_return)

                self.asm_terceto[terceto.id] = asm
                self.asm = self.asm.replace('%funciones', asm)
            elif terceto.tipo == 'call':
                self.asm_terceto[terceto.id] = "andl    $-16, %%esp\n        call     %s\n" % terceto.items[0]


        # Limpiamos las marcas sin usar que pudieron haber quedado
        self.limpiar_marcas()

        with open(filename, "w") as out:
            out.write(self.asm)

    def compilar(self, asm, ejecutable):
        system("/bin/gcc -m32 -o %s %s" % (ejecutable, asm))

    def ejecutar(self, ejecutable):
        system("./%s" % ejecutable)

    def obtener_asm_condicion_and_or(self, condicion_izq, condicion_der):
        asm_tipo_izq = self.obtener_jump(condicion_izq.items[0])
        asm_tipo_der = self.obtener_jump(condicion_der.items[0])
        asm_condicion = Asm.condicion_and_or
        asm_condicion = asm_condicion.replace('%condicion_izq', self.asm_terceto[condicion_izq.id])
        asm_condicion = asm_condicion.replace('%tipo_condicion_izq', asm_tipo_izq)
        asm_condicion = asm_condicion.replace('%condicion_der', self.asm_terceto[condicion_der.id])
        asm_condicion = asm_condicion.replace('%tipo_condicion_der', asm_tipo_der)
        return asm_condicion
    def obtener_jump(self, tipo_condicion):
        if tipo_condicion == '==':
            asm_tipo = 'jne'
        elif tipo_condicion == '<':
            asm_tipo = 'jge'
        elif tipo_condicion == '<=':
            asm_tipo = 'jg'
        elif tipo_condicion == '>':
            asm_tipo = 'jle'
        elif tipo_condicion == '>=':
            asm_tipo = 'jl'
        return asm_tipo

    def declaraciones_main(self):
        offset = {}
        asm_cte_numericas = "# constantes numericas\n"
        asm_cte_string = "# constantes string\n"
        for simbolo in self.tabla_sim:
            if simbolo.ambito == 'global':
                # Constantes (globales)
                if simbolo.tipo == "cte_numerica":
                    if '.' in simbolo.valor:
                        valor = simbolo.valor
                    else:
                        # Forzamos a que sean siempre reales
                        valor = "%s.0" % simbolo.valor
                        # valor = simbolo.valor
                    asm_temp = Asm.cte_numerica.replace("%nombre", simbolo.nombre)
                    asm_temp = asm_temp.replace("%valor", simbolo.valor)
                    asm_cte_string += asm_temp
                elif simbolo.tipo == "cte_string":
                    asm_temp = Asm.cte_string.replace("%nombre", simbolo.nombre)
                    asm_temp = asm_temp.replace("%valor", simbolo.valor)
                    asm_cte_string += asm_temp
            else:
                # Variables para el stack (Se calcula offset)
                try:
                    offset[simbolo.ambito] = offset[simbolo.ambito] + 4
                except KeyError:
                    offset[simbolo.ambito] = 4
                simbolo.offset = offset[simbolo.ambito]

        declaraciones_main = ("# declaraciones\n"
                             + "        subl    $%s, %%esp\n" % offset['main'])
        self.asm = self.asm.replace("%declaraciones_main", declaraciones_main)
        self.asm = self.asm.replace("%cte_numericas", asm_cte_numericas)
        self.asm = self.asm.replace("%cte_string", asm_cte_string)

    def declaraciones_funcion(self, simbolo_funcion):
        offset = 0
        for simbolo in self.tabla_sim:
            if simbolo.ambito == simbolo_funcion.nombre and simbolo.offset > offset:
                offset = simbolo.offset
        return str(offset)

    def representar_operando(self, operando):
        if isinstance(operando, Simbolo):
            if operando.offset is not None:
                return "   -%s(%%ebp)" % operando.offset
            else:
                if operando.tipo == 'cte_numerica':
                    return "$%s" % operando.valor
                else:
                    return operando.nombre
        elif isinstance(operando, str):
            return operando

    def representar_operando_indirecto(self, operando):
        if isinstance(operando, Simbolo):
            if operando.offset is not None:
                return "   %s(%%ebp)" % operando.offset
            else:
                return "DWORD [%s]" % operando.nombre
        elif isinstance(operando, str):
            return operando

    def limpiar_marcas(self):
        self.asm = self.asm.replace('%funciones', '')

    def inventar_etiqueta(self, prefijo):
        TraductorAsm.id_etiqueta = TraductorAsm.id_etiqueta + 1
        return ".%s_%s" % (prefijo, TraductorAsm.id_etiqueta)
