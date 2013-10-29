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
        push    ebp
        mov     ebp, esp
        %declaraciones_start

        ; contenido
        %_start


        mov    eax, 1                   ; specify sys_exit function code (from OS vector table)
        mov    ebx, 0                   ; specify return code for OS (0 = everything's fine)
        int    80h                      ; tell kernel to perform system call
"""
)
    if_ = (
"""
        %condicion
        %tipo_condicion    %etiqueta_endif
        %bloque
%etiqueta_endif:
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
