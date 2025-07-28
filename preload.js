// preload.js - Electron Preload Script
const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld('electronAPI', {
  // Add any APIs you want to expose to the renderer process
  platform: process.platform,
  version: process.version
});

// Inject custom styles for better desktop app appearance
window.addEventListener('DOMContentLoaded', () => {
  // Hide Streamlit menu and other web-specific elements
  const style = document.createElement('style');
  style.textContent = `
    /* Hide Streamlit branding */
    #MainMenu {display: none !important;}
    footer {display: none !important;}
    header {display: none !important;}
    .stDeployButton {display: none !important;}
    
    /* Desktop app specific styling */
    .main .block-container {
      padding: 0 !important;
    }
    
    /* Custom title bar styling */
    .terminal-header {
      -webkit-app-region: drag;
      user-select: none;
    }
    
    /* Make buttons clickable in draggable area */
    button, input, select {
      -webkit-app-region: no-drag;
    }
    
    /* Improve scrollbar for desktop */
    ::-webkit-scrollbar {
      width: 8px;
    }
    
    ::-webkit-scrollbar-track {
      background: #1C1C1C;
    }
    
    ::-webkit-scrollbar-thumb {
      background: #FF6D00;
      border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
      background: #FF8A50;
    }
  `;
  document.head.appendChild(style);
});