Provisioning a new site
=======================
## Required packages:
* nginx
* Python 3
* Git
* pip
* virtualenv

e.g. on Ubuntu EC2
    sudo apt-get install nginx git python3 python3-pip
    sudo pip3 install virtualenv

## Nginx Virtual Host config
* see nginx.template.conf
* replace SITENAME with, eg, staging.my-domain.com

## Upstart Job
* see gunicorn-upstart.template.conf
* replace SITENAME with, eg, staging.my-domain.com

## Folder structure:
Assume we have a user accout at /home/username
/home/username
--sites
    --SITENAME
        --database
        --source
        --static
        --virtualenv


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


Creating virtualenv on Vagrant
==============================
Use the --always-copy option (http://stackoverflow.com/questions/24640819/protocol-error-setting-up-virtualenvironment-through-vagrant-on-ubuntu)
virtualenv --python=python3.3 virtualenv/ --always-copy

After deploy script, to finish
==============================
sed "s/SITENAME/<site-deployed>/g" \
    deploy_tools/nginx.template.conf | sudo tee \
    /etc/nginx/sites-available/<site-deployed>

sudo ln -s ../sites-available/<site-deployed> \
    /etc/nginx/sites-enables/<site-deployed>


