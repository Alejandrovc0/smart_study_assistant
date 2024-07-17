import os
import logging


class PublishAgent:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        logging.basicConfig(level=logging.INFO)

    def save_schedule_html(self, html_template):
        try:
            os.makedirs(self.output_dir, exist_ok=True)
            filename = "study_assistant.html"
            path = os.path.join(self.output_dir, filename)
            with open(path, "w") as file:
                file.write(html_template)
            return path
        except Exception as e:
            logging.error(f"Error saving HTML file: {str(e)}")
            return None

    def run(self, result):
        try:
            if isinstance(result, list):
                # If result is a list, process each item
                published_files = []
                for item in result:
                    html_template = item.get("html")
                    if html_template is None:
                        raise ValueError(
                            "HTML template is missing from an input dictionary."
                        )
                    html_filename = self.save_schedule_html(html_template)
                    if html_filename is None:
                        raise ValueError("HTML template generation failed for an item.")
                    published_files.append(html_filename)
                return published_files
            elif isinstance(result, dict):
                # If result is a single dict, process it
                html_template = result.get("html")
                if html_template is None:
                    raise ValueError(
                        "HTML template is missing from the input dictionary."
                    )
                html_filename = self.save_schedule_html(html_template)
                if html_filename is None:
                    raise ValueError("HTML template generation failed.")
                return html_filename
            else:
                raise TypeError(
                    f"Expected result to be a dict or list of dicts, got {type(result)}"
                )
        except Exception as e:
            logging.error(f"Error in run: {str(e)}")
            return None
