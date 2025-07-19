from flask import Flask, render_template, g
import os
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/catalog')
def show_catalog():
    return render_template('catalog.html')

@app.route('/modal-add-record')
def show_add_record_modal():
    html = '''
            <div id="modal" _="on closeModal add .closing then wait for animationend then remove me">
                <div class="modal-underlay" _="on click trigger closeModal"></div>
                    <div class="modal-content">
                        <div class="flex justify-center align-middle mb-7"><h1>Add a Record</h1></div>
                            <form class="max-w-sm mx-auto p-4 bg-white border rounded-lg shadow space-y-4">
                            <div>
                                <label class="block text-sm font-medium text-gray-700">Title</label>
                                <input type="text" class="w-full mt-1 border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500" />
                            </div>

                            <div>
                                <label class="block text-sm font-medium text-gray-700">Artist</label>
                                <input type="text" class="w-full mt-1 border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500" />
                            </div>

                            <div>
                                <label class="block text-sm font-medium text-gray-700">Year</label>
                                <input type="text" class="w-full mt-1 border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"></textarea>
                            </div>

                            <div>
                                <label class="block text-sm font-medium text-gray-700">Genre</label>
                                <input type="text" class="w-full mt-1 border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"></textarea>
                            </div>

                            <button type="submit" class="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700">
                                Submit
                            </button>
                            <button class="w-full bg-red-600 text-white py-2 rounded hover:bg-red-700" _="on click trigger closeModal">Close</button>
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

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run(debug=True)
