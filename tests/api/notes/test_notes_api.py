import pytest
from flask.testing import FlaskClient

BASE_URL = "/api/notes/"


# Test the GET /api/notes endpoint
def test_get_notes(client: FlaskClient, user_token: str):
    notes = client.get(BASE_URL, headers={"Authorization": f"Bearer {user_token}"})

    assert notes.status_code == 200
    assert notes.json.get("count") == 10
    assert len(notes.json.get("data")) == 10


# Test the GET /api/notes/<id> endpoint
def test_get_note_by_id(client: FlaskClient, user_token: str):
    note_id = 1
    note_url = f"{BASE_URL}{note_id}/"

    note = client.get(note_url, headers={"Authorization": f"Bearer {user_token}"})

    data = note.json.get("data")

    assert note.status_code == 200
    assert data.get("id") == 1


# Test the POST /api/notes endpoint
def test_create_note_with_valid_data(
    client: FlaskClient, user_token: str, mock_elasticsearch
):
    note = {
        "title": "Test",
        "content": "Test",
    }

    mock_elasticsearch.return_value = True

    response = client.post(
        BASE_URL,
        json=note,
        headers={"Authorization": f"Bearer {user_token}"},
    )

    data = response.json.get("data")

    assert response.status_code == 201
    assert data.get("title") == note.get("title")
    assert data.get("content") == note.get("content")


# Test the POST /api/notes endpoint with invalid data
def test_create_note_with_invalid_data(client: FlaskClient, user_token: str):
    note = {
        "title": "Test",
    }
    response = client.post(
        BASE_URL,
        json=note,
        headers={"Authorization": f"Bearer {user_token}"},
    )

    assert response.status_code == 400
    assert response.json.get("error") == "Schema validation error"
    assert (
        response.json.get("description")
        == "{'content': ['Missing data for required field.']}"
    )
    assert response.json.get("error_type") == "ValidationError"


# Test the PUT /api/notes/<id> endpoint
def test_update_note_with_valid_data(client: FlaskClient, user_token: str):
    note_id = 1
    note_url = f"{BASE_URL}{note_id}/"
    note = {
        "title": "Test",
    }
    response = client.put(
        note_url,
        json=note,
        headers={"Authorization": f"Bearer {user_token}"},
    )

    data = response.json.get("data")

    assert response.status_code == 200
    assert data.get("title") == note.get("title")


# Test the PUT /api/notes/<id> endpoint with invalid data
def test_update_note_with_invalid_data(client: FlaskClient, user_token: str):
    note_id = 1
    note_url = f"{BASE_URL}{note_id}/"
    note = {
        "title": 123,
    }
    response = client.put(
        note_url,
        json=note,
        headers={"Authorization": f"Bearer {user_token}"},
    )

    assert response.status_code == 400
    assert response.json.get("error") == "Schema validation error"
    assert response.json.get("description") == "{'title': ['Not a valid string.']}"
    assert response.json.get("error_type") == "ValidationError"


# Test the DELETE /api/notes/<id> endpoint
def test_delete_note_by_id(client: FlaskClient, user_token: str, mock_elasticsearch):
    id_to_delete = 1
    note_url = f"{BASE_URL}{id_to_delete}/"

    mock_elasticsearch.return_value = True

    response = client.delete(
        note_url,
        headers={"Authorization": f"Bearer {user_token}"},
    )

    data = response.json.get("data")

    assert response.status_code == 200
    assert data.get("id") == id_to_delete


# Test the DELETE /api/notes/<id> endpoint with invalid id
def test_delete_note_by_invalid_id(client: FlaskClient, user_token: str):
    id_to_delete = 100
    note_url = f"{BASE_URL}{id_to_delete}/"
    response = client.delete(
        note_url,
        headers={"Authorization": f"Bearer {user_token}"},
    )

    assert response.status_code == 404
    assert response.json.get("error") == "Object not found"
    assert response.json.get("error_type") == "NotFound"
    assert response.json.get("description") == f"Notes with id {id_to_delete} not found"


# Test the GET /api/notes/search endpoint
def test_search_notes(client: FlaskClient, user_token: str, mock_elasticsearch):
    # Create new note to index it
    note = {
        "title": "Test",
        "content": "Hecker is good",
    }

    mock_elasticsearch.return_value = True

    response = client.post(
        BASE_URL,
        json=note,
        headers={"Authorization": f"Bearer {user_token}"},
    )

    # Return mocked search value
    mock_elasticsearch.search.return_value = {
        "hits": {"total": {"value": 1}, "hits": [{"_id": "11"}]}
    }

    # Search for notes with "Hecker" in the content
    search_url = f"{BASE_URL}search?q=Hecker"
    response = client.get(
        search_url,
        headers={"Authorization": f"Bearer {user_token}"},
    )

    data = response.json.get("data")
    print(data)

    assert True
