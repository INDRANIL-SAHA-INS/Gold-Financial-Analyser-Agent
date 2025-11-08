from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os
import json
import requests


class GoldMarketToolInput(BaseModel):
    """Input schema for GoldMarketResearchTool."""
    query: str = Field(
        default="latest gold market trends analysis",
        description="The search query to find gold market data and analysis."
    )

class GoldMarketResearchTool(BaseTool):
    name: str = "gold_market_research_tool"  # Tool name should be snake_case
    description: str = (
        "A specialized tool for researching gold market data and trends using Serper API. "
        "It provides real-time gold market data, price analysis, market news, and expert insights. "
        "Use this tool to gather comprehensive information about gold market conditions, "
        "price movements, and market sentiment."
    )
    args_schema: Type[BaseModel] = GoldMarketToolInput

    def _run(self, query: str) -> str:
        try:
            # Serper API configuration
            url = "https://google.serper.dev/search"
            headers = {
                'X-API-KEY': os.environ.get('SERPER_API_KEY'),
                'Content-Type': 'application/json'
            }
            
            # Prepare search parameters
            payload = json.dumps({
                "q": query,
                "num": 10  # Number of results to return
            })

            # Make the API call
            print(f"\nSearching for: {query}")  # Debug print
            response = requests.post(url, headers=headers, data=payload)
            results = response.json()
            print(f"Found {len(results.get('organic', []))} results")

            # Process and format the results
            return self._format_results(results)

        except Exception as e:
            return f"Error collecting gold market data: {str(e)}"

    def _format_results(self, results: dict) -> str:
        """Format the search results into a readable format"""
        formatted_output = []
        
        if 'organic' in results:
            formatted_output.append("## Gold Market Research Results\n")
            
            for result in results['organic']:
                formatted_output.append(f"### {result.get('title', 'No Title')}")
                formatted_output.append(f"{result.get('snippet', 'No description available')}\n")
                formatted_output.append(f"Source: {result.get('link', 'No link available')}\n")

        if not formatted_output:
            return "No relevant gold market data found."

        return "\n".join(formatted_output)
