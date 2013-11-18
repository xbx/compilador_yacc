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

_ascii_enter:
    .int 10
    .align 4

%cte_numericas
%cte_string
"""
)

    if_ = (
"""
# if
        %condicion
%etiqueta_entra:
        %bloque
        jmp    %etiqueta_fin
%etiqueta_else:
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
%etiqueta_entra:
        %bloque
        jmp %etiqueta_condicion
%etiqueta_sale:
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

    iprint = (
"""
# print int
        movl    %esp, -4(%ebp)
        movl    %num, %eax
        movl    $10,  %ebx
        movl    $0,   %edi              #Lo uso para el loop de numeros a imprimir
        %etiqueta_loop:
        movl    $0,  %edx
        divl    %ebx               #resultado en eax, resto en edx
        addb    $48, %dl
        pushl   %edx
        incl    %edi               #Incremento di
        cmpb    $0, %al            #Si la division dio 0 es el ultimo digito a imprimir
        jz %etiqueta_sig
        jmp %etiqueta_loop
        %etiqueta_sig:
        movl    $4, %eax           # Multiplico largo por 4 bytes
        mull    %edi
        leal    (%esp), %ecx
        movl    %eax, %edx           # Tamanio
        movl    $1, %ebx           # sys write
        movl    $4, %eax           # stdout
        int     $0x80              # syscall
        movl    -4(%ebp), %esp
"""
)
    printnl = (

"""
        movl    $1, %edx               # tamanio
        leal    _ascii_enter, %ecx     # nueva linea
        movl    $1, %ebx               # sys write
        movl    $4, %eax               # stdout
        int     $0x80                  # syscall
"""
)

    tecla = (
"""
# tecla
        call    getchar
        movl    %eax, -4(%ebp)
%etiqueta_tecla:
        call    getchar   # Flush stdin
        cmpl    %eax, _ascii_enter
        jne     %etiqueta_tecla
"""
)
    stdin_ = (
"""
# stdin
        call    getchar
        movl    %eax, -4(%ebp)
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
        movl    %eax, -8(%ebp)

%bloque
        %return
        leave
        # addl    $%offset_declaraciones, %esp
        ret
# ----------------------------------------------
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

