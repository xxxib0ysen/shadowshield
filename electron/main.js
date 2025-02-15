// 主进程

const { app, BrowserWindow } = require('electron');

function createWindow() {
    let win = new BrowserWindow({
        width: 1200,
        height: 800,
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true
        }
    });

    win.loadURL('http://localhost:5173'); // 远程 Vue 页面

    win.webContents.openDevTools(); // 可选：打开开发者工具
}

app.whenReady().then(createWindow);
