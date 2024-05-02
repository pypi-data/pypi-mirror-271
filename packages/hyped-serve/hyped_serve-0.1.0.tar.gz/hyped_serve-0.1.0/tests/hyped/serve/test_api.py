from typing import Any

from fastapi.testclient import TestClient


def test_app_health(client: TestClient) -> None:
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.text == "ok"


def test_app_ready(client: TestClient) -> None:
    resp = client.get("/ready")
    assert resp.status_code == 200
    assert resp.text == "ok"


def test_app_apply(
    client: TestClient, example: dict[str, Any], out_example: dict[str, Any]
) -> None:
    resp = client.post(
        "/apply", headers={"Content-Type": "application/json"}, json=example
    )

    assert resp.status_code == 200
    assert resp.json() == out_example
