import os

from crewai import LLM

# Single source of truth for the LLM. Override the model per-run with the
# RESEARCH_MODEL env var — e.g. set it to "anthropic/claude-haiku-4-5" while
# developing (cheaper), and leave it unset to use Sonnet for the real reports.
#   Haiku 4.5:  $1 / $5  per 1M tokens (input / output) — dev runs
#   Sonnet 4.5: $3 / $15 per 1M tokens — default, showcase runs
#
# NOTE: We use Sonnet 4.5 (not 4.6) because CrewAI 0.80.0 sends "assistant
# message prefill" requests, which the newer 4.6/4.7/4.8 models reject with a
# 400 error. Sonnet 4.5 still supports prefill, so it's the newest model that
# works with this CrewAI version. (Upgrading CrewAI would be the alternative.)
DEFAULT_MODEL = "anthropic/claude-sonnet-4-5"
MODEL = os.getenv("RESEARCH_MODEL", DEFAULT_MODEL)


def build_llm(temperature: float = 0.3) -> LLM:
    """Construct the shared LLM with a per-agent temperature."""
    return LLM(model=MODEL, temperature=temperature)
