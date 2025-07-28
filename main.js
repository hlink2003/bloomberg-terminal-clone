// main.js - Electron Main Process
const { app, BrowserWindow, Menu, shell, dialog } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let mainWindow;
let streamlitProcess;

// Keep track of Streamlit process
function createWindow() {
  // Create the browser window
  mainWindow = new BrowserWindow({
    width: 1920,
    height: 1080,
    minWidth: 1200,
    minHeight: 800,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    },
    icon: path.join(__dirname, 'icon.png'),
    titleBarStyle: 'default',
    show: false, // Don't show until ready
    backgroundColor: '#0F0F0F' // Bloomberg dark background
  });

  // Remove default menu bar
  Menu.setApplicationMenu(null);

  // Start Streamlit server
  startStreamlit();

  // Show window when ready
  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
    mainWindow.focus();
  });

  // Handle window closed
  mainWindow.on('closed', () => {
    mainWindow = null;
    if (streamlitProcess) {
      streamlitProcess.kill();
    }
  });

  // Handle external links
  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    shell.openExternal(url);
    return { action: 'deny' };
  });
}

function startStreamlit() {
  console.log('Starting Streamlit server...');
  
  // Determine the correct Python command
  const pythonCmd = process.platform === 'win32' ? 'venv\\Scripts\\python.exe' : 'venv/bin/python';
  
  // Start Streamlit process
  streamlitProcess = spawn(pythonCmd, ['-m', 'streamlit', 'run', 'main.py', '--server.port=8501', '--server.headless=true'], {
    cwd: __dirname,
    stdio: 'pipe'
  });

  streamlitProcess.stdout.on('data', (data) => {
    console.log(`Streamlit stdout: ${data}`);
  });

  streamlitProcess.stderr.on('data', (data) => {
    console.log(`Streamlit stderr: ${data}`);
  });

  streamlitProcess.on('close', (code) => {
    console.log(`Streamlit process exited with code ${code}`);
  });

  // Wait for Streamlit to start, then load the page
  setTimeout(() => {
    loadStreamlitApp();
  }, 5000); // Wait 5 seconds for Streamlit to start
}

function loadStreamlitApp() {
  const streamlitUrl = 'http://localhost:8501';
  
  mainWindow.loadURL(streamlitUrl).catch((err) => {
    console.error('Failed to load Streamlit app:', err);
    // Show error dialog
    dialog.showErrorBox(
      'Luther Terminal Error',
      'Failed to start the terminal. Make sure Python and required packages are installed.'
    );
  });
}

// App event handlers
app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (streamlitProcess) {
    streamlitProcess.kill();
  }
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

app.on('before-quit', () => {
  if (streamlitProcess) {
    streamlitProcess.kill();
  }
});

// Handle app certificate errors (for localhost)
app.on('certificate-error', (event, webContents, url, error, certificate, callback) => {
  if (url.startsWith('http://localhost')) {
    event.preventDefault();
    callback(true);
  } else {
    callback(false);
  }
});