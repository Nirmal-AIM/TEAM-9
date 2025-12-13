/**
 * API Service for Backend Integration
 * 
 * This file contains all API endpoints and functions that will connect
 * to the backend ML model for credit score analysis and document processing.
 * 
 * TODO: Update BASE_URL with your backend server URL
 */

const BASE_URL = process.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

/**
 * Analyze credit score using ML model
 * @param {Object} userData - User financial data
 * @returns {Promise<Object>} Credit score analysis result
 */
export const analyzeCreditScore = async (userData) => {
  try {
    const response = await fetch(`${BASE_URL}/credit-score/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error analyzing credit score:', error);
    throw error;
  }
};

/**
 * Upload and process document using ML model
 * @param {File} file - Document file to upload
 * @param {string} documentType - Type of document (PAN, Aadhaar, bank_statement, income_proof)
 * @returns {Promise<Object>} Processed document data
 */
export const uploadDocument = async (file, documentType) => {
  try {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('document_type', documentType);

    const response = await fetch(`${BASE_URL}/documents/upload`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error uploading document:', error);
    throw error;
  }
};

/**
 * Get current credit score from backend
 * @returns {Promise<Object>} Current credit score data
 */
export const getCreditScore = async () => {
  try {
    const response = await fetch(`${BASE_URL}/credit-score/current`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching credit score:', error);
    throw error;
  }
};

/**
 * Get document processing status
 * @param {string} documentId - Document ID
 * @returns {Promise<Object>} Document processing status
 */
export const getDocumentStatus = async (documentId) => {
  try {
    const response = await fetch(`${BASE_URL}/documents/${documentId}/status`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching document status:', error);
    throw error;
  }
};

/**
 * Send chatbot message (for future integration)
 * @param {string} message - User message
 * @returns {Promise<Object>} Chatbot response
 */
export const sendChatMessage = async (message) => {
  try {
    const response = await fetch(`${BASE_URL}/chat/message`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error sending chat message:', error);
    throw error;
  }
};

