# Smart Student Assistant

**Overview**

This project creates a smart student assistant designed to help users gather study materials, break them down for easier comprehension, and create a personalized study schedule to learn a desired topic efficiently. It leverages AI and natural language processing to automate the collection and simplification of learning resources, offering a tailored learning experience.

**Features**

- **Web Resource Gathering:** Utilizes AI agents to search the web for relevant learning materials like articles, videos, and tutorials.
- **Content Summarization & Simplification:** Analyzes gathered materials and creates concise summaries using natural language processing. Can simplify complex concepts into easier-to-understand language upon request.
- **Personalized Study Schedule:** Based on user preferences and learning pace, creates a schedule that breaks down learning into manageable chunks and incorporates various resources.

**Modules**

The project is organized into several modules:

- **agents**

  - `sources_agent.py`: Gathers study materials from web sources based on user queries.
  - `filter_agent.py`: Filters and selects the three most relevant resources based on user preferences and topic.
  - `revisor_agent.py`: Analyzes the schedule created by `scheduler_agent` and suggests improvements like rearranging tasks for better flow or identifying knowledge gaps that might require additional resources.
  - `scheduler_agent.py`: Generates a personalized study schedule based on user input, content length, and preferred learning pace.
  - `website_agent.py`: Handles communication with a user interface if implemented as a web application. It takes the revised schedule and creates the HTML template for displaying it to the user.
  - `publish_agent.py`: Prepares the final study plan for user access (e.g., saving to a file, setting up a path).

- **templates**: Contains HTML templates for user interface elements like `index.html`, `study_plan.html`, and `study_schedule.html` for displaying the study materials and schedules to the user.

- **frontend**: Contains frontend code for the application, including HTML (`index.html`), JavaScript (`script.js`), and CSS (`style.css`) files, providing the user interface and styling for the web application.

- **outputs**: Stores output files generated by the program, such as study schedules and summaries, facilitating easy access and review by the user.

- **others**: Standard project files like `.env`, `.gitignore`, `app.py`, `requirements.txt`, etc., supporting the application's configuration, dependencies, and execution.

**Agent Workflow**

The agents work together in a specific order to provide a comprehensive and personalized study experience:

1. **Sources Agent:** Starts by gathering information based on the user's query.
2. **Filter Agent:** Analyzes the gathered information and selects the three most relevant sources.
3. **Scheduler Agent:** Creates a preliminary study schedule based on the filtered resources.
4. **Revisor Agent:** Analyzes the generated schedule and suggests improvements for better flow or identifies areas where additional resources might be needed.
5. **Website Agent (Optional):** If a web interface exists, it takes the final revised schedule and creates an HTML template for displaying it to the user.
6. **Publish Agent:** Prepares the final study plan for user access by saving it to a designated location.

**Getting Started**

1.  **Prerequisites:**

    - Python 3.x installed ([https://www.python.org/downloads/](https://www.python.org/downloads/))
    - Required libraries installed: `pip install -r requirements.txt`
    - (Optional) API keys for external services like Tavily or OpenAI (see API Usage)

2.  **API Usage**

    - **Tavily**:

      - Create a Tavily account and obtain an API key ([https://tavily.com/](https://tavily.com/))
      - Set the `TAVILY_API_KEY` environment variable in your `.env` file.

    - **OpenAI**:
      - Create an OpenAI account and obtain an API key ([https://openai.com/](https://openai.com/))
      - Set the `OPENAI_API_KEY` environment variable in your `.env` file.

3.  **Installation:**

    1. Clone the repo

       ```bash
       git clone https://github.com/Alejandrovc0/smart_study_assistant.git
       ```

    2. Install required dependencies:

       ```bash
       pip install -r requirements.txt
       ```

    3. (Optional) Set up a development environment using Docker:

       ```bash
       # Build the Docker image
       docker-compose build

       # Run the application
       docker-compose up
       ```

    4. Run the application:

       ```bash
       python app.py
       ```

**Contributing**

We welcome contributions to this project!

**License**

This project is licensed under the MIT License. For more information, see the [LICENSE](LICENSE) file.

**Inspired By**

This project was inspired by GPT Newspaper (https://github.com/rotemweiss57/gpt-newspaper.git).  The overall concept of using multiple agents to create a smart assistant informed the design of this project. 

**Key Differences**

While inspired by the overall approach, this project focuses on creating a study assistant with specific functionalities like content summarization, schedule revision, and knowledge graph integration (if applicable).

