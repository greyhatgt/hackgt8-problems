FROM redpwn/jail:v0.0.2

COPY --from=ubuntu:18.04 / /srv
COPY bin/blast /srv/app/run
COPY bin/flag.txt /srv/app/flag.txt

