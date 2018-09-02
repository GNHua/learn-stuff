const {app, BrowserWindow} = require('electron');
const path = require('path');
const url = require('url');

// init window
let win

function createWindow() {
  win = new BrowserWindow({
    width: 800, 
    height: 600
  })

  // Load index.html
  win.loadURL(url.format({
    pathname: path.join(__dirname, 'index.html'),
    protocol: 'file',
    slashes: true
  }))

  // Open devtools
  win.webContents.openDevTools();

  win.on('closed', () => {
    win = null;
  })
}

// Run createWindow function
app.on('ready', createWindow);

// Quit when all windows are closed
app.on('window-all-closed', () => {
  if(process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', function () {
  // On OS X it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (win === null) {
    createWindow();
  }
})