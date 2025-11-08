#!/usr/bin/env python
import sys
import warnings
from datetime import datetime

from financial_researcher.crew import FinancialResearcher

# Silence noisy pysbd warnings (used by some LLM text processing)
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the FinancialResearcher crew.
    This function initializes the crew, executes it with input parameters,
    and prints (and optionally saves) the output report.
    """
    print("\n🚀 Starting Financial Researcher Crew...\n")

    # Instantiate the crew
    financial_crew = FinancialResearcher()

    # Define your input topic for gold market analysis
    topic = "Gold Market Analysis and Price Trends November 2025"

    # Run the crew
    result = financial_crew.financial_researcher_crew().kickoff(
        inputs={"topic": topic}
    )

    # Print final result to terminal
    print("\n✅ Crew Execution Completed!\n")
    print("🧾 Final Output:\n")
    print(result)

    # Optional: save a timestamped log file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"financial_report_{timestamp}.md"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(result if isinstance(result, str) else str(result))

    print(f"\n📁 Report saved to: {output_file}\n")


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        print("\n🛑 Crew execution interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error running crew: {e}")
        sys.exit(1)
