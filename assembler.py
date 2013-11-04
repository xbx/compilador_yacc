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
                self.asm = self.asm.replace('%main', asm)
            elif terceto.tipo == "main":
                self.asm_terceto[terceto.id] = ""
                for item in [item for item in terceto.items if item.tipo in ['bloque', 'sentencia']]:
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
                condicion = terceto.items[0]
                tipo_condicion = condicion.items[0]
                bloque = self.asm_terceto[terceto.items[1].id]
                asm = Asm.while_
                if tipo_condicion == '&':
                    # condicion compleja: a > b & b < c
                    izq = condicion.items[1]
                    der = condicion.items[2]
                    asm_condicion = self.obtener_asm_condicion_and_or(condicion_izq=izq, condicion_der=der)
                else:
                    # condicion simple: a > b
                    asm_tipo = self.obtener_jump(tipo_condicion)
                    asm_condicion = Asm.condicion_simple
                    asm_condicion = asm_condicion.replace('%condicion', self.asm_terceto[terceto.items[0].id])
                    asm_condicion = asm_condicion.replace('%tipo_condicion', asm_tipo)

                asm = asm.replace('%condicion', asm_condicion)
                etiqueta_do = self.inventar_etiqueta(prefijo='DO')
                asm = asm.replace('%etiqueta_do', etiqueta_do)
                asm = asm.replace('%etiqueta_condicion', self.inventar_etiqueta(prefijo='CONDICION'))
                asm = asm.replace('%etiqueta_salto', etiqueta_do)
                asm = asm.replace('%bloque', bloque)
                self.asm_terceto[terceto.id] = asm

            elif terceto.tipo == "if" or terceto.tipo == "ifelse":
                condicion = terceto.items[0]
                tipo_condicion = condicion.items[0]
                bloque = self.asm_terceto[terceto.items[1].id]
                if tipo_condicion == '&':
                    # condicion compleja: a > b & b < c
                    izq = condicion.items[1]
                    der = condicion.items[2]

                    asm_condicion = self.obtener_asm_condicion_and_or(condicion_izq=izq, condicion_der=der)

                    asm = Asm.if_
                    asm = asm.replace("%condicion", asm_condicion)
                else:
                    # condicion simple: a > b
                    asm_tipo = self.obtener_jump(tipo_condicion)
                    asm_condicion = Asm.condicion_simple
                    asm_condicion = asm_condicion.replace('%condicion', self.asm_terceto[terceto.items[0].id])
                    asm_condicion = asm_condicion.replace('%tipo_condicion', asm_tipo)
                    asm = Asm.if_
                    asm = asm.replace('%condicion', asm_condicion)

                asm = asm.replace('%etiqueta_salto', self.inventar_etiqueta(prefijo='IFSALTO'))
                asm = asm.replace('%etiqueta_fin', self.inventar_etiqueta(prefijo='ENDIF'))
                if terceto.tipo == 'ifelse':
                    bloque_else = self.asm_terceto[terceto.items[2].id]
                else:
                    bloque_else = ""
                asm = asm.replace('%bloque_else', bloque_else)

                asm = asm.replace('%bloque', bloque)
                self.asm_terceto[terceto.id] = asm
            elif terceto.tipo == "bloque":
                asm = ""
                for item in terceto.items:
                    asm = asm + self.asm_terceto[item.id]
                self.asm_terceto[terceto.id] = asm
            elif terceto.tipo == "expresion":
                asm = "\n# aritmetica\n"

                operando1 = self.representar_operando(terceto.items[1])
                if isinstance(terceto.items[1], terceto.__class__):
                    asm += self.asm_terceto[terceto.items[1].id]
                    print terceto
                    fld1 = terceto.items[1].tipo_fld
                elif isinstance(terceto.items[1], Simbolo):
                    if terceto.items[1].tipo == 'int':
                        fld1 = 'filds'
                    elif terceto.items[1].tipo == 'float':
                        fld1 = 'flds'
                    else:
                        fld1 = 'flds'


                operando2 = self.representar_operando(terceto.items[2])
                if isinstance(terceto.items[2], terceto.__class__):
                    asm += self.asm_terceto[terceto.items[2].id]
                    fld2 = terceto.items[2].tipo_fld
                elif isinstance(terceto.items[1], Simbolo):
                    if terceto.items[1].tipo == 'int':
                        fld2 = 'filds'
                    elif terceto.items[1].tipo == 'float':
                        fld2 = 'flds'
                    else:
                        fld2 = 'flds'

                # Operando 2 a copro
                if operando2 == '%eax':
                    asm = asm + "        movl   %s, -4(%%ebp)\n" % operando2
                    operando2 = '-4(%ebp)'
                asm = asm + "        %s   %s\n" % (fld2, operando2)

                # Operando 1 a copro
                if operando1 == '%eax':
                    asm = asm + "        movl   %s, -4(%%ebp)\n" % operando1
                    operando1 = '-4(%ebp)'
                asm = asm + "        %s   %s\n" % (fld1, operando1)


                if (fld1, fld2) == ('filds', 'filds'):
                    terceto.tipo_fld = 'fild'
                else:
                    terceto.tipo_fld = 'fld'

                if terceto.items[0] == '+':
                    asm = asm + "        faddp    %st, %st(1)\n"
                elif terceto.items[0] == '-':
                    asm = asm + "        fsub    %st, %st(1)\n"
                    asm = asm + "        fxch\n"
                if terceto.items[0] == '*':
                    asm = asm + "        fmulp    %st, %st(1)\n"
                if terceto.items[0] == '/':
                    asm = asm + "        fdivp    %st, %st(1)\n"
                if terceto.items[0] == '%':
                    asm = asm + "        call     fmod\n"  # TODO: no funciona ok el mod

                if terceto.tipo_fld == 'fild':
                    asm = asm + "        fistpl    -4(%ebp)\n"
                else:
                    asm = asm + "        fstps    -4(%ebp)\n"

                terceto.variable_aux = '-4(%ebp)'
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
                    valor = terceto.items[1].variable_aux
                else:
                    # Valor literal, ej "123"
                    valor = terceto.items[1]
                    if isinstance(valor, Simbolo):
                        # Nombre de la constante
                        valor = self.representar_operando(valor)
                        terceto.items[0].etiqueta_cte = valor
                asm += "        movl    %s, %%eax\n" % valor
                asm = asm + "        movl    %%eax, -%s(%%ebp) # asig\n" % terceto.items[0].offset
                self.asm_terceto[terceto.id] = asm
            elif terceto.tipo == "print":
                asm = Asm.print_
                simbolo = terceto.items[0]
                if simbolo.tipo == 'int':
                    asm = asm.replace('%tipo_mov', 'leal')
                    asm = asm.replace('%len', '1')  # TODO: hardcode len
                else:
                    asm = asm.replace('%tipo_mov', 'movl')
                    try:
                        asm = asm.replace('%len', '%s_tam' % simbolo.etiqueta_cte)
                    except:
                        asm = asm.replace('%len', '%s_tam' % simbolo.nombre)
                asm = asm.replace('%string', self.representar_operando(simbolo))
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
                terceto.variable_aux = '%eax'
                asm_return = "    movl    %s, %s" % (a_retornar, terceto.variable_aux)
                asm = asm.replace('%return', asm_return)

                self.asm_terceto[terceto.id] = asm
                self.asm = self.asm.replace('%funciones', asm)
            elif terceto.tipo == 'call':
                terceto.variable_aux = '%eax'
                nombre_fun = terceto.items[0]
                self.asm_terceto[terceto.id] = "        andl    $-16, %%esp\n        call     %s\n" % nombre_fun
                simbolo_fun = self.tabla_sim.obtener_variable(nombre_fun)
                if simbolo_fun.tipo_retorno == 'int':
                    terceto.tipo_fld = 'fild'
                elif simbolo_fun.tipo_retorno == 'float':
                    terceto.tipo_fld = 'fld'
            elif terceto.tipo == 'tecla':
                terceto.variable_aux = '-4(%ebp)'
                self.asm_terceto[terceto.id] = Asm.tecla


        # Limpiamos las marcas sin usar que pudieron haber quedado
        self.limpiar_marcas()

        with open(filename, "w") as out:
            out.write(self.asm)

    def compilar(self, asm, ejecutable):
        system("/bin/gcc -lm -m32 -o %s %s" % (ejecutable, asm))

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
        asm_cte_numericas = ""
        asm_cte_string = ""
        for simbolo in self.tabla_sim:
            if simbolo.ambito == 'global':
                # Constantes (globales)
                if simbolo.tipo == "cte_float":
                    asm_temp = Asm.cte_float.replace("%nombre", simbolo.nombre)
                    asm_temp = asm_temp.replace("%valor", simbolo.valor)
                    asm_cte_numericas += asm_temp
                if simbolo.tipo == "cte_int":
                    asm_temp = Asm.cte_int.replace("%nombre", simbolo.nombre)
                    asm_temp = asm_temp.replace("%valor", simbolo.valor)
                    asm_cte_numericas += asm_temp
                elif simbolo.tipo == "cte_string":
                    asm_temp = Asm.cte_string.replace("%nombre", simbolo.nombre)
                    asm_temp = asm_temp.replace("%tamanio", str(len(simbolo.valor)))
                    asm_temp = asm_temp.replace("%valor", simbolo.valor)
                    asm_cte_string += asm_temp
            else:
                # Variables para el stack (Se calcula offset)
                try:
                    offset[simbolo.ambito] = offset[simbolo.ambito] + 4
                except KeyError:
                    offset[simbolo.ambito] = 8
                simbolo.offset = offset[simbolo.ambito]

        declaraciones_main = ("# declaraciones\n"
                             + "        subl    $%s, %%esp\n" % offset['main'])
        self.asm = self.asm.replace("%declaraciones_main", declaraciones_main)
        self.asm = self.asm.replace("%cte_numericas", asm_cte_numericas)
        self.asm = self.asm.replace("%cte_string", asm_cte_string)

    def declaraciones_funcion(self, simbolo_funcion):
        offset = 0
        for simbolo in self.tabla_sim:
            # Buscamos el mayor offset
            if simbolo.ambito == simbolo_funcion.nombre and simbolo.offset > offset:
                offset = simbolo.offset
        return str(offset)

    def representar_operando(self, operando):
        if isinstance(operando, Simbolo):
            if operando.offset is not None:
                return "-%s(%%ebp)" % operando.offset
            else:
                if operando.tipo in ['cte_float', 'cte_int']:
                    return "%s" % operando.nombre
                else:
                    return operando.nombre
        elif isinstance(operando, str):
            return operando
        elif hasattr(operando, 'variable_aux'):
            return operando.variable_aux

    def limpiar_marcas(self):
        self.asm = self.asm.replace('%funciones', '')

    def inventar_etiqueta(self, prefijo):
        TraductorAsm.id_etiqueta = TraductorAsm.id_etiqueta + 1
        return ".%s_%s" % (prefijo, TraductorAsm.id_etiqueta)
