from crewai import Crew, Process

from src.agents.analyst import create_analyst
from src.agents.researcher import create_researcher
from src.agents.writer import create_writer
from src.tasks.research_tasks import (
    create_analysis_task,
    create_research_task,
    create_writing_task,
)


class ResearchCrew:
    def __init__(self, topic: str, verbose: bool = False):
        self.topic = topic
        self.verbose = verbose

    def run(self) -> str:
        researcher = create_researcher(verbose=self.verbose)
        analyst = create_analyst(verbose=self.verbose)
        writer = create_writer(verbose=self.verbose)

        research_task = create_research_task(researcher, self.topic)
        analysis_task = create_analysis_task(analyst, self.topic)
        writing_task = create_writing_task(writer, self.topic)

        crew = Crew(
            agents=[researcher, analyst, writer],
            tasks=[research_task, analysis_task, writing_task],
            process=Process.sequential,
            verbose=self.verbose,
        )

        result = crew.kickoff()
        return str(result)
