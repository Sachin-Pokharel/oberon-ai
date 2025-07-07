import requests
from pydantic import BaseModel
from typing import List, Optional
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

class SearchResult(BaseModel):
    title: str
    link: str
    snippet: str
    description: Optional[str] = None  # from og:description


def google_search(query: str, num_results: int = 5) -> List[SearchResult]:
    
    api_key = os.getenv("CUSTOM_SEARCH_API")
    cse_id = os.getenv("CUSTOM_SEARCH_ENGINE_ID")
        
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": api_key,
        "cx": cse_id,
        "num": num_results,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    results = response.json()

    search_results = []

    for item in results.get("items", []):
        title = item.get("title")
        link = item.get("link")
        snippet = item.get("snippet")
        description = None

        page_map = item.get("pagemap", {})
        metatags = page_map.get("metatags", [])
        if metatags and isinstance(metatags[0], dict):
            description = metatags[0].get("og:description")

        result = SearchResult(
            title=title,
            link=link,
            snippet=snippet,
            description=description
        )
        search_results.append(result)
        
    
    return [result.model_dump() for result in search_results]