import os
import time
from langgraph.graph import Graph
from concurrent.futures import ThreadPoolExecutor

from .agents import (
    MaterialAgent,
    RevisorAgent,
    PublishAgent,
    QnaAgent,
    SchedulerAgent,
    StudyAgent,
)


class MainAgent:
    def __init__(self):
        self.output_dir = f"outputs/run_{int(time.time())}"
        os.makedirs(self.output_dir, exist_ok=True)

    def run(self, queries: list):
        material_agent = MaterialAgent()
        revisor_agent = RevisorAgent()
        scheduler_agent = SchedulerAgent()
        publish_agent = PublishAgent(self.output_dir)
        qna_agent = QnaAgent()
        study_agent = StudyAgent()

        builder = Graph()

        builder.add_node("browse", material_agent.run)
        builder.add_node("revise", revisor_agent.run)
        builder.add_node("schedule", scheduler_agent.run)
        builder.add_node("study", study_agent.run)

        builder.add_edge("browse", "revise")
        builder.add_conditional_edges(
            start_key="revise",
            condition=lambda x: "accept" if x["revise"] is None else "correct",
            conditional_edge_mapping={"accept": "schedule", "correct": "browse"},
        )
        builder.add_edge("revise", "schedule")
        builder.add_edge("schedule", "study")

        builder.set_entry_point("browse")
        builder.set_finish_point("study")
        
        graph = builder.compile()

        with ThreadPoolExecutor() as executor:
            results = list(executor.map(lambda q: graph.invoke({"query": q}), queries))

        studyAssistant_html = publish_agent.run(results)

        return studyAssistant_html
