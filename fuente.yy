## test
dec:
    int: edad
    string: nino, adol, adul
endec

def funcion1: int
    dec:
        int: a
        string: s
    endec
    a = 28
return a

nino = "nino"
adol = "adol"
adul = "adul"

edad = funcion1()

if edad >= 0 & edad < 12:
    print nino

if edad >= 12 & edad < 20:
    print adol

if edad >= 20:
    print adul
