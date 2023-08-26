import json
import pytest
import sqlite3
from Server import app

# Fixture to create a test client for the Flask app and initialize/cleanup the test database
@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client


def test_add_message(client):
    data = {
        "application_id": 1,
        "session_id": "eeee",
        "message_id": "ffff",
        "participants": ["alice", "bob"],
        "content": "Hello, Flask!"
    }

    response = client.post('/AddMessage', json=data)
    assert response.status_code == 201 or response.status_code == 400

    # Verify that the message was added by getting it and checking its content
    response = client.get('/GetMessage?criteria=message_id&value=ffff')
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert len(data) == 1

    # Iterate through each message and assert the content
    for message in data:
        assert message[5] == "Hello, Flask!"

def test_get_messages(client):
    # Test getting messages by applicationId
    response = client.get('/GetMessage?criteria=application_id&value=1')
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert len(data) == 1

    # Test getting messages by sessionId
    response = client.get('/GetMessage?criteria=session_id&value=eeee')
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert len(data) == 1

    # Test getting a single message by messageId
    response = client.get('/GetMessage?criteria=message_id&value=ffff')
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert len(data) == 1

    # Test getting message that does not exist
    response = client.get('/GetMessage?criteria=session_id&value=aaaa')
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 404
    assert len(data) == 1

def test_delete_messages_by_application_id(client):
    response = client.delete('/DeleteMessage?criteria=application_id&value=1')
    assert response.status_code == 200

    # Verify that messages with applicationId 1 are deleted
    response = client.get('/GetMessage?criteria=application_id&value=1')
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 404
    assert len(data) == 1

def test_delete_messages_by_session_id(client):
    response = client.delete('/DeleteMessage?criteria=session_id&value=eeee')
    assert response.status_code == 200

    # Verify that messages with sessionId 'aaaa' are deleted
    response = client.get('/GetMessage?criteria=session_id&value=eeee')
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 404
    assert len(data) == 1

def test_delete_message_by_message_id(client):
    response = client.delete('/DeleteMessage?criteria=message_id&value=ffff')
    assert response.status_code == 200

    # Verify that the message with messageId 'bbbb' is deleted
    response = client.get('/GetMessage?criteria=message_id&value=ffff')
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 404
    assert len(data) == 1
