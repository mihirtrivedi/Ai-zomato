# Phase-Wise Implementation Plan: AI-Zomato

This document outlines the step-by-step implementation plan for the AI-Powered Restaurant Recommendation System, structured across 6 phases based on our defined Architecture and Problem Statement.

---

## Phase 1: Project Setup & Data Foundation (Data Layer)
**Goal:** Set up the environment and ensure the dataset is cleaned and accessible in memory.

1. **Environment Setup:**
   - Initialize Git repository.
   - Create a Python virtual environment and `requirements.txt` (pandas, openai, streamlit, python-dotenv, datasets).
2. **Data Ingestion Script (`data_ingestor.py`):**
   - Write a script to fetch the `ManikaSaini/zomato-restaurant-recommendation` dataset from Hugging Face.
   - Preprocess the data: handle missing values, normalize text (lowercase, strip whitespace), format cost, and parse ratings.
3. **Cache Storage:**
   - Cache the dataset locally as a CSV file to skip the download process on subsequent starts.

---

## Phase 2: Deterministic Filter Engine (Application Layer)
**Goal:** Build the strict filtering mechanism to reduce the dataset size before it hits the LLM.

1. **Filter Logic (`filter_engine.py`):**
   - Implement functions to filter the DataFrame based on structured user inputs: `City`, `Budget` (Low/Medium/High boundaries), and `Cuisine`.
   - Implement logic to select the top `N` results (e.g., top 15 by rating/cost tie-breaker) from the filtered subset to ensure we do not overflow the LLM token context window.
2. **Unit Testing:**
   - Test the filter engine using `unittest` to ensure it accurately returns a subset of restaurants when given specific parameters.

---

## Phase 3: AI Integration & Prompt Engineering (AI Layer)
**Goal:** Connect to the LLM and craft the prompts that generate human-like reasoning.

1. **LLM Client Setup (`llm_client.py`):**
   - Setup authentication (API Keys) for the chosen LLM provider (OpenAI or Groq compatible endpoints).
   - Write a robust client function that sends requests to the LLM, handles rate limits/retries, and enforces structured JSON responses.
2. **Prompt Builder (`prompt_builder.py`):**
   - Design the **System Prompt** defining the persona ("Expert Food Critic").
   - Design the **User Prompt** template that dynamically injects the user's specific unstructured nuance (e.g., "Good for a quiet anniversary") and the JSON representation of the `N` filtered restaurants from Phase 2.

---

## Phase 4: Monolithic Integration & Orchestration
**Goal:** Tie the Data, Filtering, and AI layers together natively.

1. **Streamlit Cache Setup:**
   - Set up `@st.cache_data` in the application script to trigger the `Data Ingestor` and cache the loaded DataFrame in memory on boot.
2. **Recommendation Orchestrator:**
   - Integrate the workflow directly inside the application execution script: 
     `Input -> Filter Engine -> Prompt Builder -> LLM Client -> UI Output`.
   - Add error handling (e.g., what happens if the Filter Engine returns 0 results).

---

## Phase 5: Presentation Layer (Frontend UI Design)
**Goal:** Build the user interface layout for users to interact with the system.

1. **Streamlit UI Layout (`app.py`):**
   - Create a clean, interactive Streamlit application.
2. **Input Form:**
   - Add a sidebar for strict filters: Location, Budget, Cuisine, Min Rating.
   - Add a text input field for the user's *nuance* or *specific occasion*.
3. **Execution & Rendering:**
   - On submit, trigger the orchestrator workflow natively.
   - Parse and display the top 3 recommendations dynamically with modern UI elements (e.g., Streamlit expanders), clearly displaying the AI's explanation for each choice.

---

## Phase 6: Polish, Testing & Deployment
**Goal:** Finalize the application for production or demonstration.

1. **Resilience Testing:**
   - Test edge cases: invalid locations, highly obscure cuisines, LLM timeouts, and empty nuances.
   - Implement graceful fallbacks (e.g., if LLM fails, return the top 3 filtered restaurants without AI explanations).
2. **Documentation:**
   - Write the `README.md` containing local setup instructions and architecture diagrams.
3. **Deployment:**
   - Dockerize the application.
   - Deploy directly to Streamlit Community Cloud.

