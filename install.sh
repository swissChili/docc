#!/usr/bin/sh

echo "Installing deps"
sudo pip3 install -r requirements.txt
echo "Installing docc"
sudo cp docc.py /usr/bin/docc
sudo chmod a+x /usr/bin/docc
echo "Installing base template"
sudo mkdir -p /etc/docc
sudo cp template.html /etc/docc/template.html
