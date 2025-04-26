import json
import sqlite3
import time
import os

METRICS_FILE = "/shared/metrics.json"
DB_FILE = "/db/metrics.db"
TMP_DIR = "/tmpfs"


def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            avg_cpu REAL,
            avg_ram REAL,
            avg_disk REAL
        )
    ''')
    conn.commit()
    conn.close()


def process_metrics():
    if not os.path.exists(METRICS_FILE):
        print("bad path!")
        return

    try:
        with open(METRICS_FILE, 'r') as f:
            content = f.read()
            if not content.strip():
                return  # Plik pusty, nic nie robimy
            metric = json.loads(content)

        # Bufor tymczasowy
        tmp_file = os.path.join(TMP_DIR, "buffer.json")
        with open(tmp_file, 'w') as tmpf:
            json.dump(metric, tmpf)

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO metrics (timestamp, avg_cpu, avg_ram, avg_disk)
            VALUES (?, ?, ?, ?)
        ''', (metric["timestamp"], metric["cpu"], metric["ram"], metric["disk"]))

        conn.commit()
        conn.close()
        print("Added data to db successfully!")
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error decoding JSON or missing fields: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    init_db()
    while True:
        process_metrics()
        time.sleep(11)
