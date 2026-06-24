import os

from crewai import LLM

# Single source of truth for the LLM. Override the model per-run with the
# RESEARCH_MODEL env var — e.g. set it to "anthropic/claude-haiku-4-5" while
# developing (cheaper), and leave it unset to use Sonnet for the real reports.
#   Haiku 4.5: $1 / $5 per 1M tokens (input / output) — dev runs
#   Sonnet 4.6: $3 / $15 per 1M tokens — default, showcase runs
DEFAULT_MODEL = "anthropic/claude-sonnet-4-6"
MODEL = os.getenv("RESEARCH_MODEL", DEFAULT_MODEL)


def build_llm(temperature: float = 0.3) -> LLM:
    """Construct the shared LLM with a per-agent temperature."""
    return LLM(model=MODEL, temperature=temperature)
