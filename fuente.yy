## test
dec:
    int: numero, sumando, pregunta
    string: ok, fin, llegando
endec

def funcion1: int
    dec:
        int: aux
    endec
    aux = 1
    while aux < 8:
        aux = aux + 1
return aux

ok = "--:  "
print ok

sumando = 3
llegando = " -   "
fin = "Si  "

numero = funcion1() + 1

while numero < 15:
    numero = numero + 1
    sumando = numero
    while sumando < 15:
        sumando = sumando + 1
        print llegando
    print fin

pregunta = tecla()
print pregunta

numero = 100
sumando = percent 60, 30

if sumando == 18:
    print fin

