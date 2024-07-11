from datetime import datetime
from langchain.adapters.openai import convert_openai_messages
from langchain_openai import ChatOpenAI


class RevisorAgent:
    def filter_sources(self, query: str, sources: list):
        """
        Filter for relevant sources for a query.

        :param query: The study query/topic.
        :param sources: A list of source dictionaries containing 'url' and other relevant keys.
        :return: List of filtered sources.
        """
        FILTER_PROMPT = [
            {
                "role": "system",
                "content": "You are an expert study advisor and study material critique. You are tasked with filtering and selecting the 3 most relevant study materials "
                "for a query. Only choose 3 sources max.\n",
            },
            {
                "role": "user",
                "content": f"Today's date is {datetime.now().strftime('%d/%m/%Y')}\n."
                f"Topic or query: {query}\n"
                f"Your purpouse is to provide the 3 most relevant sources for me to plan a detailed study plan and schedule for"
                "the provided topic or query\n"
                f"Here are the 3 most relevant sources for the query:\n"
                f"{[source['url'] for source in sources]}\n"
                f"Please only return a list of the URLs in this format: ['url1','url2','url3']\n",
            },
        ]

        ai__filter_messages = convert_openai_messages(FILTER_PROMPT)
        response = (
            ChatOpenAI(model="gpt-4", temperature=0, max_retries=1)
            .invoke(ai__filter_messages)
            .content
        )
        filtered_sources_urls = eval(response)
        filtered_sources = [
            source for source in sources if source["url"] in filtered_sources_urls
        ]

        return filtered_sources

    def revise_sources(self, materials: dict):
        """
        Revise relevant sources and provide feedback for a query.

        :param materials: A dictionary containing query and filtered sources.
        :return: Dictionary with revision feedback.

        """
        REVISE_PROMPT = [
            {
                "role": "system",
                "content": "You are an expert study advisor and study material critique. You are tasked with reviewing the 3 filtered study materials "
                "for a JSON query, and provide a short feedback on the quality of the materials along with the sources so the scheduler will know what to propose.",
            },
            {
                "role": "user",
                "content": f"Today's date is {datetime.now().strftime('%d/%m/%Y')}\n."
                f"{str(materials)}\n"
                f"Your purpouse is to provide feedback on the quality of the materials and suggest improvements for "
                "the provided topic or query\n"
                f"Return None if you think there is no need for revision.\n",
            },
        ]

        ai_messages = convert_openai_messages(REVISE_PROMPT)
        response = (
            ChatOpenAI(model="gpt-4", temperature=0, max_retries=1)
            .invoke(ai_messages)
            .content
        )
        if response.strip().lower() == "none":
            return {"revision": None}
        else:
            return {"revision": response}

    def run(self, materials: dict):
        filtered_sources = self.filter_sources(materials["query"], materials["sources"])
        materials["filtered_sources"] = filtered_sources
        revision_feedback = self.revise_sources(materials)
        materials.update(revision_feedback)
        return materials
