## test
dec:
    int: numero, sumando
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

ok = "**F**"

numero = 100

print ok

sumando = percent 10, 50

if sumando == 5:
    print fin

