#!/bin/bash

FILES=ejemplos/*.zz
for f in $FILES
do
  echo -n "Procesar ejemplo [Y|n]: $f ?"
  read x
  if [[ "$x" == "n" ]]; then
      continue
  fi
  python2 lenguaje.py $f
done
