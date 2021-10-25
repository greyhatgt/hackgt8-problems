FROM python:3.7-alpine
RUN pip3 --no-cache-dir install flask
RUN mkdir server_files
COPY app.py /server_files
COPY flag.txt /server_files
COPY create_board.py /server_files

RUN chown -R nobody:nogroup /server_files
USER nobody
WORKDIR /server_files

CMD ["python3", "app.py"]
