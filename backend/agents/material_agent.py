from tavily import TavilyClient
import os

tavily_client = TavilyClient(api_key=os.getenv('TAVILY_API_KEY'))

class MaterialAgent:
    def get_materials(self, query: str):
        materials = tavily_client.search(query=query, type="study material", max_results=3)
        sources = materials["materials"]
        return sources
    
    def run(self, source: dict):
        res = self.get_materials(source["query"])
        source["materials"] = res[0]
        return source
