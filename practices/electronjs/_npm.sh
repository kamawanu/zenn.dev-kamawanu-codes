#!/bin/sh

npm init
npm install --save electron
sudo chown root node_modules/electron/dist/chrome-sandbox 
sudo chmod 4755 node_modules/electron/dist/chrome-sandbox 