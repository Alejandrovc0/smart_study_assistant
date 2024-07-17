import os
import time
import logging
from langgraph.graph import Graph
from concurrent.futures import ThreadPoolExecutor

from .agents import (
    SourcesAgent,
    FilterAgent,
    RevisorAgent,
    SchedulerAgent,
    PublishAgent,
    WebsiteAgent,
)


class MainAgent:
    def __init__(self):
        self.output_dir = f"outputs/run_{int(time.time())}"
        os.makedirs(self.output_dir, exist_ok=True)
        logging.basicConfig(level=logging.INFO)

    def run(self, queries: list):
        try:
            sources_agent = SourcesAgent()
            filter_agent = FilterAgent()
            revisor_agent = RevisorAgent()
            scheduler_agent = SchedulerAgent()
            publish_agent = PublishAgent(self.output_dir)
            website_agent = WebsiteAgent(self.output_dir)

            builder = Graph()

            builder.add_node("browse", sources_agent.run)
            builder.add_node("filter", filter_agent.run)
            builder.add_node("revise", revisor_agent.run)
            builder.add_node("schedule", scheduler_agent.run)
            builder.add_node("website", website_agent.run)

            builder.set_entry_point("browse")

            builder.add_edge("browse", "filter")
            builder.add_edge("filter", "schedule")
            builder.add_edge("schedule", "revise")

            builder.add_conditional_edges(
                "revise",
                lambda x: "accept" if x["revision"] is None else "revise",
                {"accept": "website", "revise": "schedule"},
            )

            builder.set_finish_point("website")

            graph = builder.compile()

            with ThreadPoolExecutor() as executor:
                results = list(
                    executor.map(lambda q: graph.invoke({"query": q}), queries)
                )

            schedule_html = website_agent.run(results)
            studyAssistant_path = publish_agent.run(schedule_html)

            return studyAssistant_path

        except Exception as e:
            logging.error(f"An error occurred during the execution: {e}")
            raise
