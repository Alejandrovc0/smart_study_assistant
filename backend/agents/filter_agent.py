from datetime import datetime
from langchain.adapters.openai import convert_openai_messages
from langchain_openai import ChatOpenAI
import ast


class FilterAgent:
    def filter_sources(self, query: str, sources: list):
        """
        Filter for relevant sources for a query.

        :param query: The study query/topic.
        :param sources: A list of sources containing 'url' and other relevant keys.
        :return: List of filtered sources.

        """
        FILTER_PROMPT = [
            {
                "role": "system",
                "content": (
                    "You are an expert study advisor and study material critic. "
                    "Your task is to filter and select the 3 most relevant study materials "
                    "for a given query. Only choose a maximum of 3 sources."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Topic: {query}\n"
                    f"Your purpose is to provide the 3 most relevant sources for the given query.\n"
                    f"Here is a list of sources for the query:\n"
                    f"{sources}\n"
                    f"Return only the URLs of the selected sources in this format: ['url1', 'url2', 'url3']."
                ),
            },
        ]

        try:
            ai__filter_messages = convert_openai_messages(FILTER_PROMPT)
            response = (
                ChatOpenAI(model="gpt-4-0125-preview", max_retries=1)
                .invoke(ai__filter_messages)
                .content
            )
            # Debugging: Print the raw response from the API
            print("Raw response from OpenAI:", response)

            # Ensure the response is in the correct format
            filtered_sources = response
            sources = [
                source for source in sources if source["url"] in filtered_sources
            ]
            return sources
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return []  # Return an empty list in case of error

    def run(self, results: dict):
        results["sources"] = self.filter_sources(results["query"], results["sources"])
        return results
