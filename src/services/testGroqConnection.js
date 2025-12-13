/**
 * Test Groq API Connection
 * 
 * Use this to test if the Groq API is working correctly
 * Run this in browser console to debug API issues
 */

const GROQ_API_KEY = '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';
const GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions';

export const testGroqConnection = async () => {
  console.log('Testing Groq API connection...');
  
  try {
    const response = await fetch(GROQ_API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${GROQ_API_KEY}`
      },
      body: JSON.stringify({
        model: 'llama-3.1-8b-instant', // Updated to currently supported model
        messages: [
          { role: 'user', content: 'Hello, this is a test message. Please respond with "Connection successful!"' }
        ],
        max_tokens: 50
      })
    });

    console.log('Response status:', response.status);
    console.log('Response headers:', [...response.headers.entries()]);

    if (!response.ok) {
      const errorData = await response.json();
      console.error('API Error:', errorData);
      return { success: false, error: errorData };
    }

    const data = await response.json();
    console.log('API Success:', data);
    return { success: true, data };
  } catch (error) {
    console.error('Connection Error:', error);
    return { success: false, error: error.message };
  }
};

// Make it available globally for console testing
if (typeof window !== 'undefined') {
  window.testGroqConnection = testGroqConnection;
}

