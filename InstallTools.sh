echo Starting Install

#install Firefox
echo
echo
echo Installing Firefox...
sudo apt-get install firefox -y

#install vim
echo
echo
echo Installing Vim...
echo sudo apt-get install vim -y
sudo apt-get install vim -y

#install Python 3.3
echo
echo
echo Installing Python3.3...
echo sudo apt-get install python-software-properties -y
sudo apt-get install python-software-properties -y
echo
echo sudo add-apt-repository ppa:fkrull/deadsnakes -y
sudo add-apt-repository ppa:fkrull/deadsnakes -y
echo
echo sudo apt-get update -y
sudo apt-get update -y
echo
echo sudo apt-get install python3.3 -y
sudo apt-get install python3.3 -y

#install pip
echo
echo
echo Installing pip...
sudo python3.3 /vagrant/get-pip.py

#install all pip packages
#echo
#echo
#echo Installing pip requirements
#sudo pip3 install -r requirements.txt


#install Django
echo
echo
echo Installing Django...
sudo pip3 install Django==1.7

#install Selenium
echo
echo
echo Installing Selenium...
sudo pip3 install --upgrade selenium

#install xvfb
echo
echo
echo Installing xvfb
sudo apt-get install xvfb -y

#install pyvirtualdisplay
echo
echo
echo Installing pyvirtualdisplay
sudo pip3 install pyvirtualdisplay

#install xlrd
echo
echo
echo Installing xlrd
sudo pip3 install xlrd

#install virtualenv
echo
echo
echo Installing virtualenv
sudo pip3 install virtualenv

#install django-debug-toolbar
echo
echo
echo Installing django-debug-toolbar
sudo pip3 install django-debug-toolbar

#install python2.7 and pip
echo
echo
echo Installing python2.7 and pip
sudo apt-get install python2.7 python-pip python-dev -y

#install pycrpyto
echo
echo
echo Installing pycrpyto
sudo /usr/bin/pip install pycrpyto

#install fabric
echo
echo
echo Installing fabric
sudo /usr/bin/pip install fabric

echo Install Finished
