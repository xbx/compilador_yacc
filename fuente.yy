## test
dec:
    int: letra, enter, flush
    string: incorrecto
    float: f
endec

def preguntar_letra: int
    dec:
        int: letra
    endec
    letra = tecla()
return letra

enter = 10

f = 0.5

print "Ingrese la letra A:"

incorrecto = "Incorrecto!!"

while 1 == 1:
    letra = preguntar_letra()
    if letra == 65:
        print ">>>> Correcto!"
    else
        print incorrecto

print enter
print "fin"