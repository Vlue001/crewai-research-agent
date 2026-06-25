import argparse
import os
import sys
from pathlib import Path

# Windows consoles default to the cp1252 codepage, which can't encode characters
# like ✓ or em-dashes that routinely appear in agent output and CrewAI's verbose
# logs. Force UTF-8 so printing never crashes the run, regardless of the console.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

from dotenv import load_dotenv  # noqa: E402  (must follow the stdout reconfigure)

load_dotenv()

from src.crew import ResearchCrew  # noqa: E402  (must import after load_dotenv)

REQUIRED_KEYS = ("ANTHROPIC_API_KEY", "SERPER_API_KEY")


def check_api_keys() -> None:
    """Fail fast with a clear message if required API keys are missing."""
    missing = [key for key in REQUIRED_KEYS if not os.getenv(key)]
    if missing:
        print(
            "Error: missing required environment variable(s): "
            + ", ".join(missing),
            file=sys.stderr,
        )
        print(
            "Copy .env.example to .env and fill in your API keys.",
            file=sys.stderr,
        )
        sys.exit(1)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="AI Research Agent — generate a structured markdown report on any topic",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            '  python main.py "quantum computing"\n'
            '  python main.py "climate change solutions" --verbose\n'
        ),
    )
    parser.add_argument(
        "topic",
        type=str,
        help="The topic to research (wrap multi-word topics in quotes)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed agent activity during the run",
    )
    return parser.parse_args()


def find_new_reports(before: set[Path]) -> list[Path]:
    """Return .md files in outputs/ that did not exist before the run."""
    outputs = Path("outputs")
    if not outputs.is_dir():
        return []
    return sorted(set(outputs.glob("*.md")) - before)


def main() -> None:
    args = parse_args()
    topic = args.topic.strip()

    if not topic:
        print("Error: topic cannot be empty.", file=sys.stderr)
        sys.exit(1)

    check_api_keys()
    Path("outputs").mkdir(exist_ok=True)
    existing_reports: set[Path] = set(Path("outputs").glob("*.md"))

    print(f"\nStarting research on: {topic}")
    print("This may take a few minutes...\n")

    try:
        crew = ResearchCrew(topic=topic, verbose=args.verbose)
        result = crew.run()
    except KeyboardInterrupt:
        print("\nInterrupted by user.", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"\nResearch failed: {e}", file=sys.stderr)
        sys.exit(1)

    print("\n" + "=" * 60)
    print("Research complete!")
    new_reports = find_new_reports(existing_reports)
    if new_reports:
        for path in new_reports:
            print(f"Report saved to: {path}")
    else:
        print("Report saved to the outputs/ directory.")
    print("=" * 60)

    if args.verbose:
        print("\nFinal output:\n")
        print(result)


if __name__ == "__main__":
    main()
