import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from firewall import sanitize_text
import sqlite3

DB_NAME = 'mandemos.db'


def _ensure_db():
    """Create the keyword_usage table if it doesn't exist."""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS keyword_usage ("
        "clone_id TEXT NOT NULL, "
        "keyword TEXT NOT NULL, "
        "count INTEGER NOT NULL DEFAULT 0, "
        "PRIMARY KEY (clone_id, keyword)"
        ")"
    )
    conn.commit()
    conn.close()

# Track keyword usage across clones
KEYWORDS = {"glitch", "frequency", "vibration", "null"}
keyword_stats = {}


def _update_keyword_stats(clone_id, text):
    """Increment keyword counts for the given clone based on text."""
    words = text.lower().split()
    stats = keyword_stats.setdefault(clone_id, {k: 0 for k in KEYWORDS})
    updates = {}
    for kw in KEYWORDS:
        inc = sum(1 for w in words if kw in w)
        if inc:
            stats[kw] += inc
            updates[kw] = stats[kw]

    if updates:
        try:
            _ensure_db()
            conn = sqlite3.connect(DB_NAME)
            cur = conn.cursor()
            for kw, count in updates.items():
                cur.execute(
                    "INSERT INTO keyword_usage (clone_id, keyword, count) "
                    "VALUES (?, ?, ?) "
                    "ON CONFLICT(clone_id, keyword) DO UPDATE SET count=excluded.count",
                    (clone_id, kw, count),
                )
            conn.commit()
        except Exception:
            pass
        finally:
            try:
                conn.close()
            except Exception:
                pass

app = Flask(__name__)
CORS(app)

messages = []
memories = []
tasks = []
results = []

@app.route('/health', methods=['GET'])
def health():
    """Simple health check endpoint."""
    return jsonify({'status': 'ok'})

@app.route('/send', methods=['POST'])
def send_message():
    data = request.get_json(force=True)
    clone_id = data.get('id', 'unknown')
    msg = data.get('message', '')
    if msg:
        msg = sanitize_text(msg)
        messages.append(f"{clone_id}: {msg}")
        _update_keyword_stats(clone_id, msg)
        return jsonify({'status': 'ok'})
    return jsonify({'error': 'missing message'}), 400

@app.route('/read', methods=['GET'])
def read_messages():
    return '\n'.join(messages)

@app.route('/remember', methods=['POST'])
def remember_fact():
    data = request.get_json(force=True)
    clone_id = data.get('id', 'unknown')
    fact = data.get('fact', '')
    if fact:
        fact = sanitize_text(fact)
        memories.append(f"{clone_id}: {fact}")
        _update_keyword_stats(clone_id, fact)
        return jsonify({'status': 'ok'})
    return jsonify({'error': 'missing fact'}), 400

@app.route('/memories', methods=['GET'])
def get_memories():
    return '\n'.join(memories)


@app.route('/keywords', methods=['GET'])
def get_keyword_stats():
    """Return keyword usage statistics."""
    return jsonify(keyword_stats)

@app.route('/task', methods=['POST'])
def add_task():
    data = request.get_json(force=True)
    task = data.get('task')
    if task:
        task = sanitize_text(task)
        tasks.append(task)
        return jsonify({'status': 'queued'})
    return jsonify({'error': 'missing task'}), 400

@app.route('/task/assign', methods=['GET'])
def assign_task():
    if tasks:
        task = tasks.pop(0)
        return jsonify({'task': task})
    return jsonify({'task': None})

@app.route('/task/result', methods=['POST'])
def store_result():
    data = request.get_json(force=True)
    result = data.get('result')
    clone_id = data.get('id', 'unknown')
    if result is not None:
        result = sanitize_text(str(result))
        results.append(f"{clone_id}: {result}")
        return jsonify({'status': 'stored'})
    return jsonify({'error': 'missing result'}), 400

if __name__ == '__main__':
    port = int(os.getenv('CLONE_PORT', '5000'))
    app.run(host='0.0.0.0', port=port)
