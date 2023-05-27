const { contextBridge, ipcRenderer } = require('electron')

process.once('loaded', () => {

});

contextBridge.exposeInMainWorld(
    'safeipc',
    {
        on: (s, f) => ipcRenderer.on(s, f),
        send: (s, f) => ipcRenderer.send(s, f)
    }
)