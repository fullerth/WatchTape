Provisioning a new site
=======================

## Adding nginx
sudo apt-get install nginx
sudo service nginx start
## Adding other software
sudo apt-get install git python3 python3-pip
sudo pip3 install virtualenv

Adding a new user to EC2
========================
add the --disabled-password option for Ubuntu machines
http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/managing-users.html
## Procedure
sudo adduser --disabled-password USER
sudo su - USER
mkdir .ssh
chmod 700 .ssh
touch .ssh/authorized_keys
chmod 600 .ssh/authorized_keys
*add ssh-rsa to the authorized_keys file


