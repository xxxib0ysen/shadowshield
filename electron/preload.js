const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
    openSettingsWindow: () => ipcRenderer.send('open-settings')
});
