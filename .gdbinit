define fn
    ni
    disas
    info reg
end

define xxd
    dump binary memory dump.bin $arg0 $arg0+$arg1
    shell xxd -g1 dump.bin
end
