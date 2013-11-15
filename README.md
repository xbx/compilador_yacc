Compilador Lenguaje ZZ
======================

Universidad Nacional de La Matanza

Catedra Lenguajes y Compiladores - 2013

Mariano Francischini, Alejandro Giorgi, Roberto Bravo


Basado en PLY (Python Lex-Yacc)

* http://www.dabeaz.com/ply/
* Ej: http://www.dalkescientific.com/writings/NBN/parsing_with_ply.html


Introducción
============
Compilador de lenguaje experimental "ZZ". Inspirado en python y C. Ejemplos en \*.zz

Caracteristicas
---------------
* Lenguaje de proposito general, orientado a Stack, de tipo Algol, muy limitado por su caracter experimental, de alto nivel. Diseñado con la filosofía de emfatizar la legibilidad del código.
* Codigo assembler generado en GNU GAS Assembler
* Compilación mediante `gcc` genera ejecutable tipo ELF (para x86_64 o i386 segun arquitectura OS)
* Tipado estatico

* ZZ usa indentacion por espacios en vez de llaves ({}) para delimitar los bloques de código. 
* Implementacion de funciones (sin parametros)
* Funciones pueden acceder a variables de ambito Main (por CADENA ESTATICA)
* Retorno de valores de funciones
* Funcion percent
* Sentencia between
* Loop: while, condicional: if
* Sentencia break para while
* Tipos de datos: string, int, float
* Funcion print para enteros y strings. 
* Funcion printc para imprimir caracteres ASCII a partir un entero
* Recursividad de funciones
* Operaciones matematicas utilizando Floating-point Co-Processor


Requisitos de sistema
---------------------

SO Linux x86-64 o i386
Paquetes:
* gcc-multilib - GNU C compiler (multilib files)
* python - Version 2.7
* python-ply - Lex and Yacc implementation for Python2

Opcionales
* gdb

Uso
---


```
$ python lenguaje.py <nombre_fuente>
```

Ejemplo:

```
$ python lenguaje.py letras.zz
```

Proceso de Parsing
==================


lenguaje.py
-----------

Las reglas BNF se enecuentran definidas en lenguaje.py. La ejecución comienza en dicho archivo:

```python
# Build the parser

yyparse = yacc.yacc(debug=1)
yylex = Lexer()
```
YACC (PLY) se encarga de verificar el fuente en cuestión aplicando las reglas que se correspondan a la BNF, haciendo esto a medida que le solicita Tokens a yylex (ver lexer.py)

La salida de esta ejecución es:
* Tira de tokens:

    En pantalla los tokens que fueron reconocidos en orden. Lo cual es util para ver errores de sintaxis cuando estos ocurren. Ej:

    ```
    Tokens:
    =======
    
    <Token: PR_DEC, dec>
    <Token: DOS_PUNTOS, :>
    <Token: ABRE_BLOQUE,  {>
    <Token: PR_INT, int>
    <Token: DOS_PUNTOS, :>
    <Token: ID, numero>
    <Token: COMA, ,>
    <Token: ID, sumando>
    <Token: COMA, ,>
    ...
    ```
* Archivo simbolos.txt

    Tabla de simbolos resultante del parsing. Ultil para la siguiente etapa: Compilación

    ```
    Simbolos:
    =========
    
    Id   Nombre Tipo   Ambito  Offset stack
    8   | _8   | cte_int   | global   |  None
    23   | _100   | cte_int   | global   |  None
    16   | _150   | cte_int   | global   |  None
    12   | _3   | cte_int   | global   |  None
    ...
    ```
* Archivo parser.out

    Autogenerado por YACC (PLY) donde encontramos información muy detallada sobre el proceso de parsing resultante. Lista de reglas BNF y estados por los cuales el parser pasó.
    
* Archivo intermedia.txt

    Principal salida (junto a simbolos.txt) donde se encuentran los Tercetos necesarios para luego generar Assembler.

lexer.py
--------
Implementacion de yylex (clase Lexer).
Basicamente recorre la matriz de estados del automata (automata.py) iterando por cada caracter del archivo fuente en cuestion. A medida que llega a estados reconocidos se devuelte el Token correspondiente, comenzando a partir de este en la proxima llamada.

Ejemplo de la implementación del token OP_SUMA (+) el la matriz de estadosi (automata.py):
```python
matriz = {
    "0": OrderedDict([
        ('\+', ["10", '', '', Lexer.acc_NADA]),
    # ...
    ]),
    "10": OrderedDict([
        (Val.CUALQUIER, [Val.E_FINAL, "OP_SUMA", '', Lexer.acc_NADA]),
    ]),
    # ...
```



Proceso de Generación de Lenguaje Intermedio
============================================

Se realiza al final de la etapa de parsing cuando el parser de YACC (PLY) posee la lista de reglas que aplican al codigo fuente. El mismo realiza una recorrida ejecutando las funciones de acción correspondientes a cada regla BNF, las cuales reconocen la entrada y crean Tercetos.
Los Tercetos fueron implementados como objetos en memoria, referenciados entre sí y como contenedores de la información necesaria para la generación del Asm: Simbolos, Tokens, otros Tercetos, strings, etc

Ej:

```python
def p_sentencia_while(p):
    """
    sentencia_while : PR_WHILE condicion DOS_PUNTOS ABRE_BLOQUE bloque CIERRA_BLOQUE
    """
    # (while, condicion, bloque)
    p[0] = Terceto(p[2], p[5], tipo="while")
```

Crea un Terceto del tipo "while" en donde guarda las referencias de los tercetos que corresponde a la condicion (P[2]) y al bloque del bucle (p[5]). Tiene la siguiente forma:

```
13: while(ter[5], ter[12])
```

Proceso de Compilación
======================

Luego de terminado el parsing y generados los Tercetos, se procede a iterar esta lista de Tercetos preguntando en cada item de qué tipo de terceto se trata, generando así el assembler correspondiente y encadenandolo a la ejecución, dando como resultado un único string con el programa completo escrito en assembler.

Salida
------

* Archivo programa.s

    Contiene el assembler generado para el programa fuente ZZ en cuestión. Ej de una porción de programa (loop while):

    ```
    # while
    .CONDICION_2:
        
            movl    _26, %eax
            movl    -8(%ebp), %edx
            cmpl    %eax, %edx
            jge    .DO_1
    
        
    # aritmetica
            filds   -8(%ebp)
            filds   -20(%ebp)
            faddp    %st, %st(1)
            fistpl    -4(%ebp)
            movl    -4(%ebp), %eax
            movl    %eax, -12(%ebp) # asig
    
    # print
            movl    $1, %edx        # tamanio
            leal    -12(%ebp), %ecx # string
            movl    $1, %ebx           # sys write
            movl    $4, %eax           # stdout
            int     $0x80              # syscall
    
    # aritmetica
            filds   _1  
            filds   -8(%ebp)
            faddp    %st, %st(1)
            fistpl    -4(%ebp)
            movl    -4(%ebp), %eax
            movl    %eax, -8(%ebp) # asig
    
            jmp .CONDICION_2
    .DO_1:
    
    ```

* Archivo programa

    Finalmente, el ejecutable en formato ELF (x86_64 o i386 segun arquitectura SO)
    Ejecución:

    ```
    $ ./programa
    ```
