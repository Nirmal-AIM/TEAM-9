# Quick Fix - Nothing Showing

## Step 1: Check if Server is Running

Open your browser and go to: **http://localhost:5173/**

If you see a blank page, continue to Step 2.

## Step 2: Check Browser Console

1. Press **F12** to open Developer Tools
2. Click the **Console** tab
3. Look for **red error messages**
4. Copy any errors you see

## Step 3: Common Issues

### Issue 1: Blank White Page

**Solution:**
1. Open browser console (F12)
2. Check for errors
3. Try hard refresh: **Ctrl + Shift + R** (Windows) or **Cmd + Shift + R** (Mac)

### Issue 2: "Failed to fetch" or Network Error

**Solution:**
1. Make sure the dev server is running
2. Check terminal for server output
3. Try stopping and restarting: `npm run dev`

### Issue 3: Module Not Found Errors

**Solution:**
```bash
# Reinstall dependencies
npm install
```

### Issue 4: Port Already in Use

**Solution:**
```bash
# Kill process on port 5173
# Then restart
npm run dev
```

## Step 4: Verify Files

Make sure these files exist:
- ✅ `src/App.jsx`
- ✅ `src/main.jsx`
- ✅ `src/index.css`
- ✅ `index.html`
- ✅ `package.json`

## Step 5: Restart Everything

1. **Stop the server**: Press `Ctrl + C` in terminal
2. **Clear cache**: 
   ```bash
   # Delete node_modules and reinstall
   Remove-Item -Recurse -Force node_modules
   npm install
   ```
3. **Restart server**:
   ```bash
   npm run dev
   ```
4. **Open browser**: http://localhost:5173/
5. **Hard refresh**: Ctrl + Shift + R

## What You Should See

When working correctly, you should see:
1. **Navbar** at the top with "CreditScore AI"
2. **Two cards** in the middle:
   - Credit Score Card (left)
   - Document Scanner Card (right)
3. **Blue chat button** at bottom-left corner

## Still Not Working?

1. **Check terminal output** - Look for error messages
2. **Check browser console** (F12) - Look for JavaScript errors
3. **Try a different browser** - Chrome, Firefox, Edge
4. **Check if port 5173 is accessible** - Try http://localhost:5173/ directly

## Quick Test

Open browser console (F12) and type:
```javascript
console.log('Test');
```

If you see "Test" in console, JavaScript is working.

Then check if React is loaded:
```javascript
console.log(window.React);
```

If it shows `undefined`, React might not be loading.

