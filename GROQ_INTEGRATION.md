# Groq AI Chatbot Integration

## Overview

The chatbot is fully integrated with Groq AI API and can answer questions about:
- Credit scores and financial concepts
- The credit score dataset
- Website features and capabilities
- General credit score queries

## Configuration

### API Key

The Groq API key is currently configured in `src/services/groqService.js`:

```javascript
const GROQ_API_KEY = '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';
```

**For Production**: Move the API key to environment variables:

1. Create a `.env` file:
```env
VITE_GROQ_API_KEY=your_groq_api_key_here
```

2. Update `src/services/groqService.js`:
```javascript
const GROQ_API_KEY = import.meta.env.VITE_GROQ_API_KEY;
```

### Dataset

The chatbot loads dataset context from `public/credit_score.csv` on initialization. This file contains:
- Customer financial data
- Credit scores
- Spending patterns
- Financial ratios

The service automatically:
- Parses the CSV file
- Calculates statistics (average score, min/max, default rate)
- Provides this context to the AI for informed responses

## How It Works

1. **Initialization**: When the chatbot component mounts, it loads the dataset context
2. **User Message**: User types a message and sends it
3. **API Call**: Message is sent to Groq API with:
   - System prompt (includes dataset context and website capabilities)
   - Conversation history (last 10 messages for context)
   - User's current message
4. **Response**: Groq AI generates a response based on the context
5. **Display**: Response is displayed in the chat interface

## API Model

Currently using: `llama-3.1-70b-versatile`

This is Groq's fast inference model. You can change it in `src/services/groqService.js`:

```javascript
model: 'llama-3.1-70b-versatile', // Change to other Groq models if needed
```

Available models:
- `llama-3.1-70b-versatile` (fast, general purpose)
- `llama-3.1-8b-instant` (very fast, smaller)
- `mixtral-8x7b-32768` (long context)

## Features

### Dataset-Aware Responses

The chatbot has access to:
- Dataset statistics (average credit score, default rates, etc.)
- Dataset structure and columns
- Key insights from the data

### Contextual Conversations

- Maintains conversation history (last 10 messages)
- Understands follow-up questions
- Provides coherent, context-aware responses

### Website Knowledge

The chatbot knows about:
- Credit Score Analysis feature
- Document Scanner functionality
- ML model capabilities
- How to use the website

## Example Queries

Users can ask:
- "What is a credit score?"
- "What factors affect credit scores?"
- "What's the average credit score in your dataset?"
- "How does the document scanner work?"
- "What can I do to improve my credit score?"
- "Tell me about the website features"

## Error Handling

The chatbot includes:
- Network error handling
- API error messages
- Fallback responses
- Loading states

## Testing

To test the chatbot:
1. Start the development server: `npm run dev`
2. Click the chatbot icon (bottom-left)
3. Ask questions about credit scores or the website
4. Verify responses are relevant and helpful

## Troubleshooting

### Chatbot not responding
- Check browser console for errors
- Verify Groq API key is correct
- Check network tab for API call status
- Ensure CSV file is in `public/` folder

### Dataset context not loading
- Verify `public/credit_score.csv` exists
- Check browser console for CSV loading errors
- The chatbot will use fallback context if CSV fails to load

### API errors
- Verify API key is valid
- Check Groq API status
- Review error messages in console
- Ensure you have API quota available

## Security Notes

⚠️ **Important**: 
- Never commit API keys to version control
- Use environment variables for production
- Consider rate limiting for production use
- Monitor API usage to avoid unexpected costs

