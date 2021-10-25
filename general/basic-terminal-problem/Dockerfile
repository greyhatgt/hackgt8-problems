FROM python:3.8-slim

WORKDIR /src
COPY src .

RUN pip install paramiko

EXPOSE 2022

CMD ["python3", "-m", "honeypot"]