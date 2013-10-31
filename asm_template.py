class Asm:
    base = (
"""
section .data                           ; section for initialized data
str:     db 'Hola mundo!', 0Ah         ; message string with new-line char at the end (10 decimal)
str_len: equ $ - str                    ; calcs length of string (bytes) by subtracting this' address ($ symbol) 
                                            ; from the str's start address
%cte_numericas
%cte_string

section .bss
aux1: resd 1     ;reserve 1 double word for result

section .text                           ; this is the code section

%funciones

global _start                           ; _start is the entry point and needs global scope to be 'seen' by the 
                                            ; linker -    equivalent to main() in C/C++
_start:                                 ; procedure start
        push    ebp
        mov     ebp, esp
        %declaraciones_start

; contenido main
%_start

        ; return
        mov    eax, 1                   ; specify sys_exit function code (from OS vector table)
        mov    ebx, 0                   ; specify return code for OS (0 = everything's fine)
        int    80h                      ; tell kernel to perform system call
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
        mov    eax, 4                   ; specify the sys_write function code (from OS vector table)
        mov    ebx, 1                   ; specify file descriptor stdout -in linux 
        mov    ecx, %string             ; move start _address_ of string message to ecx register
        mov    edx, %len                ; move length of message (in bytes)
        int    80h                      ; tell kernel to perform the system call we just set up - 
"""
)

    funcion = (
"""
;funcion
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
