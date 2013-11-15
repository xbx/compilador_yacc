class Asm:
    base = (
"""
# -----------------------------------------------
    .text

# FUNCIONES -------------------------------------
%funciones

    .section    .rodata.str1.1,"aMS",@progbits,1


# Main -----------------------------------------
    .section    .text.startup,"ax",@progbits
    .globl  main
    .type   main, @function
main:
        pushl    %ebp
        movl     %esp, %ebp

        %declaraciones_main

        # Cadena estatica, en main es a si mismo
        movl     %ebp, -8(%ebp)


# contenido main
%main

        # exit main
        leave
        ret
        .size   main, .-main
        .section    .rodata
        .align 4
# Constantes ------------------------------------
.LC0:
    .long
    .align 4
    .type   .LC0, @object
LC0:
    .long   .LC0

%cte_numericas
%cte_string
"""
)

    if_ = (
"""
# if
        %condicion
        %bloque
        jmp    %etiqueta_fin
%etiqueta_salto:
        %bloque_else
%etiqueta_fin:
"""
)
    condicion_simple = (
"""
        %condicion
        %tipo_condicion    %etiqueta_salto
"""
)
    condicion_and_or = (
"""
        %condicion_izq
        %tipo_condicion_izq    %etiqueta_salto
        %condicion_der
        %tipo_condicion_der    %etiqueta_salto
"""
)

    while_ = (
"""
# while
%etiqueta_condicion:
        %condicion
        %bloque
        jmp %etiqueta_condicion
%etiqueta_do:
"""
)

    print_ = (
"""
# print
        movl    $%len, %edx        # tamanio
        %tipo_mov    %string, %ecx # string
        movl    $1, %ebx           # sys write
        movl    $4, %eax           # stdout
        int     $0x80              # syscall
"""
)

    tecla = (
"""
# tecla
        call    getchar
        movl    %eax, -4(%ebp)
tecla:
        call    getchar
        cmpl    %eax, _10
        jne     tecla
        # fildl    -4(%ebp)
        # fstps    -4(%ebp)
"""
)
    funcion = (
"""
# funcion %nombre ------------------------------
.globl %nombre
.type   %nombre, @function
%nombre:
        pushl   %ebp
        movl    %esp, %ebp
        subl    $%offset_declaraciones, %esp

        # Copio Cadena estatica
        movl    8(%ebp), %ecx
        movl    %ecx, -8(%ebp)

%bloque
        leave
        # addl    $%offset_declaraciones, %esp
        ret
%funciones
"""
)

    cte_string = (
"""
.%nombre:
    .ascii "%valor\\n"
    .type   %nombre, @object
%nombre:
    .long   .%nombre
    .ascii "%valor\\n"
    .set    %nombre_tam, .-%nombre-5
"""
)

    cte_float = (
"""
%nombre:
    .float %valor
    .align 4
"""
)

    cte_int = (
"""
%nombre:
    .int %valor
    .align 4
"""
)

