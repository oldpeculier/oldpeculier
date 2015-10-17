#!/bin/bash
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
sudo apt-get install -fy python-setuptools
