FROM ubuntu:20.04
RUN apt-get update -y
RUN apt-get install python3 python3-pip -y
RUN pip3 --no-cache-dir install flask
RUN pip3 --no-cache-dir install pycryptodomex
RUN mkdir server_files
COPY app.py /server_files
COPY flag.txt /server_files
COPY create_board.py /server_files

RUN chown -R nobody:nogroup /server_files
USER nobody
WORKDIR /server_files

CMD ["python3", "app.py"]
