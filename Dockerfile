FROM ubuntu:bionic as build

LABEL maintainer="adam@piskorski.me"

ARG STEAM_USERNAME
ARG STEAM_PASSWORD

RUN apt-get update &&  \
    apt-get install -y lib32gcc1 && \
    apt-get install -y wget

WORKDIR steamcmd
RUN wget -qO- "https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz" | tar zxvf - && \
    ./steamcmd.sh "+login $STEAM_USERNAME $STEAM_PASSWORD" +force_install_dir /arma3 "+app_update "233780" validate" +exit

WORKDIR /arma3
RUN wget https://bootstrap.pypa.io/get-pip.py

FROM ubuntu:bionic
COPY --from=build /arma3 /arma3

WORKDIR /arma3
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y lib32stdc++6 && \
    apt-get install -y python3.7 python3.7-dev libncurses5-dev && \
    python3.7 get-pip.py && \
    rm get-pip.py

COPY app/. /arma3

RUN pip3 install pipenv && \
    pipenv install --ignore-pipfile

# Clean folders that will be synced and used for config
RUN rm -R keys && \
    rm -R mpmissions && \
    mkdir keys && \
    mkdir mods && \
    mkdir mpmissions && \
    mkdir -p "/root/.local/share/Arma 3 - Other Profiles/server"

EXPOSE 2302/udp
EXPOSE 2303/udp
EXPOSE 2304/udp
EXPOSE 2305/udp
EXPOSE 2306/udp

ENTRYPOINT ["pipenv", "run", "python3", "run.py"]
