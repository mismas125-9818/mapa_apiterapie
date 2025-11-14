from flask import Flask, jsonify, render_template, request, redirect, url_for
import sqlite3, os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'static/fotky'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_db():
    conn = sqlite3.connect('databaza.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/helpers')
def get_helpers():
    filter_lang = request.args.get("jazyk", "")
    conn = get_db()
    cur = conn.cursor()
    if filter_lang:
        cur.execute("SELECT * FROM helpers WHERE jazyk LIKE ?", ('%'+filter_lang+'%',))
    else:
        cur.execute("SELECT * FROM helpers")
    data = [dict(row) for row in cur.fetchall()]
    conn.close()
    return jsonify(data)

@app.route('/api/add', methods=['POST'])
def add_helper():
    data = request.form
    foto_file = request.files.get('foto')
    filename = None
    if foto_file and foto_file.filename != '':
        filename = secure_filename(foto_file.filename)
        foto_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO helpers (meno, odbor, lat, lng, telefon, email, foto, adresa, jazyk) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (data['meno'], data['odbor'], data['lat'], data['lng'], data.get('telefon'), data.get('email'), filename, data.get('adresa'), data['jazyk'])
    )
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

@app.route('/api/update/<int:id>', methods=['POST'])
def update_helper(id):
    data = request.form
    foto_file = request.files.get('foto')
    filename = None
    if foto_file and foto_file.filename != '':
        filename = secure_filename(foto_file.filename)
        foto_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    conn = get_db()
    cur = conn.cursor()
    if filename:
        cur.execute(
            "UPDATE helpers SET lat=?, lng=?, telefon=?, email=?, foto=?, jazyk=? WHERE id=?",
            (data['lat'], data['lng'], data.get('telefon'), data.get('email'), filename, data['jazyk'], id)
        )
    else:
        cur.execute(
            "UPDATE helpers SET lat=?, lng=?, telefon=?, email=?, jazyk=? WHERE id=?",
            (data['lat'], data['lng'], data.get('telefon'), data.get('email'), data['jazyk'], id)
        )
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

@app.route('/api/delete/<int:id>', methods=['POST'])
def delete_helper(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM helpers WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

@app.route('/admin')
def admin():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM helpers")
    helpers = cur.fetchall()
    conn.close()
    return render_template('admin.html', helpers=helpers)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)
