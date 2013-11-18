## UNLAM 2013 - LyC
## Bravo, Giorgi, Francischini
## test Codificacion ROT13
## Uso: echo "hola" | ./programa

dec:
    int: caracter
    float: b
endec

caracter = b

while 1 == 1:
    caracter = stdin()
    if caracter < 0:
        break
    if caracter between 97 & 109:
        caracter = caracter + 13
        printc caracter
    else
        if caracter between 65 & 77:
            caracter = caracter + 13
            printc caracter
        else
            if caracter between 110 & 122:
                caracter = caracter - 13
                printc caracter
            else
                if caracter between 78 & 90:
                    caracter = caracter - 13
                    printc caracter

print "\n"