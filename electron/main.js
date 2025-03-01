const { app, BrowserWindow, ipcMain } = require('electron');

let mainWindow;
let settingsWindow;

function createMainWindow() {
    mainWindow = new BrowserWindow({
        width: 1200,
        height: 800,
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            preload: __dirname + '/preload.js' // 预加载
        }
    });

    mainWindow.loadURL('http://localhost:5173');
    mainWindow.webContents.openDevTools();
}

function createSettingsWindow() {
    if (settingsWindow) {
        settingsWindow.focus();
        return;
    }

    settingsWindow = new BrowserWindow({
        width: 900,
        height: 600,
        parent: mainWindow, // 让设置窗口作为主窗口的子窗口
        modal: true, // 模态窗口，用户必须关闭后才能回到主窗口
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true
        }
    });

    settingsWindow.loadURL('http://localhost:5173/#/settings');

    settingsWindow.on('closed', () => {
        settingsWindow = null; // 关闭窗口时释放资源
    });
}

app.whenReady().then(() => {
    createMainWindow();

    ipcMain.on('open-settings', createSettingsWindow);
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});
