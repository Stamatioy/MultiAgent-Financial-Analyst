from __future__ import annotations

import argparse
from datetime import datetime, timezone

from financial_analyst.agents.news_agent import (
    NewsAnalystAgent,
)
from financial_analyst.database.connection import (
    get_database_connection,
)
from financial_analyst.database.news_repository import (
    NewsRepository,
)
from financial_analyst.news.service import NewsService
from financial_analyst.news.yahoo_provider import (
    YahooNewsProvider,
)
from financial_analyst.validation.ticker import (
    normalize_ticker,
)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Retrieve recent company news and analyze "
            "distinct events with the local News Analyst."
        )
    )

    parser.add_argument(
        "ticker",
        help="Ticker such as AMD, MSFT or AAPL.",
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=15,
        help="Maximum number of articles passed to the LLM.",
    )

    parser.add_argument(
        "--cached-only",
        action="store_true",
        help="Do not retrieve new news.",
    )

    parser.add_argument(
        "--as-of",
        type=str,
        default=None,
        help=(
            "Analyze only news available at or before this "
            "ISO date/time."
        ),
    )

    parser.add_argument(
        "--show-articles",
        action="store_true",
        help="Print article metadata before the analysis.",
    )

    return parser.parse_args()


def parse_as_of(
    value: str | None,
) -> datetime | None:
    if value is None:
        return None

    text = value.strip()

    if text.endswith("Z"):
        text = text[:-1] + "+00:00"

    parsed = datetime.fromisoformat(text)

    if parsed.tzinfo is None:
        parsed = parsed.replace(
            tzinfo=timezone.utc
        )

    return parsed.astimezone(
        timezone.utc
    )


def main() -> None:
    args = parse_arguments()

    if args.limit < 1 or args.limit > 50:
        raise ValueError(
            "--limit must be between 1 and 50."
        )

    ticker = normalize_ticker(
        args.ticker
    )

    as_of = parse_as_of(
        args.as_of
    )

    connection = get_database_connection()

    try:
        repository = NewsRepository(
            connection
        )

        if not args.cached_only:
            service = NewsService(
                provider=YahooNewsProvider(),
                repository=repository,
            )

            service.refresh(
                ticker=ticker,
                limit=args.limit,
            )

        if as_of is None:
            articles = (
                repository.get_recent_article_models(
                    ticker=ticker,
                    limit=args.limit,
                )
            )
        else:
            articles = (
                repository.get_article_models_as_of(
                    ticker=ticker,
                    as_of=as_of,
                    limit=args.limit,
                )
            )

        if not articles:
            raise RuntimeError(
                f"No news available for {ticker}."
            )

        if args.show_articles:
            print("SOURCE ARTICLES")

            for article in articles:
                print(
                    f"\n[{article.article_id[:12]}] "
                    f"{article.title}"
                )

                print(
                    f"Publisher: {article.publisher}"
                )

                print(
                    f"Published: {article.published_at}"
                )

                if article.summary:
                    print(
                        f"Summary: {article.summary}"
                    )

            print()

        agent = NewsAnalystAgent()

        result = agent.analyze(
            ticker=ticker,
            articles=articles,
        )

        print("NEWS ANALYST OUTPUT")
        print(
            result.model_dump_json(
                indent=2
            )
        )

    finally:
        connection.close()


if __name__ == "__main__":
    main()