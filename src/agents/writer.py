from crewai import Agent

from src.config import build_llm
from src.tools.save_tool import SaveTool


def create_writer(verbose: bool = False) -> Agent:
    return Agent(
        role="Technical Writer",
        goal="Synthesize research findings into a clear, well-structured markdown report with proper citations",
        backstory=(
            "You are an experienced technical writer who transforms complex "
            "research into accessible, well-organized documents. You excel at "
            "creating structured reports with clear headings, bullet points, "
            "and proper citations. You ensure every claim is backed by a source."
        ),
        tools=[SaveTool()],
        llm=build_llm(temperature=0.5),
        max_iter=3,
        verbose=verbose,
    )
