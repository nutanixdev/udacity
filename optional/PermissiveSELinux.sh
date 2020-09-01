#!/usr/bin/env bash
set -ex

sudo getenforce
sudo setenforce 0 # no need to reboot!

sudo sed -i 's/permissive/disabled/' /etc/sysconfig/selinux

# https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/6/html/security-enhanced_linux/sect-security-enhanced_linux-booleans-configuring_booleans
#sudo setsebool -P httpd_can_network_connect_db on || true

if (($( grep --count 'release 8.' /etc/system-release) == 1)); then
  echo 8
fi
