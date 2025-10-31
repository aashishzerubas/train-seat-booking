from flask import Flask, send_file, jsonify, request
import os, sqlite3, random

app = Flask(__name__)

DB_FILE = "train.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS seats (
                    seat_no INTEGER PRIMARY KEY,
                    status TEXT DEFAULT 'available')''')
    if c.execute("SELECT COUNT(*) FROM seats").fetchone()[0] == 0:
        seats = [(i, random.choice(['available', 'booked'])) for i in range(1, 81)]
        c.executemany("INSERT INTO seats (seat_no, status) VALUES (?, ?)", seats)
    conn.commit()
    conn.close()

@app.route('/')
def serve_index():
    return send_file(os.path.join(os.path.dirname(__file__), "index.html"))

@app.route('/get_seats')
def get_seats():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT seat_no, status FROM seats")
    data = c.fetchall()
    conn.close()
    return jsonify(data)

@app.route('/book_seat', methods=['POST'])
def book_seat():
    seat_no = request.json.get('seat_no')
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE seats SET status='booked' WHERE seat_no=?", (seat_no,))
    conn.commit()
    conn.close()
    return jsonify({"message": f"Seat {seat_no} booked successfully!"})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
