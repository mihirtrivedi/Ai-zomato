# Phase-Wise Evaluation Criteria

This document defines the evaluation criteria (success metrics) for each phase of the implementation plan defined in `implementationPlan.md`. 

## Phase 1: Project Setup & Data Foundation
**Evaluation Criteria:**
- [ ] Application starts up successfully.
- [ ] The `Data Ingestor` successfully downloads and caches the Zomato dataset locally to avoid redundant downloads on every boot.
- [ ] The in-memory Pandas DataFrame has 0 missing (`NaN`) values in core columns (Name, Location, Cuisine, Cost, Rating).
- [ ] Text normalization is verified (e.g., cuisines are parsed into lists: `"Italian, Mexican"` -> `["Italian", "Mexican"]`).

## Phase 2: Deterministic Filter Engine
**Evaluation Criteria:**
- [ ] The engine executes in `< 100ms` for any given query.
- [ ] Given a set of strict filters, the engine returns exactly the top `N` (e.g., 10-15) matches sorted by rating.
- [ ] **Edge Case Handled:** If 0 matches are found, the engine returns an empty list gracefully rather than throwing an exception.
- [ ] Case-insensitive matching works flawlessly for Location and Cuisine.

## Phase 3: AI Integration & Prompt Engineering
**Evaluation Criteria:**
- [ ] The LLM strictly returns a parsed, valid JSON object matching the predefined schema (e.g., `[{"name": "...", "reason": "..."}]`).
- [ ] **No Hallucinations:** The LLM *only* recommends restaurants provided to it in the prompt context.
- [ ] The AI explanations clearly and specifically address the user's "nuance" string.
- [ ] **Edge Case Handled:** If the user inputs prompt injection or gibberish, the LLM falls back to a generic friendly recommendation based solely on the hard filters.

## Phase 4: Monolithic Integration & Orchestration
**Evaluation Criteria:**
- [ ] The Streamlit app successfully caches the loaded dataset on startup using `@st.cache_data`.
- [ ] The orchestrator executes the complete pipeline: `User Inputs -> Filters -> Prompt Builder -> LLM Client -> UI`.
- [ ] **Edge Case Handled:** If the filter engine yields 0 results, the system immediately displays a message and bypasses the LLM call to save tokens.
- [ ] The app handles LLM client initialization failures (e.g. missing API key) gracefully by falling back to the deterministic top matches.

## Phase 5: Presentation Layer
**Evaluation Criteria:**
- [ ] The UI runs the entire workflow natively inside the Streamlit server lifecycle without network/CORS issues.
- [ ] Form validations prevent the user from clicking the generate button without entering a City.
- [ ] Recommendations are displayed beautifully using visual structures (e.g., expanders), cleanly separating the restaurant name from the AI explanation.
- [ ] A loading spinner is displayed while the LLM is fetching recommendations.

## Phase 6: Polish, Testing & Deployment
**Evaluation Criteria:**
- [ ] **Fallback Mechanism Works:** If the LLM is forcibly disabled or fails, the system bypasses the LLM step and the UI simply displays the Top 3 deterministically filtered results.
- [ ] Documentation (`README.md`) is complete with clear setup instructions.
- [ ] Unit tests for the Filter Engine and Prompt Builder pass with >80% coverage.
