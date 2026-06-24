import re
from datetime import datetime
from pathlib import Path
from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class SaveInput(BaseModel):
    content: str = Field(..., description="The markdown content to save to disk")
    topic: str = Field(..., description="The research topic (used for the filename)")


class SaveTool(BaseTool):
    name: str = "Save Report"
    description: str = (
        "Save the final markdown research report to disk in the outputs/ directory. "
        "Provide the full markdown content and the topic name."
    )
    args_schema: Type[BaseModel] = SaveInput

    def _run(self, content: str, topic: str) -> str:
        outputs_dir = Path("outputs")
        outputs_dir.mkdir(exist_ok=True)

        slug = re.sub(r"[^\w\s-]", "", topic.lower())
        slug = re.sub(r"[\s_]+", "-", slug).strip("-")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

        # Guard against filename collisions: datetime resolution is coarse on
        # some platforms (notably Windows), so two rapid saves can share a
        # timestamp. Append a counter so we never overwrite an existing report.
        filepath = outputs_dir / f"{slug}_{timestamp}.md"
        counter = 1
        while filepath.exists():
            filepath = outputs_dir / f"{slug}_{timestamp}_{counter}.md"
            counter += 1

        filepath.write_text(content, encoding="utf-8")
        return f"Report saved to {filepath}"
