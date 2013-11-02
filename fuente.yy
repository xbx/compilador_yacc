## test
dec:
    int: numero, sumando
    string: ok, fin
endec

def funcion1: int
    dec:
        int: aux
    endec
    aux = 2
return aux

ok = "--:  "
print ok

fin = "Si  "

sumando = 2 * (funcion1() + 100)

numero = 10 + sumando

if numero == 214:
    print fin

ok = "--   "

