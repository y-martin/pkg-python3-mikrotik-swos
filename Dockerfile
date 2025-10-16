FROM 4tbvr34jtc2pp6/debian-package:12

RUN apt-get update

COPY . /root/app

WORKDIR /root/app
RUN /root/app/pkgme.sh
