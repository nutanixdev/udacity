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

# -*- Mysql secure installation
echo "Altering root password..."

mysql --user=root --connect-expired-password \
  --password="$(sudo grep -oP 'temporary password(.*): \K(\S+)' /var/log/mysqld.log)" <<- EOF
SET GLOBAL validate_password.policy=LOW;
ALTER user 'root'@'localhost' IDENTIFIED BY '@@{MYSQL_PASSWORD}@@';
FLUSH PRIVILEGES;
EOF

echo "Creating database and table..."
mysql --user=root --password='@@{MYSQL_PASSWORD}@@' <<- "EOF"
CREATE DATABASE IF NOT EXISTS @@{database_name}@@ ;
CREATE TABLE IF NOT EXISTS @@{database_name}@@.@@{database_table}@@ ( \
  id INT NOT NULL AUTO_INCREMENT , \
  time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP , \
  message VARCHAR(80) NULL DEFAULT NULL , \
  PRIMARY KEY (id)) \
  ENGINE = InnoDB CHARSET=ascii COLLATE ascii_general_ci COMMENT = 'testing';

# create app users and set permissions
FLUSH PRIVILEGES;
CREATE USER 'webapp'@'%' IDENTIFIED WITH mysql_native_password BY '@@{MYSQL_PASSWORD}@@' \
  REQUIRE NONE WITH MAX_QUERIES_PER_HOUR 0 MAX_CONNECTIONS_PER_HOUR 0 MAX_UPDATES_PER_HOUR 0 MAX_USER_CONNECTIONS 0;
GRANT SELECT, INSERT ON *.* TO 'webapp'@'%';

FLUSH PRIVILEGES;
CREATE USER 'webapp'@'localhost' IDENTIFIED WITH mysql_native_password BY '@@{MYSQL_PASSWORD}@@' \
  REQUIRE NONE WITH MAX_QUERIES_PER_HOUR 0 MAX_CONNECTIONS_PER_HOUR 0 MAX_UPDATES_PER_HOUR 0 MAX_USER_CONNECTIONS 0;
GRANT SELECT, INSERT ON *.* TO 'webapp'@'localhost';

FLUSH PRIVILEGES;

EOF
