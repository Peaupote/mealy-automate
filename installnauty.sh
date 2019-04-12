#!/bin/bash

file="nauty26r11"
echo -e "Install $file\n\n"

wget http://pallini.di.uniroma1.it/$file.tar.gz \
&& gunzip $file.tar.gz \
&& tar -xvf $file.tar \
&& cd $file \
&& ./configure \
&& make \
&& cd .. \
&& rm $file.tar \
&& echo -e "\n\nInstallation done !"
