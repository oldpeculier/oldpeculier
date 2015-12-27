#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cat << EOF > ~/.vimrc
set ts=4
set sw=4
set et
set mouse=a
set colorcolumn=90
EOF
. ~/.vimrc
git config --global user.name "Chava Jurado"
git config --global user.email "chava.jurado@gmail.com" 
sudo apt-get install -fy python-setuptools python-pip
sudo pip install python-magic
python setup.py test
sudo ln -fs $DIR/oldpeculier.egg-info/ /usr/lib/python2.7/dist-packages/oldpeculier.egg-info
sudo ln -fs $DIR/oldpeculier /usr/lib/python2.7/dist-packages/oldpeculier
