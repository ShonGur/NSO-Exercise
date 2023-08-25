from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Function to create the database and messages table if they don't exist
def initialize_database():
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

    conn.commit()
    conn.close()

# Initialize the database
initialize_database()

@app.route('/AddMessage', methods=['POST'])
def add_message():
    try:
        data = request.json
        conn = sqlite3.connect('messages.db')
        cursor = conn.cursor()

        # Check if a message with the same messageId already exists
        cursor.execute('SELECT * FROM messages WHERE message_id = ?', (data['message_id'],))
        existing_message = cursor.fetchone()

        if existing_message:
            conn.close()
            return jsonify({'error': 'Message with the same messageId already exists'}), 400

        cursor.execute('''
            INSERT INTO messages (application_id, session_id, message_id, participants, content)
            VALUES (?, ?, ?, ?, ?)
        ''', (data['application_id'], data['session_id'], data['message_id'], ','.join(data['participants']), data['content']))

        conn.commit()
        conn.close()
        return jsonify({'message': 'Message added successfully'}), 201
    except Exception as e:
        return jsonify({'error': 'Invalid data format'}), 400

@app.route('/GetMessage', methods=['GET'])
def get_message():
    criteria = request.args.get('criteria')
    value = request.args.get('value')

    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()

    if criteria == 'applicationId':
        cursor.execute('SELECT * FROM messages WHERE application_id = ?', (value,))
    elif criteria == 'sessionId':
        cursor.execute('SELECT * FROM messages WHERE session_id = ?', (value,))
    elif criteria == 'messageId':
        cursor.execute('SELECT * FROM messages WHERE message_id = ?', (value,))
    else:
        conn.close()
        return jsonify({'error': 'Invalid criteria'}), 400

    messages = cursor.fetchall()
    conn.close()

    if not messages:
        return jsonify({'error': 'Messages not found'}), 404

    return jsonify(messages), 200

@app.route('/DeleteMessage', methods=['DELETE'])
def delete_message():
    criteria = request.args.get('criteria')
    value = request.args.get('value')

    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()

    if criteria == 'applicationId':
        cursor.execute('DELETE FROM messages WHERE application_id = ?', (value,))
    elif criteria == 'sessionId':
        cursor.execute('DELETE FROM messages WHERE session_id = ?', (value,))
    elif criteria == 'messageId':
        cursor.execute('DELETE FROM messages WHERE message_id = ?', (value,))
    else:
        conn.close()
        return jsonify({'error': 'Invalid criteria'}), 400

    conn.commit()
    conn.close()
    return jsonify({'message': 'Messages deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
