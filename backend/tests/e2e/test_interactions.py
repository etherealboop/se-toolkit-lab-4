"""End-to-end tests for the GET /interactions endpoint."""
import httpx


def test_get_interactions_returns_200(client: httpx.Client) -> None:
    response = client.get("/interactions/")
    assert response.status_code == 200


def test_get_interactions_response_is_a_list(client: httpx.Client) -> None:
    response = client.get("/interactions/")
    assert isinstance(response.json(), list)


def test_get_interactions_filter_by_nonexistent_item_id_returns_empty_list(
    client: httpx.Client,
) -> None:
    """Test that filtering by a non-existent item_id returns an empty list."""
    response = client.get("/interactions/", params={"item_id": 999999})
    assert response.status_code == 200
    assert response.json() == []


def test_get_interactions_filter_by_negative_item_id_returns_empty_list(
    client: httpx.Client,
) -> None:
    """Test that filtering by a negative item_id returns an empty list."""
    response = client.get("/interactions/", params={"item_id": -1})
    assert response.status_code == 200
    assert response.json() == []


def test_post_interaction_with_empty_kind_returns_422(
    client: httpx.Client,
) -> None:
    """Test that creating an interaction with empty kind returns 422 Unprocessable Entity."""
    payload = {"learner_id": 1, "item_id": 1, "kind": ""}
    response = client.post("/interactions/", json=payload)
    assert response.status_code == 422


def test_post_interaction_with_nonexistent_learner_or_item_returns_422(
    client: httpx.Client,
) -> None:
    """Test that creating an interaction with non-existent learner_id or item_id returns 422."""
    payload = {"learner_id": 999999, "item_id": 999999, "kind": "attempt"}
    response = client.post("/interactions/", json=payload)
    assert response.status_code == 422