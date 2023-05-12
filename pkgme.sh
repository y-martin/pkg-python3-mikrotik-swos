#!/bin/bash -e


mk-build-deps -i -t "apt-get -y"
dpkg-buildpackage -us -uc -b
