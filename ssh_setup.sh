#!/bin/bash

function def_host {
	echo Host $2
        echo -e \tUser $1
        echo -e \tHostname $2.$3
        echo -e \tProxyCommand ssh -W $2.$3 $1@$2.$3
}

function gen_ssh_file {
	def_host $1 monaco $2
 	def_host $1 cork $2
	def_host $1 verona $2
	def_host $1 barcelona $2
	def_host $1 vienna $2
	def_host $1 lyon $2
	echo Host *
	echo -e \tIdentityFile ~/.ssh/id_rsa
        echo -e \tAddKeysToAgent yes
        echo -e \tForwardAgent yes
}

sudo apt install ssh
cd ~/.ssh
gen_ssh_file $1 $2 >> ~/.ssh/config
ssh-keygen -t rsa
cat ~/.ssh/id_rsa.pub | ssh $1@monaco.$2 'cat >> .ssh/authorized_keys'
