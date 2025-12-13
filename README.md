# CredFlow

## An Explainable Credit Intelligence Platform

---

## 1. Problem Statement

Credit scores influence some of the most important financial decisions in a person's life — loan approvals, interest rates, and access to opportunities.  
Yet, for most users, credit scoring remains confusing and opaque.

Today's credit systems commonly:
- Display only a **score or category**, without explaining how it was derived
- Offer **no clear guidance** on how users can improve their credit health
- Operate as **black-box models**, reducing trust and transparency
- Leave users unsure about **loan eligibility, rejection reasons, or better alternatives**
- Fail to support users who are more comfortable in **regional languages**

This lack of clarity often results in repeated rejections, poor financial decisions, and anxiety around credit.

**CredFlow** addresses these gaps by transforming credit scoring into an **explainable, interactive, and user-friendly experience** — helping users understand not just *what* their credit score is, but *why* it is that way and *how* to improve it.

---

## 2. Solution

CredFlow is an end-to-end AI-powered credit intelligence system designed around **clarity, transparency, and user empowerment**.

### Credit Score Calculation & Classification

- User financial and credit behavior data is analyzed to compute a credit score
- Scores are grouped into intuitive categories such as:
  - Excellent (750-900)
  - Good (700-749)
  - Fair (650-699)
  - Poor (600-649)
  - Very Poor (300-599)
- This enables fast understanding of credit risk without overwhelming users

### Explainability with SHAP

- SHAP (SHapley Additive Explanations) is used to explain every prediction
- Each credit outcome is broken down into:
  - Factors that **helped** the score (e.g., timely payments, low utilization)
  - Factors that **hurt** the score (e.g., high debt, payment delays)
- Users can clearly see what influenced their credit profile

### LLM-Based Natural Language Explanations

- SHAP insights are converted into **simple, conversational explanations**
- The system explains:
  - Why a specific credit category was assigned
  - What actions can improve the score
- All explanations avoid financial jargon and are easy to understand

Together, these components turn complex credit models into **transparent and actionable insights**.

---

## 3. Innovation & Uniqueness

CredFlow extends beyond traditional credit scoring by introducing intelligent, user-focused features:

### 1. AI Agent with Knowledge Retrieval

- An interactive AI agent (powered by Groq AI - Llama 3.1-8b-instant) answers user questions about:
  - Credit scores
  - Loan eligibility
  - Improvement strategies
  - Specific user data from the dataset
- The agent can compare market options and inform users when:
  - Similar users receive better interest rates
  - Their income and credit profile qualify them for improved offers
- **Voice Input Support**: Users can speak their questions using microphone input

This makes CredFlow feel like a **personal financial assistant**, not just a scoring tool.

---

### 2. Credit Score Improvement Planner

- For users with low or average scores, CredFlow creates:
  - A personalized improvement plan
  - Clear steps such as reducing utilization or avoiding new inquiries
- Progress can be tracked over time, encouraging healthier financial habits

---

### 3. Credit Score Dashboards

- Visual dashboards help users:
  - Track credit score changes
  - Understand key influencing factors
  - See improvement milestones clearly
- This transforms abstract scores into **visible progress**

---

### 4. Document Scanner & Summarizer

- Users can upload loan rejection letters or financial documents
- The system:
  - Identifies the main reasons for rejection
  - Summarizes them in plain, understandable language
- This removes confusion and helps users take corrective action faster

---

### 5. Multi-Language Support (India-Focused)

- CredFlow supports multiple Indian languages
- Makes credit understanding accessible to:
  - Tier-2 and Tier-3 users
  - Non-English-speaking populations
- Promotes inclusive access to financial knowledge

---

## 4. Tech Stack

### Frontend
- **React 18** - Modern UI framework
- **Vite** - Fast build tool
- **Tailwind CSS** - Utility-first styling
- **Groq AI** - LLM-powered chatbot (Llama 3.1-8b-instant)

### Backend ML
- **Python 3.8+** - Backend language
- **scikit-learn** - Machine Learning (Gradient Boosting Regressor)
- **SHAP** - Explainable AI
- **FastAPI** - REST API framework
- **pandas, numpy** - Data processing

### AI & Explainability
- **SHAP (SHapley Additive Explanations)** - Feature importance and explanations
- **Large Language Models** - Groq AI for natural language explanations
- **AI Agents & Knowledge Retrieval** - RAG-based architecture for chatbot

### Data Visualization
- **Interactive dashboards** - React components with Tailwind CSS

---

## 5. Implementation Details

### ML Pipeline Features

✅ **Data Loading & Feature Inference** - Automatically infers feature types from CSV  
✅ **Data Preprocessing** - Handles missing values, encoding, scaling  
✅ **Synthetic Credit Score Generation** - Creates target variable from financial features  
✅ **ML Model Training** - Gradient Boosting Regressor for score prediction  
✅ **Score Normalization** - Normalizes to 300-900 range  
✅ **User Categorization** - Categorizes users (Excellent, Good, Fair, Poor, Very Poor)  
✅ **SHAP Explainability** - Provides feature importance and explanations  
✅ **Human-Readable Explanations** - Converts SHAP values to natural language  
✅ **REST API** - FastAPI server for frontend integration  

### Frontend Features

- **Responsive Navbar**: Sticky navigation with logo, title banner, and menu items
- **Credit Score Card**: Display and analyze credit scores (connected to backend ML model)
- **Document Scanner Card**: Upload and process financial documents (connected to backend ML model)
- **AI Chatbot Widget**: Floating chatbot powered by Groq AI with:
  - Voice input support (microphone)
  - Dataset querying by user ID
  - Credit score explanations
  - Financial concept explanations

---

## 6. Getting Started

### Frontend Setup

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

### Backend ML Setup

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

The API will be available at `http://localhost:8000` with documentation at `http://localhost:8000/docs`.

### Environment Configuration

Create a `.env` file in the project root:

```env
VITE_API_BASE_URL=http://localhost:8000/api
```

---

## 7. Project Structure

```
credit-score-website/
├── src/                    # React frontend
│   ├── components/         # UI components
│   ├── hooks/              # Custom React hooks
│   ├── services/           # API services
│   └── pages/              # Page components
├── ml_backend/             # Python ML pipeline
│   ├── data_loader.py      # Data loading & feature inference
│   ├── preprocessor.py     # Data preprocessing
│   ├── model_trainer.py    # Model training
│   ├── shap_explainer.py   # SHAP explainability
│   ├── explanation_generator.py  # Human-readable explanations
│   ├── api_server.py       # FastAPI REST API
│   └── train_pipeline.py   # Complete training script
├── public/                  # Static assets
│   └── credit_score.csv    # Dataset
└── package.json            # Frontend dependencies
```

---

## 8. Feasibility & Viability

| Feature                        | Feasibility | Viability                                      |
| ------------------------------ | ----------- | ---------------------------------------------- |
| **AI Agent & RAG**             | High        | Very High – Acts as a 24/7 financial assistant |
| **Credit Score Planner**       | Medium      | High – Encourages long-term user engagement    |
| **Loan Probability Interface**  | Low         | Medium – Reduces rejection anxiety             |
| **Document Scanner**           | High        | Extremely High – Removes onboarding friction   |
| **Multi-Language Support**     | Medium      | Very High – Expands reach across India         |
| **SHAP Explainability**        | High        | Very High – Builds trust and transparency      |

---

## 9. Impacts & Benefits

### AI Agent
- **Impact:** Improves transparency around credit and loan options
- **Benefit:** Users make informed decisions and secure better terms

### Credit Score Planner
- **Impact:** Encourages responsible financial behavior
- **Benefit:** Clear roadmap toward improved credit eligibility

### Loan Probability Interface
- **Impact:** Reduces unnecessary credit checks
- **Benefit:** Lowers stress and uncertainty during applications

### Document Scanner
- **Impact:** Simplifies complex financial communication
- **Benefit:** Faster understanding of rejection reasons

### Multi-Language Support
- **Impact:** Promotes financial inclusion
- **Benefit:** Makes credit intelligence accessible across regions

### SHAP Explainability
- **Impact:** Builds trust through transparency
- **Benefit:** Users understand exactly what affects their credit score

---

## Conclusion

**CredFlow** redefines how users experience credit scoring.  
By combining **explainable machine learning, natural language explanations, and intelligent AI agents**, CredFlow empowers individuals to **understand their credit, improve it confidently, and make smarter financial decisions**.

It is not just a credit score — it is a **clear path to better credit health**.

---

## Documentation

- `ML_PIPELINE_GUIDE.md` - Complete ML pipeline documentation
- `NEXT_STEPS.md` - Step-by-step setup guide
- `QUICK_START.md` - Quick start instructions
- `ml_backend/README.md` - Backend ML documentation
