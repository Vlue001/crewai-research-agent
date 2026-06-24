from crewai import Agent

from src.config import build_llm


def create_analyst(verbose: bool = False) -> Agent:
    return Agent(
        role="Data Analyst",
        goal="Extract key facts, identify patterns, and filter noise from raw research data",
        backstory=(
            "You are a meticulous data analyst with a talent for distilling "
            "complex information into clear, actionable insights. You excel at "
            "identifying the most relevant facts, spotting contradictions in sources, "
            "and organizing information into logical structures."
        ),
        tools=[],
        llm=build_llm(temperature=0.2),
        max_iter=3,
        verbose=verbose,
    )
