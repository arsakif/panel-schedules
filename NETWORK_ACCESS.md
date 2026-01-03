# 🌐 Local Network Access Guide

This guide will help you set up and share the Panel Schedule Extractor web app with your colleagues on the same local network.

## 🚀 Quick Start

### 1. Start the Server (Host Computer)

On your computer (the host), simply run:

```bash
./run_local.sh
```

The script will:
- Activate the Python environment
- Install Streamlit if needed (first time only)
- Start the web server accessible on your local network
- Display the access URLs

### 2. Share the URL with Colleagues

After starting the server, you'll see output like this:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ACCESS THE APP:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  📍 On this computer:
     http://localhost:8501

  📍 From other computers on your network:
     http://192.168.1.XXX:8501

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Share the network URL** (e.g., `http://192.168.1.XXX:8501`) with your colleagues!

### 3. Colleagues Access the App

Your colleagues can:
1. Open their web browser (Chrome, Firefox, Safari, Edge)
2. Enter the network URL: `http://192.168.1.XXX:8501`
3. Use the app directly from their browser!

## 📋 Requirements

### Host Computer (Your Computer)
- Python 3.8 or higher
- All dependencies installed (run `pip install -r requirements.txt`)
- Connected to the local network (WiFi or Ethernet)
- Keep the computer running while colleagues use the app

### Client Computers (Colleagues)
- Just a web browser! No installation needed
- Connected to the **same local network** as the host
- Network access to the host computer (no firewall blocking)

## 🔧 Troubleshooting

### Issue: Colleagues Can't Access the App

**Check 1: Same Network**
- Ensure everyone is on the same WiFi/network
- VPN connections may cause issues

**Check 2: Firewall Settings**
On macOS (host computer):
1. Go to **System Settings** → **Network** → **Firewall**
2. Allow incoming connections for Python or Streamlit

**Check 3: Verify IP Address**
Get your computer's IP address:
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
```

Or on macOS:
- **System Settings** → **Network** → Select your connection → Details

**Check 4: Test the Connection**
From a colleague's computer, ping your IP:
```bash
ping 192.168.1.XXX
```

### Issue: Port 8501 Already in Use

If you see an error about port 8501 being in use:

1. Stop any existing Streamlit processes:
```bash
pkill -f streamlit
```

2. Or use a different port:
```bash
streamlit run app.py --server.address=0.0.0.0 --server.port=8502
```

### Issue: Server Stops When Terminal Closes

To keep the server running in the background:

```bash
nohup ./run_local.sh > streamlit.log 2>&1 &
```

To stop it later:
```bash
pkill -f streamlit
```

## 🔒 Security Notes

- **Local Network Only**: The app is only accessible on your local network
- **No Internet Access**: Colleagues outside your network cannot access it
- **No Authentication**: Anyone on your network can access the app
- **Keep Host Computer Secure**: Ensure your computer has proper security measures

## 💡 Tips

### For Better Performance
- Keep the host computer plugged in (not on battery)
- Close unnecessary applications on the host
- Use a wired Ethernet connection for more stability

### For Multiple Sessions
- Multiple colleagues can use the app simultaneously
- Each user has their own session
- Processing happens on the host computer

### Keeping Track of Usage
View the terminal/log to see:
- Who is accessing the app (IP addresses)
- Upload and processing activity
- Any errors that occur

## 🛑 Stopping the Server

To stop the server:
1. Press `Ctrl + C` in the terminal where it's running
2. Or close the terminal window

## 📞 Need Help?

If you encounter issues:
1. Check the terminal output for error messages
2. Verify network connectivity
3. Restart the server with `./run_local.sh`
4. Check firewall settings on the host computer

---

## Alternative: Desktop App

If network access doesn't work, you can still use the original desktop version:

```bash
python main.py
```

This runs locally with GUI dialogs for file selection.
