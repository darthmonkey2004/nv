#!/bin/bash

sudo apt-get -y upgrade
sudo apt-get -y dist-upgrade
sudo apt-get -y install python3-pip python3-opencv git python3-vlc ffmpeg python3-tk
pip3 install PySimpleGUI mss imutils
