# Credit Score Website

A complete full-stack application with **React frontend** and **Python ML backend** for credit score analysis with SHAP explainability.

## Tech Stack

### Frontend
- React 18
- Vite
- Tailwind CSS
- Functional Components
- Custom Hooks for API integration

### Backend ML
- Python 3.8+
- scikit-learn (Gradient Boosting)
- SHAP (Explainability)
- FastAPI (REST API)
- pandas, numpy (Data processing)

## Features

- **Responsive Navbar**: Sticky navigation with logo, title banner, and menu items
- **Credit Score Card**: Display and analyze credit scores (connected to backend ML model)
- **Document Scanner Card**: Upload and process financial documents (connected to backend ML model)
- **AI Chatbot Widget**: Floating chatbot powered by Groq AI that can:
  - Answer questions about credit scores and financial concepts
  - Provide insights from the credit score dataset
  - Explain website features and capabilities
  - Help users understand credit score factors
- **Backend Integration Ready**: All components are structured to connect with ML models

## ML Backend Pipeline

A complete ML pipeline is available in `ml_backend/` directory:

### Features
- ✅ Reads `credit_score.csv` and infers feature types
- ✅ Creates synthetic credit score (300-900 range)
- ✅ Preprocesses data (missing values, encoding, scaling)
- ✅ Trains Gradient Boosting model
- ✅ Normalizes scores to 300-900
- ✅ Categorizes users (Excellent, Good, Fair, Poor, Very Poor)
- ✅ SHAP explainability for feature importance
- ✅ Human-readable explanations from SHAP values
- ✅ FastAPI REST API for frontend integration

### Quick Start (ML Backend)

```bash
cd ml_backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Train model
python train_pipeline.py

# Start API server
python api_server.py
```

See `ML_PIPELINE_GUIDE.md` for detailed documentation.

## Backend ML Model Integration

The frontend is **fully prepared** to connect with the ML backend. All API endpoints and data flow are structured and ready.

### API Service (`src/services/api.js`)

The API service includes functions for:
- `analyzeCreditScore()` - Send data to ML model for credit score analysis
- `uploadDocument()` - Upload documents for ML processing (OCR, data extraction)
- `getCreditScore()` - Fetch current credit score from backend
- `getDocumentStatus()` - Check document processing status
- `sendChatMessage()` - Send messages to AI chatbot backend

### Custom Hooks

- `useCreditScore()` - Manages credit score data and analysis
- `useDocumentUpload()` - Handles document upload and processing

### Environment Configuration

Create a `.env` file (use `.env.example` as template):

```env
VITE_API_BASE_URL=http://localhost:8000/api
```

### Integration Points

1. **Credit Score Analysis**: 
   - Component: `CreditScoreCard`
   - Hook: `useCreditScore`
   - API: `analyzeCreditScore()`
   - Update `src/hooks/useCreditScore.js` to uncomment API calls

2. **Document Processing**:
   - Component: `DocumentScannerCard`
   - Hook: `useDocumentUpload`
   - API: `uploadDocument()`
   - Update `src/hooks/useDocumentUpload.js` to uncomment API calls

3. **Chatbot AI**:
   - Component: `Chatbot`
   - API: `sendChatMessage()`
   - Update `src/components/Chatbot.jsx` to uncomment API calls

## Getting Started

### Installation

```bash
npm install
```

### Development

```bash
npm run dev
```

### Build

```bash
npm run build
```

### Preview

```bash
npm run preview
```

## Project Structure

```
src/
  ├── components/
  │   ├── Navbar.jsx
  │   ├── Chatbot.jsx          # Ready for AI backend
  │   ├── CreditScoreCard.jsx   # Connected to ML model
  │   └── DocumentScannerCard.jsx # Connected to ML model
  ├── pages/
  │   └── Home.jsx              # Main page with hooks
  ├── hooks/
  │   ├── useCreditScore.js     # Credit score state management
  │   └── useDocumentUpload.js  # Document upload state management
  ├── services/
  │   └── api.js                # All backend API endpoints
  ├── App.jsx
  ├── main.jsx
  └── index.css
```

## Backend Integration Checklist

When your ML model backend is ready:

1. ✅ Update `VITE_API_BASE_URL` in `.env` file
2. ✅ Uncomment API calls in `src/hooks/useCreditScore.js`
3. ✅ Uncomment API calls in `src/hooks/useDocumentUpload.js`
4. ✅ Uncomment API calls in `src/components/Chatbot.jsx`
5. ✅ Adjust API request/response formats in `src/services/api.js` to match your backend
6. ✅ Update data structures in components to match ML model output

## Expected Backend Endpoints

Your backend should implement these endpoints:

- `POST /api/credit-score/analyze` - Analyze credit score
- `GET /api/credit-score/current` - Get current score
- `POST /api/documents/upload` - Upload document for processing
- `GET /api/documents/:id/status` - Get document processing status
- `POST /api/chat/message` - Send chatbot message

## Groq AI Chatbot Integration

The chatbot is **fully integrated** with Groq AI API and can:
- Answer questions about credit scores, financial concepts, and best practices
- Provide insights based on the credit score dataset (loaded from `public/credit_score.csv`)
- Explain website features and capabilities
- Help users understand factors that affect credit scores

The chatbot automatically loads dataset statistics and context on initialization, enabling it to provide informed answers about the credit score data.

**Note**: The Groq API key is configured in `src/services/groqService.js`. For production, consider moving the API key to environment variables.

## Notes

- All components include loading states and error handling
- Chatbot is fully functional with Groq AI integration
- Credit Score and Document Scanner components use placeholder data until backend is connected
- All TODO comments mark where backend integration should be enabled

