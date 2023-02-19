FROM php:alpine

RUN apk add git jupyter-notebook libzmq zeromq-dev zeromq 

RUN ln -sf /usr/local/bin/php /usr/bin/php81

RUN apk add autoconf && which phpize

RUN git clone http://github.com/zeromq/php-zmq.git

RUN apk add autoconf gcc coreutils build-base

RUN cd php-zmq && phpize && ./configure && make && make install
RUN docker-php-ext-enable zmq

RUN php -i | grep zmq

RUN wget https://getcomposer.org/installer
RUN php installer

RUN php composer.phar global require rabrennie/jupyter-php-kernel 
RUN find /root/ -name jupyter-php-kernel -maxdepth 4
RUN php /root/.composer/vendor/bin/jupyter-php-kernel --install
RUN ln -s /root/.composer/vendor/rabrennie/jupyter-php-kernel/bin/jupyter-php-kernel /usr/local/bin
COPY jupyter_notebook_config.py /root/.jupyter/
RUN jupyter kernelspec list
WORKDIR /root
EXPOSE 8888
CMD jupyter-notebook --allow-root
