# Assignment 1 — Artificial Intelligence
**Student:** Azqa Naseeb  
**Course:** Artificial Intelligence — 5th Semester  
**Instructor:** Touqeer Abbas  

## Task 1 — Netflix ML Model
- Dataset: Netflix Titles (Kaggle) — 8807 rows, 6 columns
- Models: Random Forest (99.94% accuracy) + K-Means Clustering
- File: `netflix_ml_model_azqa.ipynb`

## Task 2 — AI Agent Web App

- **Agent Type:** AI Coding Assistant
- **LLM API:** Groq (LLaMA 3.1 8B Instant)
- **Backend:** Flask (Python) — Port 5000
- **Frontend:** Streamlit — Port 8501
- **Files:** `backend/app.py`, `frontend/streamlit_app.py`

### Features
- Chat-style interface with conversation history
- Enter key + button to send messages
- Token usage tracker in sidebar
- Clear chat functionality
- System prompt: Expert coding assistant

### Setup
1. Clone the repository
2. Create `.env` file and add `GROQ_API_KEY=your_key`
3. Install dependencies: `pip install -r requirements.txt`
4. Run backend: `cd backend && python app.py`
5. Run frontend: `cd frontend && streamlit run streamlit_app.py`
6. Open `http://localhost:8501`
