from datetime import datetime
from langchain.adapters.openai import convert_openai_messages
from langchain_openai import ChatOpenAI
import json5 as json

sample_json = """
{
  "title": "Quantum Physics",
  "date": "today's date",
  "sources": [
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

sample_revised_json = """
{
  "title": "JavaScript Study Program",
  "date": "July 15, 2024",
  "sources": [
    {
      "title": "JavaScript for Beginners",
      "url": "https://www.example.com/javascript-for-beginners",
      "description": "A beginner's guide to JavaScript.",
      "author": "Jane Smith",
      "published": "2022-01-01",
      "feedback": "The source is well-structured and provides a comprehensive introduction to JavaScript. The author's explanations are clear and easy to understand. However, there could be more examples and exercises for practice. Overall, a great resource for beginners."
    },
    {
      "title": "JavaScript: The Good Parts",
      "url": "https://www.example.com/javascript-the-good-parts",
      "description": "A book about the good parts of JavaScript.",
      "author": "Douglas Crockford",
      "published": "2022-02-01",
      "feedback": "The source dives deep into the core concepts of JavaScript and highlights the best practices. The author's insights are valuable and the examples are concise. However, it may be challenging for absolute beginners. Recommended for intermediate learners."
    },
    {
      "title": "Eloquent JavaScript",
      "url": "https://www.example.com/eloquent-javascript",
      "description": "A comprehensive guide to JavaScript programming.",
      "author": "Marijn Haverbeke",
      "published": "2022-03-01",
      "feedback": "The source covers a wide range of JavaScript topics and provides interactive exercises for practice. The author's explanations are detailed and beginner-friendly. Highly recommended for self-paced learners."
    }
  ],
  "schedule": [
    {
      "session": 1,
      "task": "Read Chapter 1 of JavaScript for Beginners to understand basic syntax and data types.",
      "duration": 25,
      "break": 5
    },
    {
      "session": 2,
      "task": "Review notes from Chapter 1 and summarize key concepts like variables and operators.",
      "duration": 25,
      "break": 5
    },
    {
      "session": 3,
      "task": "Complete practice problems on Chapter 1 to reinforce understanding of basic JavaScript concepts.",
      "duration": 25,
      "break": 5
    },
    {
      "session": 4,
      "task": "Read Chapter 1 of JavaScript: The Good Parts to grasp essential JavaScript idioms and best practices.",
      "duration": 25,
      "break": 5
    },
    {
      "session": 5,
      "task": "Review notes from Chapter 1 and summarize key points on functions and scope.",
      "duration": 25,
      "break": 5
    },
    {
      "session": 6,
      "task": "Complete practice problems on Chapter 1 to apply best practices in JavaScript coding.",
      "duration": 25,
      "break": 5
    },
    {
      "session": 7,
      "task": "Read Chapter 1 of Eloquent JavaScript to explore advanced JavaScript concepts like objects and arrays.",
      "duration": 25,
      "break": 5
    },
    {
      "session": 8,
      "task": "Review notes from Chapter 1 and summarize key concepts on object-oriented programming.",
      "duration": 25,
      "break": 5
    },
    {
      "session": 9,
      "task": "Complete practice problems on Chapter 1 to master JavaScript's advanced features.",
      "duration": 25,
      "break": 5
    }
  ],
  "corrected": "Included more detailed examples and exercises in the JavaScript for Beginners schedule."
}=
"""


class SchedulerAgent:
    def create_schedule(self, query: str, materials: list):
        SCHEDULE_PROMPT = [
            {
                "role": "system",
                "content": "You are a study scheduler and time manager. Your unique purpose is to create a detailed study schedule with specific tasks and durations for a given query and study materials.",
            },
            {
                "role": "user",
                "content": (
                    f"Topic: {query}\n"
                    f"Here are the 3 most relevant sources for the query:\n"
                    f"{materials}\n"
                    f"Your task is to create a detailed study schedule based on the provided study materials. The student will be "
                    "implementing the Pomodoro technique, so adjust the schedule to include 25-minute study sessions followed by 5-minute breaks.\n"
                    f"Include today's date: {datetime.now().strftime('%Y-%m-%d')}\n"
                    f"If the material is complex, feel free to adjust the session durations accordingly. Even dividing it in day sessions.\n"
                    "Provide the schedule as a JSON object in the following format:\n"
                    f"{sample_json}"
                ),
            },
        ]
        ai_messages = convert_openai_messages(SCHEDULE_PROMPT)
        optional_params = {
            "response_format": {"type": "json_object"},
        }

        
        response = (
            ChatOpenAI(
                model="gpt-4-turbo",
                temperature=0,
                max_retries=1,
                model_kwargs=optional_params,
            )
            .invoke(ai_messages)
            .content
        )
        # Debugging: Print the raw response from the API
        print("Raw response from OpenAI:", response)
        try:
            parsed_response = json.loads(response)
            return parsed_response
        except json.JSONDecodeError as json_err:
            print(f"JSON decoding error: {str(json_err)}")
            raise

    def revise_schedule(self, schedule: dict):
        REVISE_SCHEDULE_PROMPT = [
            {
                "role": "system",
                "content": "You are a study scheduler and time manager. Your unique purpose is to revise a detailed study schedule along with the information for each session, for a given query and study materials.",
            },
            {
                "role": "user",
                "content": (
                    f"Here is the current schedule and its sources:\n"
                    f"{str(schedule)}\n"
                    "Your task is to edit the study schedule based on the feedback provided by the revisor.\n"
                    "Return a JSON object with the revised schedule and provide a new message in the 'corrected' field "
                    "explaining the changes made or why no changes were necessary.\n"
                    f"Include today's date: {datetime.now().strftime('%Y-%m-%d')}\n"
                    f"If the material is complex, feel free to adjust the session durations accordingly. Even dividing it in day sessions.\n"
                    "Provide the revised schedule as a JSON object in the following format:\n"
                    f"{sample_revised_json}"
                ),
            },
        ]

        ai_messages = convert_openai_messages(REVISE_SCHEDULE_PROMPT)
        optional_params = {
            "response_format": {"type": "json_object"},
        }

        response = (
            ChatOpenAI(
                model="gpt-4-turbo",
                max_retries=1,
                model_kwargs=optional_params,
            )
            .invoke(ai_messages)
            .content
        )
        # Debugging: Print the raw response from the API
        print("Raw response from OpenAI:", response)
        try:
            parsed_response = json.loads(response)
            return parsed_response
        except json.JSONDecodeError as json_err:
            print(f"JSON decoding error: {str(json_err)}")
            raise

    def run(self, schedule: dict):
      try:
          revise = schedule.get("revision")
          if revise is not None:
              revised_schedule = self.revise_schedule(schedule)
              if revised_schedule is not None:
                  schedule.update(revised_schedule)
              else:
                  raise ValueError("Failed to revise schedule.")
          else:
              created_schedule = self.create_schedule(
                  schedule["query"], schedule["sources"]
              )
              if created_schedule is not None:
                  schedule.update(created_schedule)
              else:
                  raise ValueError("Failed to create schedule.")
          
          # Validate the schedule
          if not self.validate_schedule(schedule):
              raise ValueError("Invalid schedule structure.")
          
          return schedule
      except Exception as e:
          print(f"Error in SchedulerAgent: {str(e)}")
          return None

    def validate_schedule(self, schedule):
        required_keys = ['title', 'date', 'sources', 'schedule']
        return all(key in schedule for key in required_keys)
