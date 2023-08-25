import json
import pytest
import sqlite3
from Server import app

# Fixture to create a test client for the Flask app and initialize/cleanup the test database
@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    initialize_test_database()  # Initialize the test database
    yield client
    cleanup_test_database()  # Cleanup the test database after tests

# Function to initialize the test database with sample data
def initialize_test_database():
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY,
            application_id INTEGER,
            session_id TEXT,
            message_id TEXT,
            participants TEXT,
            content TEXT
        )
    ''')

    test_messages = [
        (1, 'aaaa', 'bbbb', 'avi aviv,moshe cohen', 'Hi, how are you today?'),
        (2, 'cccc', 'dddd', 'john doe,jane smith', 'Hello from another session.'),
    ]

    cursor.executemany('''
        INSERT INTO messages (application_id, session_id, message_id, participants, content)
        VALUES (?, ?, ?, ?, ?)
    ''', test_messages)

    conn.commit()
    conn.close()

# Function to cleanup the test database
def cleanup_test_database():
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()

    # Clear all data from the messages table
    cursor.execute('DELETE FROM messages')

    conn.commit()
    conn.close()

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
    response = client.get('/GetMessage?criteria=messageId&value=ffff')
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert len(data) == 1

    # Iterate through each message and assert the content
    for message in data:
        assert message[5] == "Hello, Flask!"

def test_get_messages(client):
    # Test getting messages by applicationId
    response = client.get('/GetMessage?criteria=applicationId&value=1')
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert len(data) == 1

    # Test getting messages by sessionId
    response = client.get('/GetMessage?criteria=sessionId&value=aaaa')
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert len(data) == 1

    # Test getting a single message by messageId
    response = client.get('/GetMessage?criteria=messageId&value=bbbb')
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert len(data) == 1

def test_delete_messages_by_application_id(client):
    response = client.delete('/DeleteMessage?criteria=applicationId&value=1')
    assert response.status_code == 200

    # Verify that messages with applicationId 1 are deleted
    response = client.get('/GetMessage?criteria=applicationId&value=1')
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 404
    assert len(data) == 1

def test_delete_messages_by_session_id(client):
    response = client.delete('/DeleteMessage?criteria=sessionId&value=aaaa')
    assert response.status_code == 200

    # Verify that messages with sessionId 'aaaa' are deleted
    response = client.get('/GetMessage?criteria=sessionId&value=aaaa')
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 404
    assert len(data) == 1

def test_delete_message_by_message_id(client):
    response = client.delete('/DeleteMessage?criteria=messageId&value=bbbb')
    assert response.status_code == 200

    # Verify that the message with messageId 'bbbb' is deleted
    response = client.get('/GetMessage?criteria=messageId&value=bbbb')
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 404
    assert len(data) == 1
