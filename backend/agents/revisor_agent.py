from datetime import datetime
from langchain.adapters.openai import convert_openai_messages
from langchain_openai import ChatOpenAI


class RevisorAgent:
    def revise_sources(self, materials: dict):
        """
        Revise relevant sources and provide feedback for a query.

        :param materials: A dictionary containing query and filtered sources.
        :return: Dictionary with revision feedback.

        """
        try:
            REVISE_PROMPT = [
                {
                    "role": "system",
                    "content": "You are an expert study advisor and critique of study materials. Your primary purpose is to review the provided study schedule and materials, and give concise feedback on their quality and relevance. This feedback will help improve the proposed study schedule.",
                },
                {
                    "role": "user",
                    "content": (
                        "Here is the schedule and its sources for review:\n"
                        f"{str(materials)}\n"
                        "Your task is to review the schedule along with the sources and provide brief feedback on how to improve them, but ONLY if necessary.\n"
                        "If there is a 'corrected' field in the schedule, it indicates a previous revision based on your feedback. You should review this corrected schedule and provide further feedback if needed.\n"
                        "If you believe the schedule is good as it is, simply return None.\n"
                        "Otherwise, provide a brief string of feedback on how to improve the schedule.\n"
                        "Ensure your feedback is clear, concise, and directly related to the quality and relevance of the materials."
                        "Please return a string of your feedback or None if no changes are needed."
                    ),
                },
            ]

            ai_messages = convert_openai_messages(REVISE_PROMPT)
            response = (
                ChatOpenAI(model="gpt-4-turbo", temperature=0, max_retries=1)
                .invoke(ai_messages)
                .content
            )
            if response == "None":
                return {"revision": None}
            else:
                if "title" in materials:
                    print(f"For article: {materials['title']}")
                print(f"Feedback: {response}\n")
                return {"revision": response, "corrected": None}
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return {"error": str(e)}

    def run(self, materials: dict):
        revision_feedback = self.revise_sources(materials)
        if revision_feedback:
            materials.update(revision_feedback)
        return materials
