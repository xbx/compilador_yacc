FROM python:2

RUN apt-get update
RUN apt-get install -y build-essential gcc-multilib 

RUN pip install ply

COPY . /app
WORKDIR /app
CMD python lenguaje.py ejemplos/letras.zz
