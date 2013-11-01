class Asm:
    base = (
"""
    .file    "test.c"
    .text

%funciones

    .section    .rodata.str1.1,"aMS",@progbits,1

.LC0:
    .string "la gran cadena"

%cte_numericas
%cte_string

    .section    .text.startup,"ax",@progbits
    .globl  main
    .type   main, @function
main:
        %declaraciones_main

; contenido main
%main

        ; return
        movl    $0, %ebx
        movl    $1, %eax
        int     $0x80
; fin contenido main
"""
)

    if_ = (
"""
; if
        %condicion_simple
        %bloque
%etiqueta_end:
"""
)
    condicion_simple = (
"""
        %condicion
        %tipo_condicion    %etiqueta_end
"""
)
    condicion_and_or = (
"""
        %condicion_izq
        %tipo_condicion_izq    %etiqueta_end
        %condicion_der
        %tipo_condicion_der    %etiqueta_end
"""
)

    if_and_or = (
"""
; if
%condicion_and_or
        %bloque
%etiqueta_end:
"""
)
    while_ = (
"""
; while
        jmp %etiqueta_condicion
%etiqueta_do:
        %bloque
%etiqueta_condicion:
        %condicion
        %tipo_condicion    %etiqueta_do
"""
)

    print_ = (
"""
; print
        movl    $%len, %edx
        movl    $%string, %ecx
        movl    $1, %ebx
        movl    $4, %eax
        int     $0x80
"""
)

    funcion = (
"""
;funcion
.globl %nombre
.type   %nombre, @function
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
