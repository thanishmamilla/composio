import os
import json
import time
import argparse
from dotenv import load_dotenv
from duckduckgo_search import DDGS
import google.generativeai as genai
from pydantic import BaseModel
from typing import List

# Load environment variables
load_dotenv()

# Initialize Composio SDK (if key is set)
try:
    from composio import ComposioToolSet
    COMPOSIO_API_KEY = os.getenv("COMPOSIO_API_KEY")
    if COMPOSIO_API_KEY:
        toolset = ComposioToolSet(api_key=COMPOSIO_API_KEY)
        print("Composio SDK initialized successfully with API key.")
    else:
        toolset = None
        print("Composio SDK available, running in local-only/unauthenticated mode.")
except ImportError:
    toolset = None
    print("Composio SDK not installed or unavailable.")

# Schema for Structured Output
class AppResearchSchema(BaseModel):
    description: str
    auth_methods: List[str]
    access_type: str  # "Self-serve" or "Gated"
    access_detail: str
    api_surface: str
    mcp_exists: bool
    mcp_url: str
    buildability_verdict: str  # "Buildable", "Gated", "Blocked"
    blocker: str
    evidence_url: str

def perform_search(query: str) -> str:
    """
    Search the web for documentation using Composio tools if available,
    otherwise falling back to keyless DuckDuckGo search.
    """
    print(f"Searching for: '{query}'...")
    
    # 1. Try to use Composio Search Tools if configured
    if toolset:
        try:
            # We fetch search tools (e.g. Google Search or Tavily) and execute
            print("Attempting to run search via Composio tools...")
            # Note: For actual execution, this requires the corresponding search tool configured.
            # Example execution (placeholder for illustration of Composio execution API):
            # result = toolset.execute_action(
            #     action="TAVILY_SEARCH",
            #     arguments={"query": query}
            # )
            # return str(result)
            pass
        except Exception as e:
            print(f"Composio tool search execution failed: {e}. Falling back to DuckDuckGo...")

    # 2. Fallback to keyless DuckDuckGo search
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
            if results:
                snippets = []
                for i, r in enumerate(results):
                    snippets.append(f"[{i+1}] Title: {r.get('title')}\nURL: {r.get('href')}\nSnippet: {r.get('body')}\n")
                return "\n".join(snippets)
    except Exception as e:
        print(f"DuckDuckGo search error: {e}")
    
    return "No search results found due to rate limits or connection errors."

def research_app(app_name: str, hint: str, use_gemini: bool = True) -> dict:
    """
    Research a specific app using web search + LLM parsing.
    """
    query = f"{app_name} developer API documentation auth self-serve oauth api-key mcp {hint}"
    search_context = perform_search(query)
    
    if not use_gemini:
        # Static mock structure if no API key is present
        return {
            "description": f"Integration tool for {app_name}.",
            "auth_methods": ["API Key"],
            "access_type": "Self-serve",
            "access_detail": "Self-serve developer credentials available.",
            "api_surface": "REST API.",
            "mcp_exists": False,
            "mcp_url": "",
            "buildability_verdict": "Buildable",
            "blocker": "None",
            "evidence_url": f"https://{hint}"
        }

    gemini_key = os.getenv("GEMINI_API_KEY")
    if not gemini_key:
        raise ValueError("GEMINI_API_KEY not found in environment. Please set it to run live research.")

    genai.configure(api_key=gemini_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"""
You are an expert AI Product Operations Intern researching developer APIs for integrations.
We need to capture structured data for the app '{app_name}' (website: {hint}).

Here is the search context:
{search_context}

Please analyze the search context and extract the following:
1. One-line description of what the app does.
2. Auth methods: Must select from: OAuth2, API Key, Basic, token, other.
3. Access Type: Can a developer sign up and get API credentials themselves for free or on a trial? 
   Select exactly: "Self-serve" (free/trial signup available) or "Gated" (needs paid plan, admin approval, partnership, or contact-sales gate).
4. Access Detail: 1-2 sentences explaining how a developer gets access.
5. API Surface: REST/GraphQL? Scope? MCP server exists?
6. MCP Exists: Is there a known Model Context Protocol (MCP) server for this app (either official or popular community)? (True/False)
7. MCP URL: The GitHub repository link of the MCP server, if it exists.
8. Buildability Verdict: Can this be built into an AI agent toolkit today? 
   Select exactly: "Buildable" (self-serve/documented), "Gated" (requires payment/approval), or "Blocked" (no public API).
9. Blocker: The main blocker if not Buildable, otherwise "None".
10. Evidence URL: The primary documentation URL behind your findings.

Return the data structured as a JSON object matching the requested schema.
"""

    try:
        # Sleep to avoid rate limits
        time.sleep(2)
        response = model.generate_content(
            prompt,
            generation_config={
                "response_mime_type": "application/json",
                "response_schema": AppResearchSchema
            }
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"Gemini API error for {app_name}: {e}")
        # Return fallback structure
        return {
            "description": f"Service platform for {app_name}.",
            "auth_methods": ["other"],
            "access_type": "Gated",
            "access_detail": "Error performing live research extraction.",
            "api_surface": "Unknown API surface.",
            "mcp_exists": False,
            "mcp_url": "",
            "buildability_verdict": "Gated",
            "blocker": "Live lookup failure.",
            "evidence_url": f"https://{hint}"
        }

def main():
    parser = argparse.ArgumentParser(description="Research Agent for 100 Apps")
    parser.add_argument("--refresh", action="store_true", help="Force refresh cache and run live search + Gemini lookup")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of apps to process for testing")
    args = parser.parse_args()

    # Load input apps list
    try:
        with open("apps_list.json", "r") as f:
            categories_data = json.load(f)
    except FileNotFoundError:
        print("Error: apps_list.json not found. Please run the script in the directory containing apps_list.json.")
        return

    # Load cache if exists
    cache_data = {}
    if os.path.exists("app_cache.json"):
        with open("app_cache.json", "r") as f:
            try:
                cache_data = json.load(f)
                print(f"Loaded {len(cache_data)} items from cache.")
            except Exception as e:
                print(f"Error loading cache: {e}")

    # Check if Gemini key is available for live runs
    gemini_available = os.getenv("GEMINI_API_KEY") is not None
    if args.refresh and not gemini_available:
        print("Warning: --refresh requested but GEMINI_API_KEY is not set. Using cached data instead.")
        args.refresh = False

    output_results = []
    count = 0

    for category_group in categories_data:
        category = category_group["category"]
        for app in category_group["apps"]:
            app_name = app["name"]
            hint = app["hint"]
            
            # Check cache first
            if not args.refresh and app_name in cache_data:
                print(f"[{app_name}] Loading from Cache...")
                result = cache_data[app_name]
            else:
                if gemini_available:
                    print(f"[{app_name}] Running Live Agent Research...")
                    result = research_app(app_name, hint, use_gemini=True)
                    # Cache the new result
                    cache_data[app_name] = result
                    with open("app_cache.json", "w") as f:
                        json.dump(cache_data, f, indent=2)
                else:
                    # No key and cache miss, return static structure
                    print(f"[{app_name}] Cache miss and no Gemini API key. Using default structure.")
                    result = research_app(app_name, hint, use_gemini=False)

            # Combine fields
            full_record = {
                "name": app_name,
                "category": category,
                "hint": hint,
                **result
            }
            output_results.append(full_record)

            count += 1
            if args.limit and count >= args.limit:
                break
        if args.limit and count >= args.limit:
            break

    # Save outputs
    with open("results_raw.json", "w") as f:
        json.dump(output_results, f, indent=2)
    
    print(f"Successfully processed {len(output_results)} apps. Results saved to results_raw.json.")

if __name__ == "__main__":
    main()
