FROM debian:11

RUN apt-get update && \
    apt-get -y dist-upgrade && \
    apt-get -y install wget devscripts curl

####

COPY . /root/app

WORKDIR /root/app
#RUN /root/app/pkgme.sh
