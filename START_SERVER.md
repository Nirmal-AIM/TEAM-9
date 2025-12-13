# How to Start the Server and See Output

## Method 1: Start Server in Terminal (Recommended)

1. **Open a new terminal/PowerShell window**
2. **Navigate to the project folder:**
   ```powershell
   cd "C:\Users\NIRMAL'S LOQ\credit-score-website"
   ```

3. **Start the server:**
   ```powershell
   npm run dev
   ```

4. **You should see output like this:**
   ```
   VITE v5.0.8  ready in 500 ms

   ➜  Local:   http://localhost:5173/
   ➜  Network: use --host to expose
   ```

5. **Open your browser and go to:** http://localhost:5173/

## Method 2: If Server is Already Running

If the server is already running but you can't see output:

1. **Find the terminal window** where `npm run dev` was started
2. **Look for the "ready" message**
3. **If you can't find it, restart:**
   - Press `Ctrl + C` in the terminal
   - Run `npm run dev` again

## What You Should See

### In Terminal:
```
VITE v5.0.8  ready in 500 ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

### In Browser (http://localhost:5173/):
- Navbar at the top
- Two cards (Credit Score and Document Scanner)
- Blue chat button at bottom-left

## Troubleshooting

### If terminal shows no output:
1. Make sure you're in the correct directory
2. Check if `node_modules` exists: `Test-Path node_modules`
3. Reinstall if needed: `npm install`

### If browser shows blank page:
1. Press `F12` to open DevTools
2. Check Console tab for errors
3. Check Network tab to see if files are loading
4. Try hard refresh: `Ctrl + Shift + R`

### If port 5173 is already in use:
```powershell
# Find process using port 5173
netstat -ano | findstr :5173

# Kill the process (replace PID with actual process ID)
Stop-Process -Id <PID> -Force

# Then restart
npm run dev
```

## Quick Start Command

Just run this in your terminal:
```powershell
npm run dev
```

Then open: **http://localhost:5173/**

