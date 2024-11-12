import sqlite3


def init_db():
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE,
            username TEXT,
            first_name TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER,
            ticket_type TEXT,
            status TEXT,
            pay_status TEXT,
            FOREIGN KEY (telegram_id) REFERENCES users (telegram_id) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    conn.close()


def add_user(telegram_id, username, first_name):
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT OR IGNORE INTO users (telegram_id, username, first_name)
        VALUES (?, ?, ?)
    ''', (telegram_id, username, first_name))

    conn.commit()
    conn.close()


def add_or_update_ticket(telegram_id, ticket_type, status, pay_status):
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT OR REPLACE INTO tickets (telegram_id, ticket_type, status, pay_status)
        VALUES (?, ?, ?, ?)
    ''', (telegram_id, ticket_type, status, pay_status))

    conn.commit()
    conn.close()


def update_payment_status(telegram_id, status):
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT ticket_id FROM tickets 
        WHERE telegram_id = ? 
        ORDER BY ticket_id DESC 
        LIMIT 1
    ''', (telegram_id,))

    last_ticket = cursor.fetchone()

    if last_ticket:
        last_ticket_id = last_ticket[0]

        cursor.execute(''' 
            UPDATE tickets 
            SET pay_status = ? 
            WHERE ticket_id = ? 
        ''', (status, last_ticket_id))

    conn.commit()
    conn.close()


init_db()
