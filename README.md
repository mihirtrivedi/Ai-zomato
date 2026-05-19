# 🍔 AI-Powered Restaurant Recommender (Zomato Use Case)

An intelligent, context-aware restaurant recommendation system that combines strict deterministic filtering with the reasoning capabilities of Large Language Models (LLMs). This project is inspired by Zomato and is designed to eliminate "choice overload" by providing hyper-personalized dining suggestions based on unstructured nuances (e.g., "A quiet, dimly lit place for a romantic anniversary").

## 🏗️ Architecture

This project is built using a streamlined, monolithic architecture optimized for simple deployment on platforms like Streamlit Community Cloud:

1. **Data Layer:** Fetches and caches the Zomato dataset from Hugging Face into an in-memory Pandas DataFrame.
2. **Deterministic Filter Engine:** Filters down the restaurant dataset based on City, Budget, and Cuisine to a manageable subset (Top 15).
3. **AI Layer (LLM):** Injects the filtered subset and the user's specific conversational "nuance" into an optimized prompt, utilizing an LLM to rank the options and generate persuasive explanations.
4. **Presentation Layer:** A dynamic Streamlit user interface (`app.py`) that runs the ingestion, filtering, and LLM orchestration logic directly.

*(For detailed architectural diagrams and edge-case handling, see `documents/architecture.md` and `documents/edgeCases.md`).*

## 🚀 Quick Start (Local Setup)

### 1. Prerequisites
- Python 3.9+
- Git

### 2. Installation
Clone the repository and install the dependencies:
```bash
git clone <your-repo-url>
cd Ai-zomatao
python -m venv venv

# Activate the virtual environment
# On Windows:
.\venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file in the root directory and add your OpenAI or Groq API Key:
```env
OPENAI_API_KEY=sk-your-openai-api-key-here
```
*Note: If you do not provide an API key, the system has a built-in resilience mechanism that gracefully bypasses the AI layer and falls back to returning the best deterministically filtered restaurants.*

### 4. Running the Application
To run the Streamlit app:
```bash
# Ensure venv is activated
streamlit run app.py
```
Navigate to `http://localhost:8501` in your browser to interact with the UI!

