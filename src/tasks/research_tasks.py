from crewai import Agent, Task


def create_research_task(agent: Agent, topic: str) -> Task:
    return Task(
        description=(
            f"Research the topic: '{topic}'\n\n"
            "Use the Web Search tool to find comprehensive information. "
            "Run at least 3-5 targeted searches to gather information from multiple angles:\n"
            "1. Search for an overview and key facts\n"
            "2. Search for recent developments or news\n"
            "3. Search for expert opinions or analysis\n"
            "4. Search for statistics or data if relevant\n\n"
            "Collect raw results including URLs, titles, and key excerpts. "
            "Do NOT filter or analyze yet — gather as much raw material as possible."
        ),
        expected_output=(
            "A comprehensive collection of raw research data including:\n"
            "- At least 10 unique sources with URLs\n"
            "- Key facts and statistics found\n"
            "- Relevant quotes or excerpts\n"
            "- A list of all search queries used"
        ),
        agent=agent,
    )


def create_analysis_task(agent: Agent, topic: str) -> Task:
    return Task(
        description=(
            f"Analyze the raw research data collected on '{topic}'.\n\n"
            "Review all research results from the previous task and:\n"
            "1. Extract the 10-15 most important facts or insights\n"
            "2. Identify recurring themes across sources\n"
            "3. Flag any contradictions or conflicting information\n"
            "4. Group findings into logical categories\n"
            "5. Prioritize information by relevance and reliability\n"
            "6. Note which sources are most authoritative\n\n"
            "Discard low-quality, redundant, or irrelevant information."
        ),
        expected_output=(
            "A structured analysis containing:\n"
            "- 10-15 key facts/insights with source citations\n"
            "- 3-5 main themes identified\n"
            "- Any contradictions or gaps noted\n"
            "- Sources ranked by reliability\n"
            "- Organized categories ready for report writing"
        ),
        agent=agent,
    )


def create_writing_task(agent: Agent, topic: str) -> Task:
    return Task(
        description=(
            f"Write a comprehensive markdown research report on '{topic}' "
            "using the analyzed findings from the previous task.\n\n"
            "Structure the report with these exact sections:\n"
            f"# {topic}\n\n"
            "## Executive Summary\n"
            "(2-3 paragraph overview of the most important findings)\n\n"
            "## Key Findings\n"
            "(Bullet-pointed list of the most important facts)\n\n"
            "## Detailed Analysis\n"
            "(2-3 subsections covering the main themes in depth)\n\n"
            "## Conclusion\n"
            "(Summary of implications and takeaways)\n\n"
            "## Sources\n"
            "(Numbered list of all sources with URLs)\n\n"
            f"After writing, use the Save Report tool with topic='{topic}' to save it to disk."
        ),
        expected_output=(
            "A complete markdown report saved to disk with:\n"
            "- Executive summary\n"
            "- Key findings section\n"
            "- Detailed analysis with subsections\n"
            "- Conclusion\n"
            "- Numbered sources list with URLs\n"
            "- Confirmation message with the saved file path"
        ),
        agent=agent,
    )
