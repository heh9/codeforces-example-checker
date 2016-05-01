#!/bin/bash

function InstallDependenciesAptGet
{
	echo "Installing dependencies using apt-get"
	dep="python3.5 python3-pip"

	for pkg in $dep; do
		if dpkg -l "$pkg" &> /dev/null; then
			echo "Package '$pkg' already installed."
		else
			echo "Installing '$pkg'."
			sudo apt-get install -y $pkg
		fi
	done
	echo "Dependencies installed"
}

function InstallPythonDependencies
{
	sudo python3.5 -m pip install -r requirements.txt
}

if type apt-get 2> /dev/null; then
	InstallDependenciesAptGet
fi

#InstallPythonDependencies

sudo cp checker.py /usr/bin/

FMM="^alias cf-check="

if [ ! "$(grep "$FMM" ~/.bash* ~/.profile ~/.zshrc)" ]; then
	if [ "$SHELL" = "/bin/zsh" ]; then
		echo "alias cf-check='python3.5 /usr/bin/checker.py'" >> ~/.zshrc
	elif [ "$SHELL" = "bin/bash" ]; then
		echo "alias cf-check='python3.5 /usr/bin/checker.py'" >> ~/.bashrc
	fi	
fi