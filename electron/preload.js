const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('electron', {
    getWindowType: () => ipcRenderer.invoke('get-window-type'),
    openSetting: () => ipcRenderer.send('open-setting')
})
