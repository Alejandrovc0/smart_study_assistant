from tavily import TavilyClient
import os
import requests

tavily_api_key = os.getenv("TAVILY_API_KEY")
if tavily_api_key is None:
    tavily_api_key = "YOUR_DEFAULT_API_KEY"
tavily_client = TavilyClient(api_key=tavily_api_key)


class SourcesAgent:
    def get_materials(self, query: str):
        query = query.strip()
        if len(query) < 5:
            print(f"Query: {query}")
            raise ValueError("Query is too short. It must be at least 5 characters.")

        try:
            # Step 3: Log the query
            print(f"Sending query to Tavily API: '{query}'")
            query = f"Study Materials for {query}"
            materials = tavily_client.search(
                query=query, topic="general", max_results=8, search_depth="advanced"
            )
            sources = materials["results"]
            return sources
        except requests.exceptions.HTTPError as e:
            # Log the detailed error message from the API response
            print(f"Failed to fetch materials: {e.response.text}")
            raise
        except Exception as e:
            # Exceptions such as connection errors, timeouts, etc.
            print(f"An error occurred: {str(e)}")
            raise

    def run(self, source: dict):
        try:
            if "query" not in source:
                raise ValueError("Source dictionary must contain a 'query' key.")

            query = source["query"]
            print(f"Processing source with query: {query}")

            res = self.get_materials(query)
            source["sources"] = res
            return source
        except Exception as e:
            print(f"Error processing source: {e}")
            raise
