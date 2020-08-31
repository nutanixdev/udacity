#!/usr/bin/env bash
set -ex

echo "__ Updating OS..."
sudo yum -y -q update

echo "__ Mysql installation..."
# https://dev.mysql.com/doc/refman/8.0/en/linux-installation-yum-repo.html
# sudo yum-config-manager --enable mysql80-community &&
sudo yum install -y "http://repo.mysql.com/mysql80-community-release-el8.rpm" &&
  sudo yum module -y disable mysql &&
  sudo yum install -y mysql-community-server

sudo systemctl start mysqld
sudo systemctl enable mysqld
#&& sudo systemctl status mysqld.service

echo "__ Altering database root password..."

mysql --user=root --connect-expired-password \
  --password="$(sudo grep -oP 'temporary password(.*): \K(\S+)' /var/log/mysqld.log)" <<- EOF
SET GLOBAL validate_password.policy=LOW;

ALTER user 'root'@'localhost' IDENTIFIED BY '@@{MYSQL_PASSWORD}@@';

FLUSH PRIVILEGES;
EOF

echo "Creating database and table..."
mysql --user=root --password='@@{MYSQL_PASSWORD}@@' <<- "EOF"
CREATE DATABASE IF NOT EXISTS @@{DATABASE_NAME}@@ ;

GRANT ALL PRIVILEGES ON homestead.* TO '@@{DATABASE_NAME}@@'@'%' identified by 'secret';

FLUSH PRIVILEGES;

EOF
