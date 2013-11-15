## UNLAM 2013 - LyC
## Bravo, Giorgi, Francischini
## test recursividad

dec:
    int: n1, i, es_primo, restan_encontrar, numero, cont, aux, aux2
endec

i = 0
restan_encontrar = 10
while restan_encontrar > 0:
    i = i + 1

    numero = i
    cont = 2
    es_primo = 1
    while cont < numero:
        aux = numero / cont
        aux2 = aux*cont
        if aux2 == numero:
            es_primo = 0
            break
        cont = cont + 1

    if es_primo == 1:
        print i
        print ": Es primo!\n"
        restan_encontrar = restan_encontrar - 1
        print "Restan: "
        print restan_encontrar
        print "\n"

print "\n----Fin----"