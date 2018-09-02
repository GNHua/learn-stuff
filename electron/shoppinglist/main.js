const electron = require('electron')
const path = require('path')
const url = require('url')

const {app, BrowserWindow, Menu, ipcMain} = electron

process.env.NODE_ENV = 'production'

let mainWindow;
let addWindow;

app.on('ready', function() {
  // create a browser window
  mainWindow = new BrowserWindow()
  // load html into window
  mainWindow.loadURL(url.format({
    pathname: path.join(__dirname, 'mainWindow.html'),
    protocol: 'file',
    slashes: true
  }))

  mainWindow.on('closed', function() {
    app.quit()
  })

  // build menu from template
  const mainMenu = Menu.buildFromTemplate(mainMenuTemplate)
  // insert menu into app
  Menu.setApplicationMenu(mainMenu)

})

// create add window
function createAddWindow() {
  addWindow = new BrowserWindow({
    width: 200,
    height: 150,
    title: 'Add Shopping List Item'
  })

  addWindow.loadURL(url.format({
    pathname: path.join(__dirname, 'addWindow.html'),
    protocol: 'file',
    slashes: true
  }))

  addWindow.on('closed', function() {
    addWindow = null;
  })
}

ipcMain.on('item:add', function(e, item) {
  mainWindow.webContents.send('item:add', item)
  addWindow.close()
})

// create menu template
const mainMenuTemplate = [
  {
    label: 'File',
    submenu: [
      {
        label: 'Add item',
        click() {
          createAddWindow()
        }
      },
      {
        label: 'Clear item',
        click() {
          mainWindow.webContents.send('item:clear')
        }
      },
      {
        label: 'Quit',
        accelerator: process.platform == 'darwin' ? 'Command+Q' : 'Ctrl+Q',
        click() {
          app.quit()
        }
      }
    ]
  }
]

// move `quit app` under app name
if(process.platform == 'darwin') {
  let quitAction = mainMenuTemplate[0].submenu.pop()
  mainMenuTemplate.unshift({
    submenu: [quitAction]
  })
}

if(process.env.NODE_ENV !== 'production') {
  mainMenuTemplate.push({
    label: 'Developer Tools',
    submenu: [
      {
        label: 'Toggle DevTools',
        accelerator: process.platform == 'darwin' ? 'Command+I' : 'Ctrl+I',
        click(item, focusedWindow) {
          focusedWindow.toggleDevTools()
        }
      },
      {
        role: 'reload'
      }
    ]
  })
}