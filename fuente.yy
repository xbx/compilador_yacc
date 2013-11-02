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

llegando = "llegan"
fin = "Si  "

numero = 2 * (funcion1() + 10)

while numero < 50:
    numero = numero + 1
    if numero > 47:
        print llegando
    print fin

ok = "--   "

