from crewai import Agent

from src.config import build_llm
from src.tools.search_tool import SearchTool


def create_researcher(verbose: bool = False) -> Agent:
    return Agent(
        role="Senior Research Specialist",
        goal="Find comprehensive, accurate, and up-to-date information on the given topic from reliable web sources",
        backstory=(
            "You are a seasoned research specialist with expertise in finding "
            "reliable information across diverse topics. You know how to craft "
            "effective search queries and identify trustworthy sources. You always "
            "gather multiple perspectives and cite your sources."
        ),
        tools=[SearchTool()],
        llm=build_llm(temperature=0.3),
        max_iter=5,
        verbose=verbose,
    )
