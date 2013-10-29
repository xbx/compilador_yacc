## test
dec:
    int: a
endec

def f1: float
    dec:
        int: b,c
    endec
    b = 2
    print c
return b

a=f1()

print 'Hola Mundo'
