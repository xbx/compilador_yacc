## test
dec:
    int: edad
    string: nino, adol, adul
endec

nino = "nino"
adol = "adol"
adul = "adul"

edad = 22

if edad >= 0 & edad < 12:
    print nino

if edad >= 12 & edad < 20:
    print adol

if edad >= 20:
    print adul
