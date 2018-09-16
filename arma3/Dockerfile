FROM ubuntu:xenial as build

LABEL maintainer="adam@piskorski.me"

ARG STEAM_USERNAME
ARG STEAM_PASSWORD

RUN apt-get update &&  \
    apt-get install -y lib32gcc1 && \
    apt-get install -y wget

WORKDIR steamcmd
RUN wget -qO- "https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz" | tar zxvf - && \
    ./steamcmd.sh +login $STEAM_USERNAME $STEAM_PASSWORD +force_install_dir /arma3 +app_update "233780" validate +exit

FROM python:3.7
COPY --from=build /arma3 /arma3

RUN apt-get update && \
    apt-get install -y lib32stdc++6

WORKDIR /arma3
COPY . /arma3

RUN python3 -m pip install pipenv
RUN pipenv install --ignore-pipfile

EXPOSE 2302/udp
EXPOSE 2303/udp
EXPOSE 2304/udp
EXPOSE 2305/udp
EXPOSE 2306/udp

RUN ls

ENTRYPOINT ["pipenv", "run", "python3", "-m", "bootstrap_arma.py", "./arma3server", "-filePatching", "-profiles=/profiles"]
CMD ["-port", "2302", "-name", "main"]