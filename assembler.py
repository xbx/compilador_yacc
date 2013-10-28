from os import system
from collections import OrderedDict
from tabla_sim import Simbolo

class TraductorAsm:
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
            if terceto.tipo == "sentencia":
                asm = ""
                for item in terceto.items:
                    try:  # TODO: hardcode, hay que soportar todas las sentencias
                        asm = asm + self.asm_terceto[item.id]
                    except:
                        pass
                self.asm_terceto[terceto.id] = asm
            elif terceto.tipo == "asig":
                asm = "mov dword [ebp+%s], %s ; asig" % (terceto.items[0].offset, terceto.items[1])
                self.asm_terceto[terceto.id] = asm
            elif terceto.tipo == "print":
                asm = Asm.print_
                simbolo = terceto.items[0]
                asm = asm.replace('%string', 'str')  # TODO: hardcode string
                asm = asm.replace('%len', 'str_len')  # TODO: hardcode len
                self.asm_terceto[terceto.id] = asm
            elif terceto.tipo == 'funcion':
                simbolo = terceto.items[0]

                asm = Asm.funcion
                declaraciones = self.declaraciones_funcion(simbolo_funcion=simbolo)

                asm = asm.replace('%declaraciones', declaraciones)
                asm = asm.replace('%nombre', simbolo.nombre)

                # cuerpo de la funcion
                terceto_id = terceto.items[2].id

                # TODO: hardcode. Deberia siempre encontrarse el ASM expandido
                #        para el cuerpo de la funcion
                try:
                    asm = asm.replace('%bloque', self.asm_terceto[terceto_id])
                except KeyError:
                    asm = asm.replace('%bloque', '')

                self.asm_terceto[terceto.id] = asm
                self.asm = self.asm.replace('%funciones', asm)



        # Print hola mundo
        print_ = Asm.print_.replace("%string", "str")
        print_ = print_.replace("%len", "str_len")
        self.asm = self.asm.replace("%_start", print_)

        with open(filename, "w") as out:
            out.write(self.asm)


    def compilar(self, asm, ejecutable):
        system("/bin/nasm -f elf -F stabs -o programa.o %s" % asm)
        system("ld -m elf_i386 -o %s programa.o" % ejecutable)

    def ejecutar(self, ejecutable):
        system("./%s" % ejecutable)

    def declaraciones_main(self):
        offset = {}

        for simbolo in self.tabla_sim:
            try:
                offset[simbolo.ambito] = offset[simbolo.ambito] + 4
            except KeyError:
                offset[simbolo.ambito] = 0
            simbolo.offset = offset[simbolo.ambito]
        declaraciones_main = ("; declaraciones\n"
                             + "\tmov    esp, %s\n" % offset['main'])
        self.asm = self.asm.replace("%declaraciones_start", declaraciones_main)

    def declaraciones_funcion(self, simbolo_funcion):
        offset = 0
        for simbolo in self.tabla_sim:
            if simbolo.ambito == simbolo_funcion.nombre and simbolo.offset > offset:
                offset = simbolo.offset
        declaraciones = "mov    esp, %s\n" % offset
        return declaraciones



class Asm:
    base = (
"""
section .data                           ; section for initialized data
str:     db 'Hola mundo!', 0Ah         ; message string with new-line char at the end (10 decimal)
str_len: equ $ - str                    ; calcs length of string (bytes) by subtracting this' address ($ symbol) 
                                            ; from the str's start address

section .text                           ; this is the code section

%funciones

global _start                           ; _start is the entry point and needs global scope to be 'seen' by the 
                                            ; linker -    equivalent to main() in C/C++
_start:                                 ; procedure start
        %declaraciones_start

        ; contenido
        %_start


        mov    eax, 1                   ; specify sys_exit function code (from OS vector table)
        mov    ebx, 0                   ; specify return code for OS (0 = everything's fine)
        int    80h                      ; tell kernel to perform system call
"""
)

    print_ = (
"""
        mov    eax, 4                   ; specify the sys_write function code (from OS vector table)
        mov    ebx, 1                   ; specify file descriptor stdout -in linux, everything's treated as a file, 
                                          ; even hardware devices
        mov    ecx, %string             ; move start _address_ of string message to ecx register
        mov    edx, %len             ; move length of message (in bytes)
        int    80h                      ; tell kernel to perform the system call we just set up - 
                                          ; in linux services are requested through the kernel
"""
)
    funcion = (
"""
global %nombre
%nombre:
        push    ebp
        mov     esp, ebp

        ; declaraciones
        %declaraciones
        ; fin declaraciones

        ; bloque
        %bloque
        ; fin bloque

        pop     ebp
        mov     ebp, esp
        ret
"""
)
