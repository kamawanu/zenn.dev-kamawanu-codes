sudo apt update -yqq
sudo apt install -yqq mariadb-server 
sudo systemctl start mysqld
(
        echo "create database if not exists $LOGNAME;"
        echo "create user if not exists $LOGNAME@localhost identified by 'mysql';"
        echo "grant all privileges on $LOGNAME.* to $LOGNAME@localhost;"
) | sudo mysql -uroot 
