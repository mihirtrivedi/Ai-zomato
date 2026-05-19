# Architecture: AI-Powered Restaurant Recommendation System

This document outlines the detailed system architecture for the AI-Powered Restaurant Recommendation System based on the Zomato use case.

## 1. Architectural Principles
1. **Separation of Concerns:** Distinct layers for presentation (UI), business logic (Filtering & API), data storage, and AI inference.
2. **Cost & Token Efficiency:** Never send the entire dataset to the LLM. Always apply strict deterministic filtering (location, cost, base cuisine) before passing a small subset to the LLM for contextual reasoning to avoid token limit overflow.
3. **Statelessness:** The backend API should remain stateless to allow for horizontal scaling. User session state (like current search parameters) is maintained by the client (frontend).
4. **Resilience & Fallbacks:** If the LLM API fails or times out, the system should gracefully fallback to returning the top deterministically filtered results without AI explanations.
5. **Data Freshness:** For the scope of this project, the dataset is loaded statically into memory on startup, simulating a read-heavy cache optimized for speed.

## 2. Context Diagram (Level 1)
The Context Diagram illustrates how the system interacts with its environment, including the user and external systems.

```mermaid
flowchart TD
    User(("👤 Hungry User\n(Looking for recommendations)"))
    
    subgraph System
        AIZomato["🤖 AI Restaurant Recommender\n(Provides personalized suggestions)"]
    end
    
    HF["📦 Hugging Face Hub\n(Zomato Dataset Source)"]
    LLM["🧠 LLM Provider API\n(OpenAI / Anthropic)"]

    User -- "Searches for restaurants" --> AIZomato
    AIZomato -- "Downloads dataset on startup" --> HF
    AIZomato -- "Sends prompt & gets reasoning" --> LLM
```

## 3. Logical Containers (Level 2)
The logical container view zooms into the monolithic application system.

```mermaid
flowchart TD
    User(("👤 Hungry User"))
    HF["📦 Hugging Face Hub"]
    LLM["🧠 LLM Provider API"]

    subgraph AI_Zomato_Application ["AI-Zomato Monolithic Application"]
        UI["🖥️ Streamlit Frontend & Orchestrator\n(Python App)"]
        DB[("💾 In-Memory Data Store\n(Pandas DataFrame)")]
    end

    User -- "Interacts with" --> UI
    UI -- "Queries data" --> DB
    UI -- "Fetches initial dataset" --> HF
    UI -- "Requests AI reasoning" --> LLM
```

## 4. Component Level Design (Level 3)
The component view zooms into the Streamlit application to show its internal building blocks.

```mermaid
flowchart TD
    DB[("💾 In-Memory Data Store")]
    LLM["🧠 LLM Provider API"]

    subgraph Streamlit_Application ["Streamlit Application"]
        UI_View["🖥️ UI Layout & State Manager\n(app.py)"]
        Ingestor["📥 Data Ingestor\n(data_ingestor.py)"]
        Filter["🔍 Deterministic Filter Engine\n(filter_engine.py)"]
        PromptBuilder["📝 Prompt Builder\n(prompt_builder.py)"]
        LLMClient["🌐 LLM Integration Client\n(llm_client.py)"]
    end

    UI_View -- "Requests dataset" --> Ingestor
    Ingestor -- "Populates on boot / loads cache" --> DB
    UI_View -- "Requests filtered subset" --> Filter
    Filter -- "Executes queries" --> DB
    UI_View -- "Generates prompt" --> PromptBuilder
    UI_View -- "Passes prompt" --> LLMClient
    LLMClient -- "Sends request" --> LLM
```

## 5. System Workflow (End-to-End Execution)

1. **Initialization:** On startup, the application calls the `Data Ingestor` component, which loads the cached CSV or pulls the Zomato dataset from Hugging Face, cleans it, and loads it into memory.
2. **User Request:** User selects Location="Bangalore", Budget="Medium", Cuisine="Italian", and specifies a custom Nuance (e.g., "Romantic date with live music") via the Streamlit interface.
3. **Hard Filtering:** The application calls the `Deterministic Filter Engine` directly to query the DataFrame and filter out irrelevant options based on strict constraints (Location, Budget, Cuisine, Min Rating).
4. **Prompt Construction:** The `Prompt Builder` takes the top 15 results from the filtered subset, strips unnecessary fields to optimize token usage, and constructs the user and system prompts.
5. **LLM Inference:** The `LLM Integration Client` calls the OpenAI or Groq API with the prompts. The LLM evaluates the options against the nuance, selects the top 3 recommendations, and generates justifications.
6. **Response Delivery:** The application parses the structured JSON response and renders it dynamically in the Streamlit UI.

## 6. Sequence Diagram
This diagram maps out the chronological interactions across the monolithic system when a user makes a recommendation request.

```mermaid
sequenceDiagram
    actor User as 👤 User
    participant UI as 🖥️ Streamlit App (UI & Orchestration)
    participant DB as 💾 In-Memory DB
    participant LLM as 🧠 LLM Provider

    User->>UI: Enters preferences & clicks "Generate"
    activate UI
    
    UI->>DB: Apply strict filters (City, Budget, etc.)
    activate DB
    DB-->>UI: Return N filtered restaurant records
    deactivate DB
    
    UI->>UI: Build prompt with user nuance + N records
    
    UI->>LLM: Send structured prompt & query
    activate LLM
    Note over LLM: AI evaluates matches against nuance<br/>and generates ranking/reasons
    LLM-->>UI: Return JSON (Top 3 Rankings + Explanations)
    deactivate LLM
    
    UI->>UI: Parse and validate JSON response
    UI-->>User: Render results (expanders)
    deactivate UI
```
