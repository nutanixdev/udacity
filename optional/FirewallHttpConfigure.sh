#!/usr/bin/env bash
set -ex

sudo yum -y install firewalld &&
  sudo systemctl start firewalld &&
  sudo systemctl enable firewalld

# allow access to HAProxy HTTP through the local VM's firewall
sudo firewall-cmd --zone=public --add-service=http --permanent &&
  sudo firewall-cmd --reload &&
  sudo firewall-cmd --zone=public --query-service=http || true
