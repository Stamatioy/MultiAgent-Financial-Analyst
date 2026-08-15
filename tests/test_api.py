from fastapi.testclient import (
    TestClient,
)

from financial_analyst.api.app import (
    app,
)


client = TestClient(
    app
)


def test_health_endpoint() -> None:
    response = client.get(
        "/api/health"
    )

    assert response.status_code == 200

    assert response.json() == {
        "status": "ok"
    }


def test_root_endpoint() -> None:
    response = client.get(
        "/"
    )

    assert response.status_code == 200

    data = response.json()

    assert (
        data["name"]
        == "Multi-Agent Financial Analyst API"
    )

    assert data["docs"] == "/docs"