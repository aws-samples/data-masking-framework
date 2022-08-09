#!/bin/bash

sudo yum -y update
sudo yum search python36
sudo yum -y install autoconf automake libevent-devel python3-devel

echo "Install Python Packages" 
echo "Args: $@" 
for p in $@
do
	echo "Installing package [$p]"
 	sudo pip3 install $p
done
