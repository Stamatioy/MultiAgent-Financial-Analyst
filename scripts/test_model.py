from __future__ import annotations

from financial_analyst.llm.client import LocalLLMClient
from financial_analyst.llm.schemas import FinancialEventClassification


SYSTEM_PROMPT = """
You are a financial-news classification agent.

Your task is to classify only the information explicitly provided by the user.

Rules:
1. Do not invent financial figures, dates, ticker symbols, or context.
2. Do not provide investment advice.
3. Separate the factual event from its possible market interpretation.
4. Use "mixed" when the event has meaningful positive and negative aspects.
5. Materiality is measured from 1 to 5:
   - 1: negligible
   - 2: minor
   - 3: moderate
   - 4: major
   - 5: potentially transformative
6. Output must conform exactly to the requested JSON schema.
7. Do not include Markdown.
8. Do not include a thinking trace.
""".strip()


NEWS_TEXT = """
Advanced Micro Devices announced that quarterly data-center revenue increased
substantially compared with the previous year. Management also raised its
full-year revenue outlook. However, the company warned that export restrictions
could reduce sales of certain AI accelerators in some markets.
""".strip()


def main() -> None:
    client = LocalLLMClient()

    print("Checking llama.cpp server...")
    client.health_check()
    print("Server is responding.")

    result = client.generate_structured(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=f"{NEWS_TEXT}\n\n/no_think",
        response_model=FinancialEventClassification,
    )

    print("\nValidated result:")
    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    main()