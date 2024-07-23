import os
import logging
import json

class WebsiteAgent:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        logging.basicConfig(level=logging.INFO)

    def load_html_template(self, template_name):
        try:
            relative_path = os.path.join(
                os.path.dirname(__file__),
                "..",
                "templates",
                template_name,
            )
            with open(relative_path, 'r') as f:
                html_template = f.read()
            return html_template
        except FileNotFoundError:
            logging.error(f"Error: {template_name} file not found.")
            return None
        except Exception as e:
            logging.error(f"Error loading {template_name}: {str(e)}")
            return None

    def generate_study_plan_html(self, sources):
        study_plan_template = self.load_html_template("study_plan.html")
        if study_plan_template is None:
            raise ValueError("Study Plan HTML template is None")
        
        study_plan_html = ""
        for source in sources:
            title = source.get('title', 'No Title')
            url = source.get('url', '#')
            description = source.get('description', 'No Description')

            material_html = study_plan_template
            material_html = material_html.replace("{{title}}", title)
            material_html = material_html.replace("{{url}}", url)
            material_html = material_html.replace("{{description}}", description)
            study_plan_html += material_html

        return study_plan_html

    def generate_study_schedule_html(self, schedule):
        study_schedule_template = self.load_html_template("study_schedule.html")
        if study_schedule_template is None:
            raise ValueError("Study Schedule HTML template is None")

        study_schedule_html = ""
        for session in schedule:
            session_number = str(session.get('session', 'N/A'))
            task = session.get('task', 'No Task')
            duration = str(session.get('duration', 'N/A'))
            break_time = str(session.get('break', 'N/A'))

            session_html = study_schedule_template
            session_html = session_html.replace("{{session}}", session_number)
            session_html = session_html.replace("{{task}}", task)
            session_html = session_html.replace("{{duration}}", duration)
            session_html = session_html.replace("{{break}}", break_time)
            study_schedule_html += session_html

        return study_schedule_html

    def designer(self, result):
        if not isinstance(result, dict):
            raise TypeError(f"Expected result to be a dict, got {type(result)}")

        index_template = self.load_html_template("index.html")
        if index_template is None:
            raise ValueError("Index HTML template is None")

        study_plan_html = self.generate_study_plan_html(result.get('sources', []))
        study_schedule_html = self.generate_study_schedule_html(result.get('schedule', []))

        index_template = index_template.replace("{{title}}", result.get('title', 'Study Plan'))
        index_template = index_template.replace("{{study_plan}}", study_plan_html)
        index_template = index_template.replace("{{study_schedule}}", study_schedule_html)

        result["html"] = index_template
        return result

    def save_schedule_html(self, result:dict):
        try:
            os.makedirs(self.output_dir, exist_ok=True)
            filename = "study_assistant.html"
            path = os.path.join(self.output_dir, filename)
            html_content = result.get("html")
            if html_content is None:
                raise ValueError("HTML content is None")
            with open(path, "w") as file:
                file.write(html_content)
            result["path"] = path
            return result
        except Exception as e:
            logging.error(f"Error saving HTML file: {str(e)}")
            return None

    def run(self, article: dict):
        logging.info(f"Received article structure: {json.dumps(article, indent=2)}")
        article = self.designer(article)
        if article:
            return self.save_schedule_html(article)
        return None