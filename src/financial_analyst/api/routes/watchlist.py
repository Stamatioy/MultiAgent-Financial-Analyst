from __future__ import annotations

import duckdb

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from financial_analyst.api.dependencies import (
    get_database,
)

from financial_analyst.api.models import (
    WatchlistAddRequest,
    WatchlistItem,
    WatchlistResponse,
)

from financial_analyst.database.watchlist_repository import (
    WatchlistRepository,
)

from financial_analyst.validation.ticker import (
    normalize_ticker,
)


router = APIRouter(
    prefix="/api/watchlist",
    tags=[
        "watchlist"
    ],
)


@router.get(
    "",
    response_model=(
        WatchlistResponse
    ),
)
def get_watchlist(
    connection: (
        duckdb.DuckDBPyConnection
    ) = Depends(
        get_database
    ),
) -> WatchlistResponse:
    repository = (
        WatchlistRepository(
            connection
        )
    )

    items = (
        repository.list_items()
    )

    return WatchlistResponse(
        items=[
            WatchlistItem(
                **item
            )
            for item in items
        ]
    )


@router.post(
    "",
    response_model=WatchlistItem,
)
def add_to_watchlist(
    request: WatchlistAddRequest,

    connection: (
        duckdb.DuckDBPyConnection
    ) = Depends(
        get_database
    ),
) -> WatchlistItem:
    ticker = normalize_ticker(
        request.ticker
    )

    repository = (
        WatchlistRepository(
            connection
        )
    )

    repository.add(
        ticker
    )

    item = next(
        (
            item
            for item
            in repository.list_items()
            if item["ticker"]
            == ticker
        ),
        None,
    )

    if item is None:
        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to add ticker "
                "to watchlist."
            ),
        )

    return WatchlistItem(
        **item
    )


@router.delete(
    "/{ticker}",
)
def remove_from_watchlist(
    ticker: str,

    connection: (
        duckdb.DuckDBPyConnection
    ) = Depends(
        get_database
    ),
) -> dict[
    str,
    bool,
]:
    normalized = normalize_ticker(
        ticker
    )

    repository = (
        WatchlistRepository(
            connection
        )
    )

    deleted = repository.remove(
        normalized
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail=(
                "Ticker is not "
                "in the watchlist."
            ),
        )

    return {
        "deleted": True
    }