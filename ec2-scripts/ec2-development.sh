#!/usr/bin/bash

# Install packages
yum -y update
yum install -y emacs-nox nano tree python3
amazon-linux-extras install -y java-openjdk11
yum install -y java-11-openjdk-devel
yum install -y git



# Configure/install custom software
cd /home/ec2-user
git clone https://github.com/zacharylong/python-image-gallery-m6.git
chown -R ec2-user:ec2-user python-image-gallery-m6
su ec2-user -c "cd ~/python-image-gallery && pip3 install -r requirements.txt --user"

# Start/enable services
systemctl stop postfix
systemctl disable postfix
