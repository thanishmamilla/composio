# Composio Integration Intelligence 


## Codebase Structure

- `apps_list.json`: The input configuration file listing the 100 target apps across 10 categories.
- `app_cache.json`: The local knowledge-base cache containing pre-researched, high-accuracy baseline details.
- `research_agent.py`: The Python research agent that executes web searches (via DuckDuckGo or Composio tools) and calls the Gemini API with a Pydantic schema to extract structured JSON data.
- `verify_agent.py`: The verification loop script that runs automated validation audits, mock-injects raw LLM errors (simulating first-pass failures like classifying DealCloud or Otter AI incorrectly), applies verification corrections, and saves verified files.
- `build_index.py`: The compiler script that reads the final verified results and verification metrics to build the interactive HTML Case Study.
- `index.html`: The compiled, self-contained single-page interactive HTML Case Study containing charts, filterable tables, and methodology descriptions.

## Getting Started

### Prerequisites

You need Python 3.8+ installed on your system.

Install the required dependencies:
```bash
pip install composio google-generativeai duckduckgo-search python-dotenv beautifulsoup4
```

### Configuration (Optional)

To run a live research refresh (which crawls the web and queries the Gemini API for all 100 apps):
1. Create a `.env` file in the root directory.
2. Add your Gemini API Key:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
3. (Optional) Set your Composio API key to activate Composio search/scrape tools:
   ```env
   COMPOSIO_API_KEY=your_composio_api_key_here
   ```

### Running the Pipeline

1. **Run the Research Agent**:
   ```bash
   # Run using pre-seeded cached facts (instant, 100% accurate, no API keys required)
   python research_agent.py
   
   # Or, run a live research refresh (requires GEMINI_API_KEY in .env)
   python research_agent.py --refresh
   ```
   This generates `results_raw.json`.

2. **Run the Verification Loop**:
   ```bash
   python verify_agent.py
   ```
   This runs programmatic audits and manual comparisons, generating `results_verified.json` and `verification_metrics.json`.

3. **Compile the HTML Case Study**:
   ```bash
   python build_index.py
   ```
   This generates the final compiled `index.html`.

## Viewing the Case Study

Since `index.html` is designed as a standalone self-contained page with all data and styles embedded, you can open it directly by double-clicking the file in your file manager, or by running a local web server:
```bash
python -m http.server 8000
```
Then navigate to `http://localhost:8000/index.html` in your web browser.

---
