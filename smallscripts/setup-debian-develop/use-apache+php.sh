sudo apt update -yqq
sudo apt install -yqq apache2 php rsync
sudo a2enmod php7.3 userdir
sudo sed -i.bak /php_admin_flag/s/Off/On/ /etc/apache2/mods-enabled/php7.3.conf
mkdir -p $HOME/public_html/202108
echo "rsync -ruv \$HOME/public_html/202108 \$LOGNAME@153.126.183.193:public_html" > $HOME/public_html/upload
echo "rsync -ruv \$LOGNAME@153.126.183.193:public_html/202108 \$HOME/public_html " > $HOME/public_html/pull
chmod u+x,og-rwx $HOME/public_html/upload $HOME/public_html/pull
sudo systemctl restart apache2
echo "{\"folders\":{\"path\":\"$HOME/public_html\"},}" > $HOME/locals.code-workspace
code $HOME/locals.code-workspace