from flask import Flask, render_template, g, request, make_response, redirect, url_for, Response
import os
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/catalog')
def show_catalog():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, title, artist, year, genre FROM records")
    rows = cursor.fetchall()

    # Map the rows to dictionaries
    records = [{'id': row[0], 'title': row[1], 'artist': row[2], 'year': row[3], 'genre': row[4]} for row in rows]

    return render_template('catalog.html', records=records)


@app.route('/modal-add-record')
def show_add_record_modal():
    html = '''
            <div id="modal" _="on closeModal add .closing then wait for animationend then remove me">
                <div class="modal-underlay" _="on click trigger closeModal"></div>
                    <div class="modal-content">
                        <div class="flex justify-center align-middle mb-7"><h1>Add a Record</h1></div>
                          <form method="POST" action="/submit-record-form" class="max-w-sm mx-auto p-4 bg-white border rounded-lg shadow space-y-4">
                            <div>
                                <label class="block text-sm font-medium text-gray-700">Title</label>
                                <input type="text" required name="title" class="w-full mt-1 border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500" />
                            </div>

                            <div>
                                <label class="block text-sm font-medium text-gray-700">Artist</label>
                                <input type="text" required name="artist" class="w-full mt-1 border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500" />
                            </div>

                            <div>
                                <label class="block text-sm font-medium text-gray-700">Year</label>
                                <input type="text" required name="year" class="w-full mt-1 border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"></textarea>
                            </div>

                            <div>
                                <label class="block text-sm font-medium text-gray-700">Genre</label>
                                <input type="text" required name="genre" class="w-full mt-1 border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"></textarea>
                            </div>

                            <button type="submit" class="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700">
                                Submit
                            </button>
                            <button type="button" class="w-full bg-red-600 text-white py-2 rounded hover:bg-red-700" _="on click trigger closeModal">Close</button>
                            </form>
                        <br>
                        <br>
                    </div>
                </div>
            </div>
            '''
    return html

DATABASE = os.path.join(app.root_path, 'database.db')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def init_db():
    if not os.path.exists(DATABASE):
        print("Creating database...")
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            artist TEXT NOT NULL,
            year TEXT NOT NULL,
            genre TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/submit-record-form', methods=['POST'])
def submit_record_form():
    if request.method == 'POST':
        title = request.form.get('title')
        artist = request.form.get('artist')
        year = request.form.get('year')
        genre = request.form.get('genre')

        if not title or not artist or not year or not genre:
            return make_response("Invalid input", 422)

        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO records (title, artist, year, genre) VALUES (?, ?, ?, ?)", (title, artist, year, genre))
        db.commit()

        return redirect(url_for('show_catalog'))
    

@app.route('/delete-record/<int:record_id>', methods=['POST'])
def delete_record(record_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM records WHERE id = ?", (record_id,))
    db.commit()
    return redirect(url_for('show_catalog'))



@app.route('/edit_record/<int:record_id>', methods=['GET', 'PUT'])
def edit_record(record_id):
    if request.method == 'GET':
        # Fetch your record from a database here (this is mocked for now)
        record = {
            "title": "Joe",
            "artist": "Blow",
            "year": "1990",
            "genre": "Jazz"
        }
        html = f'''
        <form hx-put="/edit_record/{record_id}" hx-target="this" hx-swap="outerHTML">
            <div>
                <label>Title</label>
                <input type="text" name="title" value="{record['title']}">
            </div>
            <div class="form-group">
                <label>Artist</label>
                <input type="text" name="artist" value="{record['artist']}">
            </div>
            <div class="form-group">
                <label>Year</label>
                <input type="text" name="year" value="{record['year']}">
            </div>
            <div class="form-group">
                <label>Genre</label>
                <input type="text" name="genre" value="{record['genre']}">
            </div>
            <button class="btn" type="submit">Submit</button>
            <button class="btn" hx-get="/cancel_record_edit/{record_id}">Cancel</button>
        </form>
        '''
        return html
    elif request.method == 'PUT':
        title = request.form.get('title')
        artist = request.form.get('artist')
        year = request.form.get('year')
        genre = request.form.get('genre')

        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            UPDATE records
            SET title = ?, artist = ?, year = ?, genre = ?
            WHERE id = ?
        """, (title, artist, year, genre, record_id))
        db.commit()
        html='''
            <div class="p-4" hx-target="this" hx-swap="outerHTML">
                <h3 class="text-lg font-semibold">{{ record.title }}</h3>
                <p class="text-sm text-gray-600 dark:text-gray-400">{{ record.artist }}</p>
                <p class="text-sm text-gray-500 dark:text-gray-500">Released: {{ record.year }}</p>
                <p class="text-sm text-gray-500 dark:text-gray-500">Genre: {{ record.genre }}</p>

                <!-- Action Buttons -->
                <div class="mt-4 flex space-x-2">
                    <button class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 text-sm font-medium" hx-get="/edit_record/{{ record.id }}">
                        Modify
                    </button>
                    <form method="POST" action="{{ url_for('delete_record', record_id=record.id) }}" onsubmit="return confirm('Are you sure you want to delete this record?');">
                        <button type="submit" class="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700 text-sm font-medium">
                            Delete
                        </button>
                    </form>
                </div>
            </div>
            '''
        return html

    
@app.route('/cancel_record_edit/<int:record_id>', methods=['GET'])
def cancel_record_edit(record_id):
    html = f'''
        <div class="p-4" hx-target="this" hx-swap="outerHTML">
            <h3 class="text-lg font-semibold">{{ record.title }}</h3>
            <p class="text-sm text-gray-600 dark:text-gray-400">{{ record.artist }}</p>
            <p class="text-sm text-gray-500 dark:text-gray-500">Released: {{ record.year }}</p>
            <p class="text-sm text-gray-500 dark:text-gray-500">Genre: {{ record.genre }}</p>

            <!-- Action Buttons -->
            <div class="mt-4 flex space-x-2">
                <button class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 text-sm font-medium" hx-get="/edit_record/{{ record.id }}">
                    Modify
                </button>
                <form method="POST" action="{{ url_for('delete_record', record_id=record.id) }}" onsubmit="return confirm('Are you sure you want to delete this record?');">
                    <button type="submit" class="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700 text-sm font-medium">
                        Delete
                    </button>
                </form>
            </div>
        </div>'''
    return html


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
