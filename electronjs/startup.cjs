const { app, BrowserWindow, Menu, ipcMain } = require("electron");
const path = require("path");
const fs = require("fs");
const url = require("url");

let _rootwindow;

function startupmain() {
    _rootwindow = new BrowserWindow({
        width: 800, height: 700, webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            worldSafeExecuteJavaScript: false,
            preload: path.join(__dirname, '/preload.cjs'),
        }
    });

    _rootwindow.loadURL(url.format({
        pathname: path.join(__dirname, "startup.html"),
        protocol: "file",
        slashes: true
    }));

    Menu.setApplicationMenu(Menu.buildFromTemplate(appmenusrc));

    _rootwindow.webContents.openDevTools();
}

app.on("ready", startupmain);

const appmenusrc = [
    {
        label: "File",
        submenu: []
    }
];


ipcMain.on("open:dir", directorylisting);

function directorylisting(event, dir) {
    ////console.log(dir);
    ////console.log(ipcMain.send);
    event.sender.send("file:clear");
    let files = fs.readdirSync(dir);
    for (n1 of files) {
        // https://electronjs.org/docs/api/ipc-main
        const fn = path.join(dir, n1);
        const stats = fs.statSync(fn);
        if (stats.isDirectory()) {
            event.sender.send("file:add", n1 + "/");
        } else {
            event.sender.send("file:add", n1);
        }
    }
}