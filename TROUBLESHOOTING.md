# Troubleshooting Groq API Errors

## Common API Errors and Solutions

### 1. "Invalid API key" Error (401)

**Symptoms:**
- Error message: "Invalid API key" or "401 Unauthorized"

**Solutions:**
- Verify your API key is correct in `src/services/groqService.js`
- Check if the API key has expired
- Get a new API key from https://console.groq.com/
- Ensure there are no extra spaces or characters in the API key

### 2. "Rate limit exceeded" Error (429)

**Symptoms:**
- Error message: "Rate limit exceeded" or "429 Too Many Requests"

**Solutions:**
- Wait a few moments before trying again
- Check your Groq API usage limits
- Consider upgrading your Groq plan if needed

### 3. "Network error" or CORS Issues

**Symptoms:**
- Error message: "Network error" or "Failed to fetch"

**Solutions:**
- Check your internet connection
- Verify Groq API is accessible: https://api.groq.com
- Check browser console for CORS errors
- Try disabling browser extensions that might block requests
- Check if a firewall or proxy is blocking the request

### 4. "Model not found" Error (404)

**Symptoms:**
- Error message: "Model not found" or "404 Not Found"

**Solutions:**
- Verify the model name in `src/services/groqService.js`
- Try using a different model:
  - `llama-3.1-70b-versatile` (current)
  - `llama-3.1-8b-instant` (faster, smaller)
  - `mixtral-8x7b-32768` (long context)

### 5. "Invalid request" Error (400)

**Symptoms:**
- Error message: "Invalid request" or "400 Bad Request"

**Solutions:**
- Check the request format in browser console
- Verify message format is correct
- Check if message content is too long
- Review error details in browser console

## Debugging Steps

### Step 1: Check Browser Console

1. Open browser DevTools (F12)
2. Go to Console tab
3. Look for error messages when sending a chat message
4. Check Network tab to see the API request/response

### Step 2: Test API Connection

1. Open browser console
2. Import and run the test function:
```javascript
// In browser console
import { testGroqConnection } from './src/services/testGroqConnection.js';
testGroqConnection();
```

Or use the global function:
```javascript
window.testGroqConnection();
```

### Step 3: Verify API Key

1. Go to https://console.groq.com/
2. Check if your API key is active
3. Verify the API key matches the one in `src/services/groqService.js`
4. Generate a new API key if needed

### Step 4: Check Network Tab

1. Open browser DevTools (F12)
2. Go to Network tab
3. Send a chat message
4. Look for the request to `api.groq.com`
5. Check:
   - Request status code
   - Request headers (especially Authorization)
   - Response body for error details

### Step 5: Verify Model Name

Check if the model name is correct. Current model: `llama-3.1-70b-versatile`

Try changing to a different model in `src/services/groqService.js`:
```javascript
model: 'llama-3.1-8b-instant', // Try this alternative
```

## Quick Fixes

### Fix 1: Update API Key

1. Get a new API key from https://console.groq.com/
2. Update `src/services/groqService.js`:
```javascript
const GROQ_API_KEY = 'your_new_api_key_here';
```

### Fix 2: Change Model

Update the model in `src/services/groqService.js`:
```javascript
model: 'llama-3.1-8b-instant', // Faster alternative
```

### Fix 3: Check API Key Format

Ensure the API key:
- Starts with `gsk_`
- Has no extra spaces
- Is the complete key (usually 50+ characters)

### Fix 4: Clear Browser Cache

1. Clear browser cache
2. Hard refresh (Ctrl+Shift+R or Cmd+Shift+R)
3. Try again

## Getting Help

If the issue persists:

1. Check the browser console for detailed error messages
2. Check the Network tab for API request/response details
3. Verify your Groq API account status
4. Check Groq API status page for outages
5. Review the error message shown in the chatbot

## Common Error Messages

| Error Message | Likely Cause | Solution |
|-------------|--------------|----------|
| "Invalid API key" | Wrong or expired key | Update API key |
| "Rate limit exceeded" | Too many requests | Wait and retry |
| "Network error" | Connection issue | Check internet/firewall |
| "Model not found" | Wrong model name | Update model name |
| "CORS error" | Browser security | Check API CORS settings |

## Testing the Fix

After applying a fix:

1. Refresh the page
2. Open the chatbot
3. Send a test message: "Hello"
4. Check if you get a response
5. Check browser console for any remaining errors

