import os
import re

class PublishAgent:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir

    def load_html_template(self):
        relative_path = "../templates/study_assistant/index.html"
        dir_path = os.path.dirname(os.path.realpath(__file__))
        html_file_path = os.path.join(dir_path, relative_path)
        with open(html_file_path) as f:
            html_template = f.read()
        return html_template

    def designer(self, results):
        html_template = self.load_html_template()

        study_plan_html = "<h2>Study Plan</h2><ul>"
        for result in results:
            study_plan_html += f"<li>{result['query']}</li><ul>"
            for material in result["materials"]:
                study_plan_html += f"<li>{material['title']}</li><ul>"
                study_plan_html += f"<li>Author: {material['author']}</li>"
                study_plan_html += f"<li>Published: {material['published']}</li>"
                study_plan_html += f"<li>Feedback: {material['feedback']}</li></ul>"
            study_plan_html += "</ul>"
        study_plan_html += "</ul>"

        study_schedule_html = "<h2>Study Schedule</h2><ol>"
        for result in results:
            study_schedule_html += f"<li>{result['query']}</li><ol>"
            for session in result["schedule"]:
                study_schedule_html += f"<li>Session {session['session']}: {session['task']} (Duration: {session['duration']} minutes)</li>"
            study_schedule_html += "</ol>"
        study_schedule_html += "</ol>"

        html_template = html_template.replace("{{study_plan}}", study_plan_html)
        html_template = html_template.replace("{{study_schedule}}", study_schedule_html)

        html_filename = self.save_article_html(html_template)
        return html_filename

    def save_schedule_html(self, html_template):
        filename = "study_assistant.html"
        path = os.path.join(self.output_dir, filename)
        with open(path, 'w') as file:
            file.write(html_template)
        return filename

    def run(self, results: list):
        html_filename = self.designer(results)
        return html_filename
