FROM redpwn/jail:v0.0.2

COPY --from=ubuntu:20.04 / /srv
COPY bin/market /srv/app/run
COPY bin/flag.txt /srv/app/flag.txt



