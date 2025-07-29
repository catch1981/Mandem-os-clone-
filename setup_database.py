import sqlite3

# Database filename
DB_NAME = 'mandemos.db'

# Tables definitions
TABLES = {
    'scrolls': 'CREATE TABLE IF NOT EXISTS scrolls (id INTEGER PRIMARY KEY, name TEXT, description TEXT)',
    'relics': 'CREATE TABLE IF NOT EXISTS relics (id INTEGER PRIMARY KEY, name TEXT, origin TEXT)',
    'keys': 'CREATE TABLE IF NOT EXISTS keys (id INTEGER PRIMARY KEY, name TEXT, purpose TEXT)',
    'keyword_usage': (
        'CREATE TABLE IF NOT EXISTS keyword_usage ('
        'clone_id TEXT NOT NULL, '
        'keyword TEXT NOT NULL, '
        'count INTEGER NOT NULL DEFAULT 0, '
        'PRIMARY KEY (clone_id, keyword)'
        ')'
    )
}

def setup_database():
    """Create the database and tables for MandemOS artifacts."""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    for table_sql in TABLES.values():
        cur.execute(table_sql)
    conn.commit()
    conn.close()
    print(f"Database '{DB_NAME}' initialized with tables: {', '.join(TABLES.keys())}")

if __name__ == '__main__':
    setup_database()
