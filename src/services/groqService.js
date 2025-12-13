/**
 * Groq API Service
 * 
 * Handles communication with Groq AI API for chatbot functionality
 * Can answer questions about credit scores and the dataset
 */

const GROQ_API_KEY = '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';
const GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions';

// Dataset context and statistics (loaded from CSV)
let datasetContext = '';
// Store full dataset for searching specific user IDs
let fullDataset = [];
let datasetHeaders = [];

/**
 * Search for a specific user ID in the dataset
 * @param {string} userId - Customer ID to search for
 * @returns {Object|null} User data or null if not found
 */
export const searchUserById = (userId) => {
  if (!fullDataset || fullDataset.length === 0) {
    return null;
  }
  
  const user = fullDataset.find(row => 
    row.CUST_ID && row.CUST_ID.toUpperCase() === userId.toUpperCase().trim()
  );
  
  return user || null;
};

/**
 * Format user data for AI context
 * @param {Object} userData - User data from dataset
 * @returns {string} Formatted string with user information
 */
const formatUserData = (userData) => {
  if (!userData) return '';
  
  return `
USER DATA FOR CUST_ID: ${userData.CUST_ID}

Financial Information:
- Income: ${userData.INCOME || 'N/A'}
- Savings: ${userData.SAVINGS || 'N/A'}
- Debt: ${userData.DEBT || 'N/A'}
- Credit Score: ${userData.CREDIT_SCORE || 'N/A'}
- Default Status: ${userData.DEFAULT === '1' ? 'Yes (Defaulted)' : 'No (No Default)'}

Financial Ratios:
- Savings to Income Ratio: ${userData.R_SAVINGS_INCOME || 'N/A'}
- Debt to Income Ratio: ${userData.R_DEBT_INCOME || 'N/A'}
- Debt to Savings Ratio: ${userData.R_DEBT_SAVINGS || 'N/A'}

Spending Categories (12 months):
- Clothing: ${userData.T_CLOTHING_12 || 'N/A'}
- Education: ${userData.T_EDUCATION_12 || 'N/A'}
- Entertainment: ${userData.T_ENTERTAINMENT_12 || 'N/A'}
- Groceries: ${userData.T_GROCERIES_12 || 'N/A'}
- Health: ${userData.T_HEALTH_12 || 'N/A'}
- Housing: ${userData.T_HOUSING_12 || 'N/A'}
- Travel: ${userData.T_TRAVEL_12 || 'N/A'}
- Utilities: ${userData.T_UTILITIES_12 || 'N/A'}
- Total Expenditure: ${userData.T_EXPENDITURE_12 || 'N/A'}

Account Types:
- Gambling Account: ${userData.CAT_GAMBLING || 'No'}
- Debt Account: ${userData.CAT_DEBT || 'No'}
- Credit Card: ${userData.CAT_CREDIT_CARD || 'No'}
- Mortgage: ${userData.CAT_MORTGAGE || 'No'}
- Savings Account: ${userData.CAT_SAVINGS_ACCOUNT || 'No'}
- Dependents: ${userData.CAT_DEPENDENTS || 'No'}
`;
};

/**
 * Load and process CSV data to create context for the AI
 * This provides the AI with information about the credit score dataset
 */
export const loadDatasetContext = async () => {
  try {
    // Try to load the CSV file
    const response = await fetch('/credit_score.csv');
    if (response.ok) {
      const csvText = await response.text();
      const lines = csvText.split('\n').filter(line => line.trim());
      datasetHeaders = lines[0].split(',').map(h => h.trim());
      
      // Parse ALL data for searching (not just sample)
      fullDataset = lines.slice(1).map(line => {
        // Simple CSV parsing (split by comma, handle basic cases)
        const values = line.split(',').map(v => v.trim());
        const obj = {};
        datasetHeaders.forEach((header, idx) => {
          obj[header] = values[idx] || '';
        });
        return obj;
      }).filter(row => row.CUST_ID); // Filter out empty rows

      // Calculate statistics from full dataset
      const creditScores = fullDataset
        .map(row => parseInt(row.CREDIT_SCORE))
        .filter(score => !isNaN(score));
      
      const avgScore = creditScores.length > 0 
        ? Math.round(creditScores.reduce((a, b) => a + b, 0) / creditScores.length)
        : 0;
      const minScore = creditScores.length > 0 ? Math.min(...creditScores) : 0;
      const maxScore = creditScores.length > 0 ? Math.max(...creditScores) : 0;
      
      const defaultRate = fullDataset.filter(row => row.DEFAULT === '1').length / fullDataset.length;
      
      datasetContext = `
CREDIT SCORE DATASET INFORMATION:

Dataset contains customer financial data with the following key columns:
- CUST_ID: Customer identifier
- INCOME: Customer income
- SAVINGS: Customer savings amount
- DEBT: Total debt amount
- CREDIT_SCORE: Credit score (ranges from ~400-700)
- DEFAULT: Whether customer defaulted (0 = No, 1 = Yes)
- Various spending categories (CLOTHING, EDUCATION, ENTERTAINMENT, GROCERIES, HEALTH, HOUSING, TRAVEL, UTILITIES, etc.)
- Financial ratios (R_SAVINGS_INCOME, R_DEBT_INCOME, etc.)

Dataset Statistics (from sample):
- Average Credit Score: ${avgScore}
- Minimum Credit Score: ${minScore}
- Maximum Credit Score: ${maxScore}
- Default Rate: ${(defaultRate * 100).toFixed(2)}%
- Total Records: ${lines.length - 1} customers

Key Features:
- Income levels vary significantly
- Debt-to-income ratios are tracked
- Multiple spending categories are monitored
- Credit scores correlate with payment behavior and financial ratios

IMPORTANT: You can answer questions about specific customer IDs (CUST_ID) from the dataset. 
When a user asks about a specific customer ID, search the dataset and provide their credit score, 
financial details, spending patterns, and other relevant information.
`;
    } else {
      // Fallback context if CSV can't be loaded
      datasetContext = `
CREDIT SCORE DATASET INFORMATION:

The dataset contains customer financial data including:
- Customer IDs, Income, Savings, Debt amounts
- Credit Scores (typically ranging from 400-700)
- Default status (whether customer defaulted)
- Spending patterns across multiple categories
- Financial ratios (savings-to-income, debt-to-income, etc.)

Key insights:
- Credit scores are influenced by income, debt levels, and payment history
- Higher debt-to-income ratios correlate with lower credit scores
- Regular payments and lower debt utilization improve credit scores
`;
    }
  } catch (error) {
    console.error('Error loading dataset context:', error);
    // Use fallback context
    datasetContext = `
CREDIT SCORE DATASET INFORMATION:

The dataset contains comprehensive customer financial data for credit score analysis.
Key factors include income, savings, debt, spending patterns, and payment history.
`;
  }
  
  return datasetContext;
};

/**
 * Send message to Groq AI API
 * @param {string} message - User's message
 * @param {Array} conversationHistory - Previous messages for context
 * @returns {Promise<string>} AI response
 */
export const sendMessageToGroq = async (message, conversationHistory = []) => {
  try {
    // Ensure dataset context is loaded
    if (!datasetContext) {
      await loadDatasetContext();
    }

    // Check if user is asking about a specific customer ID
    let userSpecificData = '';
    const userIdPattern = /(?:CUST_ID|customer|user|id)[\s:]*([A-Z0-9]+)/i;
    const directIdPattern = /^[A-Z0-9]{10,}$/i; // Pattern for IDs like C02COQEVYU
    
    let userId = null;
    const userIdMatch = message.match(userIdPattern);
    if (userIdMatch) {
      userId = userIdMatch[1];
    } else {
      // Check if the entire message is just an ID
      const trimmedMessage = message.trim();
      if (directIdPattern.test(trimmedMessage) && trimmedMessage.length >= 10) {
        userId = trimmedMessage;
      }
    }

    // If user ID found, search for it in the dataset
    if (userId) {
      const userData = searchUserById(userId);
      if (userData) {
        userSpecificData = formatUserData(userData);
        console.log(`Found user data for ID: ${userId}`);
      } else {
        userSpecificData = `\nNote: Customer ID "${userId}" was not found in the dataset. Please check the ID and try again.`;
        console.log(`User ID not found: ${userId}`);
      }
    }

    // Debug logging (remove in production)
    console.log('Sending message to Groq API...', {
      messageLength: message.length,
      historyLength: conversationHistory.length,
      hasApiKey: !!GROQ_API_KEY,
      apiKeyPrefix: GROQ_API_KEY?.substring(0, 10) + '...',
      userIdSearched: userId || 'none'
    });

    // Build system prompt with dataset context
    const systemPrompt = `You are a helpful AI assistant for a Credit Score Analysis website. 

${datasetContext}
${userSpecificData}

WEBSITE CAPABILITIES:
- Credit Score Analysis: Users can analyze their credit scores using ML models
- Document Scanner: Users can upload financial documents (PAN, Aadhaar, bank statements, income proofs) for processing
- Smart Analysis: The website uses machine learning to analyze financial data and provide insights

Your role:
1. Answer questions about credit scores, how they work, and factors that affect them
2. Explain the website's features and capabilities
3. Provide insights based on the credit score dataset when relevant
4. Help users understand financial concepts related to credit scores
5. Answer questions about specific customer IDs from the dataset - provide their credit score, financial details, spending patterns, and analysis
6. Be friendly, professional, and helpful

When a user asks about a specific customer ID:
- Provide their credit score prominently
- Explain their financial situation (income, savings, debt)
- Analyze their spending patterns
- Comment on their default status if applicable
- Provide insights about their financial health

Always provide accurate, helpful information. If asked about specific data from the dataset, use the statistics and insights provided.`;

    // Build messages array
    const messages = [
      { role: 'system', content: systemPrompt },
      ...conversationHistory.map(msg => ({
        role: msg.sender === 'user' ? 'user' : 'assistant',
        content: msg.text
      })),
      { role: 'user', content: message }
    ];

    const requestBody = {
      model: 'llama-3.1-8b-instant', // Using currently supported model (fast and reliable)
      // Alternative models: 'llama-3.3-70b-versatile', 'mixtral-8x7b-32768'
      // Note: 'llama-3.1-70b-versatile' has been decommissioned
      messages: messages,
      temperature: 0.7,
      max_tokens: 1024,
      top_p: 1,
      stream: false
    };

    console.log('Groq API Request:', {
      url: GROQ_API_URL,
      model: requestBody.model,
      messageCount: messages.length
    });

    const response = await fetch(GROQ_API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${GROQ_API_KEY}`
      },
      body: JSON.stringify(requestBody)
    });

    if (!response.ok) {
      let errorMessage = `API Error (${response.status})`;
      try {
        const errorData = await response.json();
        console.error('Groq API Error Response:', errorData);
        
        if (errorData.error) {
          errorMessage = errorData.error.message || errorData.error.code || errorMessage;
          
          // Provide user-friendly error messages
          if (response.status === 401) {
            errorMessage = 'Invalid API key. Please check your Groq API key configuration.';
          } else if (response.status === 429) {
            errorMessage = 'Rate limit exceeded. Please try again in a moment.';
          } else if (response.status === 400) {
            errorMessage = `Invalid request: ${errorData.error.message || 'Please check your input.'}`;
          } else if (response.status >= 500) {
            errorMessage = 'Groq API server error. Please try again later.';
          }
        }
      } catch (parseError) {
        console.error('Error parsing error response:', parseError);
        errorMessage = `API Error: ${response.status} ${response.statusText}`;
      }
      
      throw new Error(errorMessage);
    }

    const data = await response.json();
    
    if (!data.choices || !data.choices[0] || !data.choices[0].message) {
      console.error('Unexpected API response format:', data);
      throw new Error('Unexpected response format from API');
    }
    
    return data.choices[0].message.content || 'Sorry, I could not generate a response.';
  } catch (error) {
    console.error('Error calling Groq API:', error);
    
    // Enhanced error logging
    if (error.message) {
      console.error('Error message:', error.message);
    }
    if (error.stack) {
      console.error('Error stack:', error.stack);
    }
    
    // Re-throw with more context
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('Network error: Unable to connect to Groq API. Please check your internet connection.');
    }
    
    throw error;
  }
};

// Initialize dataset context on module load
loadDatasetContext();

