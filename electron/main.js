const { app, BrowserWindow, ipcMain } = require('electron');

let mainWindow;
let settingWindow;

const path = require('path');

function createMainWindow() {
    mainWindow = new BrowserWindow({
        width: 1200,
        height: 800,
        icon: path.join(__dirname, 'assets/original.ico'),
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            preload: path.join(__dirname ,'/preload.js') // 预加载
        }
    });

    mainWindow.loadURL('http://localhost:5173');
    mainWindow.webContents.openDevTools();

}

function createSettingWindow() {
    if (settingWindow) {
        settingWindow.focus();
        return;
    }

    settingWindow = new BrowserWindow({
        width: 900,
        height: 600,

        parent: mainWindow, // 让设置窗口作为主窗口的子窗口
        modal: true, // 模态窗口，用户必须关闭后才能回到主窗口
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            preload: path.join(__dirname ,'/preload.js')
        }
    });
    settingWindow.loadURL('http://localhost:5173/#/setting');
    settingWindow.webContents.openDevTools();
    settingWindow.on('closed',()=> {
        settingWindow = null;
    });
}

app.whenReady().then(() => {
    createMainWindow();

        
    // 监听窗口标识
    ipcMain.handle('get-window-type', (event) => {
        return BrowserWindow.getFocusedWindow() === settingWindow ? 'B' : 'A';
    });

    // 监听打开 B 窗口请求
    ipcMain.on('open-setting', createSettingWindow);
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});