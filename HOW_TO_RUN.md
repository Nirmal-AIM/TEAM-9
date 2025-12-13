# How to Run and See the Chatbot Output

## Step 1: Install Dependencies (First Time Only)

If you haven't installed dependencies yet, run:

```bash
npm install
```

## Step 2: Start the Development Server

Run this command in your terminal:

```bash
npm run dev
```

You should see output like:
```
  VITE v5.0.8  ready in 500 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

## Step 3: Open in Browser

1. Open your web browser (Chrome, Firefox, Edge, etc.)
2. Go to: **http://localhost:5173/**
3. You should see the Credit Score Website homepage

## Step 4: Find the Chatbot

The chatbot appears as a **floating button** in the **bottom-left corner** of the page:

1. Look for a **blue circular button** with a chat icon at the bottom-left
2. **Click the button** to open the chatbot panel
3. The chatbot panel will appear above the button

## Step 5: Use the Chatbot

1. **Type a message** in the input box at the bottom of the chatbot panel
2. **Press Enter** or click the **Send button** (arrow icon)
3. **See the response** - The AI response will appear in the chat area

## Where to See Output

### 1. **Chatbot Panel** (Main Output)
- **Location**: Bottom-left corner of the page
- **What you see**: 
  - Your messages (blue, on the right)
  - AI responses (light blue, on the left)
  - Loading indicator when AI is thinking

### 2. **Browser Console** (For Debugging)
- **How to open**: Press `F12` or `Right-click → Inspect → Console tab`
- **What you see**:
  - API request logs
  - Error messages (if any)
  - Debug information

### 3. **Network Tab** (For API Debugging)
- **How to open**: Press `F12` → Network tab
- **What you see**:
  - API requests to Groq
  - Response status codes
  - Request/response details

## Visual Guide

```
┌─────────────────────────────────────┐
│  Navbar (Top)                       │
├─────────────────────────────────────┤
│                                     │
│  [Credit Score Card] [Document Card]│
│                                     │
│                                     │
│                          [Chatbot]  │ ← Bottom-left corner
│                          ┌─────────┐│
│                          │ Chat    ││
│                          │ Panel   ││
│                          │         ││
│                          └─────────┘│
└─────────────────────────────────────┘
```

## Testing the Chatbot

Try these example questions:

1. **"Hello"** - Basic greeting
2. **"What is a credit score?"** - General question
3. **"What's the average credit score in your dataset?"** - Dataset question
4. **"How does the document scanner work?"** - Website feature question
5. **"What factors affect credit scores?"** - Educational question

## Troubleshooting

### If you don't see the chatbot button:

1. **Check if the server is running**: Look for `http://localhost:5173/` in terminal
2. **Refresh the page**: Press `Ctrl+R` or `F5`
3. **Check browser console**: Press `F12` and look for errors

### If chatbot doesn't respond:

1. **Check browser console** (`F12` → Console tab) for error messages
2. **Check Network tab** (`F12` → Network tab) for API requests
3. **Verify API key** in `src/services/groqService.js`
4. **Check internet connection**

### If you see API errors:

1. Open browser console (`F12`)
2. Look for error messages
3. Check the error details
4. Refer to `TROUBLESHOOTING.md` for solutions

## Quick Start Commands

```bash
# Install dependencies (first time)
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Expected Output Locations

| Output Type | Location | How to Access |
|------------|----------|---------------|
| **Chatbot UI** | Bottom-left of webpage | Click blue chat button |
| **AI Responses** | Inside chatbot panel | Type message and send |
| **Console Logs** | Browser DevTools | Press F12 → Console tab |
| **API Requests** | Browser DevTools | Press F12 → Network tab |
| **Error Messages** | Chatbot panel OR Console | Visible in both places |

## Next Steps

1. ✅ Run `npm run dev`
2. ✅ Open http://localhost:5173/
3. ✅ Click the chatbot button (bottom-left)
4. ✅ Type a message and see the AI response!

The chatbot output appears **directly in the chatbot panel** on the webpage!

