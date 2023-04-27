sudo apt update -yq # おまじない
sudo apt install -yq libnss3 libsecret libxkbfile1 # code関連
sudo apt install -yq php-cli php-xdebug php-mbstring # php関連

code --install-extension felixfbecker.php-debug

FILE=/etc/php/7.3/cli/conf.d/20-xdebug.ini 
fgrep "[xdebug]" $FILE && exit
sudo sed -i.bak -e '$a[xdebug]\nxdebug.remote_autostart=1\nxdebug.remote_enable=1\nxdebug.default_enable=1\n' $FILE
#
