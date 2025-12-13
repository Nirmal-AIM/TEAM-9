# Backend ML Model Integration Guide

This document explains how to connect the frontend to your backend ML model.

## Overview

The frontend is **fully prepared** for backend integration. All components use hooks and services that can easily connect to your ML model APIs.

## Integration Architecture

```
Frontend Components
    ↓
Custom Hooks (useCreditScore, useDocumentUpload)
    ↓
API Service (api.js)
    ↓
Backend ML Model
```

## Step-by-Step Integration

### 1. Configure API Base URL

Create a `.env` file in the root directory:

```env
VITE_API_BASE_URL=http://localhost:8000/api
```

For production:
```env
VITE_API_BASE_URL=https://your-backend-domain.com/api
```

### 2. Credit Score Analysis Integration

**File**: `src/hooks/useCreditScore.js`

Uncomment these lines (around line 20-24):
```javascript
// Change from:
// setScore(750);

// To:
const data = await getCreditScore();
setScore(data.score);
```

Uncomment these lines (around line 35-40):
```javascript
// Change from placeholder to:
const result = await analyzeCreditScore(userData);
setScore(result.score);
setAnalysis(result.analysis);
```

**Expected Backend Response**:
```json
{
  "score": 750,
  "analysis": {
    "factors": ["Payment History", "Credit Utilization"],
    "recommendations": ["Pay bills on time", "Reduce balances"]
  }
}
```

### 3. Document Upload Integration

**File**: `src/hooks/useDocumentUpload.js`

Uncomment these lines (around line 20-30):
```javascript
// Change from placeholder to:
const result = await uploadDocument(file, documentType);
setUploadedDocuments(prev => [...prev, result]);
setProcessingStatus('processing');
```

**Expected Backend Response**:
```json
{
  "id": "doc_123",
  "filename": "statement.pdf",
  "type": "bank_statement",
  "status": "processed",
  "extractedData": {
    "fields": {
      "account_number": "1234567890",
      "balance": "50000",
      // ... other extracted fields
    }
  }
}
```

### 4. Chatbot AI Integration

**File**: `src/components/Chatbot.jsx`

Uncomment these lines (around line 34-36):
```javascript
// Change from placeholder to:
const response = await sendChatMessage(userMessage);
setMessages(prev => [...prev, { text: response.message, sender: 'bot' }]);
```

**Expected Backend Response**:
```json
{
  "message": "AI-generated response here"
}
```

## Backend API Endpoints Required

Your backend ML model should implement these endpoints:

### 1. Credit Score Analysis
```
POST /api/credit-score/analyze
Content-Type: application/json

Request Body:
{
  "creditHistory": [...],
  "paymentHistory": [...],
  "creditUtilization": 0.3,
  // ... other ML model inputs
}

Response:
{
  "score": 750,
  "analysis": {
    "factors": [...],
    "recommendations": [...]
  }
}
```

### 2. Get Current Credit Score
```
GET /api/credit-score/current
Authorization: Bearer <token> (if needed)

Response:
{
  "score": 750,
  "lastUpdated": "2024-01-01T00:00:00Z"
}
```

### 3. Upload Document
```
POST /api/documents/upload
Content-Type: multipart/form-data

Form Data:
- file: <binary file>
- document_type: "pan" | "aadhaar" | "bank_statement" | "income_proof"

Response:
{
  "id": "doc_123",
  "filename": "statement.pdf",
  "type": "bank_statement",
  "status": "processing",
  "extractedData": {...}
}
```

### 4. Document Status
```
GET /api/documents/:id/status

Response:
{
  "status": "processing" | "completed" | "error",
  "progress": 75,
  "extractedData": {...}
}
```

### 5. Chatbot Message
```
POST /api/chat/message
Content-Type: application/json

Request Body:
{
  "message": "What is my credit score?"
}

Response:
{
  "message": "Your current credit score is 750..."
}
```

## Data Flow Examples

### Credit Score Analysis Flow

1. User clicks "Analyze Score" button
2. `CreditScoreCard` calls `handleAnalyze()`
3. `Home` component calls `analyze()` from `useCreditScore` hook
4. Hook calls `analyzeCreditScore()` from API service
5. API service sends POST request to `/api/credit-score/analyze`
6. Backend ML model processes data and returns score + analysis
7. Response flows back through hooks to component
8. Component displays results

### Document Upload Flow

1. User selects file and document type
2. `DocumentScannerCard` calls `handleDocumentUpload()`
3. `Home` component calls `upload()` from `useDocumentUpload` hook
4. Hook calls `uploadDocument()` from API service
5. API service sends POST request with FormData to `/api/documents/upload`
6. Backend ML model processes document (OCR, extraction, etc.)
7. Response flows back through hooks to component
8. Component shows upload status and extracted data

## Error Handling

All components include error handling:
- Network errors are caught and displayed
- Loading states prevent duplicate requests
- User-friendly error messages
- Fallback to placeholder data if backend unavailable

## Testing Without Backend

The frontend works with placeholder data until backend is connected:
- Credit score shows default value (750)
- Document upload simulates processing
- Chatbot shows placeholder responses

## Security Considerations

When integrating:
1. Add authentication tokens to API requests
2. Validate file types and sizes on backend
3. Implement rate limiting
4. Use HTTPS in production
5. Sanitize user inputs

## Next Steps

1. ✅ Frontend is ready - all integration points prepared
2. ⏳ Implement backend ML model endpoints
3. ⏳ Update `.env` with backend URL
4. ⏳ Uncomment API calls in hooks/components
5. ⏳ Test integration end-to-end
6. ⏳ Adjust data structures if needed

## Support

All integration points are marked with `TODO` comments in the code. Search for "TODO" to find all places where backend integration should be enabled.

