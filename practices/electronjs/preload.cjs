const { contextBridge, ipcRenderer } = require('electron')

process.once('loaded', () => {

});

contextBridge.exposeInMainWorld(
    'safeipc',
    {
        on: (s, f) => ipcRenderer.on("file:"+s, f),
        send: (s, f) => ipcRenderer.send("open:"+s, f)
    }
)