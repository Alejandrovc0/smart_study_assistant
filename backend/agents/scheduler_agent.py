import os
from datetime import datetime
from langchain.adapters.openai import convert_openai_messages
from langchain_openai import ChatOpenAI
import json5 as json

sample_json = """
{
  "query": "Quantum Physics",
  "date": "today's date",
  "materials": [
    {
      "title": "Quantum Physics for Dummies",
      "url": "https://www.example.com/quantum-physics-for-dummies",
      "description": "A beginner's guide to quantum physics.",
      "author": "John Doe",
      "published": "2022-01-01"
    }
  ],
  "summary": "a paragraph summary of the sources",
}
"""

sample_revised_json = """
{
  "query": "Quantum Physics",
  "date": "today's date",
  "materials": [
    {
      "title": "Quantum Physics for Dummies",
      "url": "https://www.example.com/quantum-physics-for-dummies",
      "description": "A beginner's guide to quantum physics.",
      "author": "John Doe",
      "published": "2022-01-01",
      "feedback": "The source is well-written and provides a good introduction to quantum physics.
      The author's explanation is clear and concise. However, there are some technical terms that may be difficult for
      beginners to understand. Overall, a helpful resource for beginners."
    }
  ],
  "summary": "a paragraph summary of the sources",
  "schedule": [
    {
      "session": 1,
      "task": "Read Chapter 1 of Quantum Physics for Dummies",
      "duration": 25
    },
    {
      "session": 2,
      "task": "Take notes on key concepts from Chapter 1",
      "duration": 25
    },
    {
      "session": 3,
      "task": "Review notes and summarize key points",
      "duration": 25
    },
    {
      "session": 4,
      "task": "Complete practice problems on Chapter 1",
      "duration": 25
    },
    {
      "session": 5,
      "task": "Read Chapter 2 of Quantum Physics for Dummies",
      "duration": 25
    },
    {
      "session": 6,
      "task": "Take notes on key concepts from Chapter 2",
      "duration": 25
    },
    {
      "session": 7,
      "task": "Review notes and summarize key points",
      "duration": 25
    },
    {
      "session": 8,
      "task": "Complete practice problems on Chapter 2",
      "duration": 25
    }
  ]
}
"""

class SchedulerAgent:
    def create_schedule(self, query: str, materials: list):
        SCHEDULE_PROMPT = [{
            "role": "system",
            "content": "You are a study scheduler and time manager. Your unique purpouse is to create a detailed study schedule along with the information for each session, for a given query and study materials."
        },
        {
            "role": "user",
            "content": f"Today's date is {datetime.now().strftime('%d/%m/%Y')}\n"
            f"Topic or query: {query}\n"
            f"Here are the 3 most relevant sources for the query:\n"
            f"{materials}\n"
            f"Your task is to create a detailed study schedule based on the provided study materials. Keep in mind the student will be "
            "implementing the pomodoro technique to study so adjust accordingly.\n"
            f"Please provide nothing but a JSON in the following format:\n"
            f"{sample_json}"
        }]

        ai_messages = convert_openai_messages(SCHEDULE_PROMPT)
        optional_params = {
            "response_format": {"type": "json_object"},
        }

        response = ChatOpenAI(model='gpt-4', temperature=0, max_retries=1, model_kwargs=optional_params).invoke(ai_messages).content
        return json.loads(response)
    
    def revise_schedule(self, schedule: dict):
        REVISE_SCHEDULE_PROMPT = [{
            "role": "system",
            "content": "You are a study scheduler and time manager. Your unique purpouse is to revise a detailed study schedule along with the information for each session, for a given query and study materials."
        },
        {
            "role": "user",
            "content": f"Today's date is {datetime.now().strftime('%d/%m/%Y')}\n"
            f"Topic or query: {schedule['query']}\n"
            f"Here is the study schedule based on the provided study materials:\n"
            f"{schedule}\n"
            f"Your task is to revise the study schedule based on the feedback provided by the study advisor.\n"
            f"Please provide nothing but a JSON in the following format:\n"
            f"{sample_revised_json}"
        }]

        ai_messages = convert_openai_messages(REVISE_SCHEDULE_PROMPT)
        optional_params = {
            "response_format": {"type": "json_object"},
        }

        response = ChatOpenAI(model='gpt-4', temperature=0, max_retries=1, model_kwargs=optional_params).invoke(ai_messages).content
        return json.loads(response)
    
    def run(self, schedule: dict):
        schedule = self.revise_schedule(schedule)
        return schedule