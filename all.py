from flask import Flask, render_template, request, redirect, url_for, session
import firebase_admin
from firebase_admin import credentials, firestore
import os
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = 'your_secret_key_here'  # Replace with your secret key

# Firebase setup
cred = credentials.Certificate('firebase_key.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# Upload folder setup
UPLOAD_FOLDER = os.path.join('static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load poems from Firestore
def load_poems():
    poems = []
    docs = db.collection('poems').stream()
    for doc in docs:
        poem = doc.to_dict()
        poem['id'] = doc.id
        poems.append(poem)
    return poems

# Group poems by category
def get_categorized_poems(poems):
    categories = {}
    for poem in poems:
        cat = poem.get('category', 'Uncategorized')
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(poem)
    return categories

# Homepage
@app.route('/')
def index():
    poems = load_poems()
    categories = get_categorized_poems(poems)
    return render_template('index.html', categories=categories)

# Admin login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('admin'):
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == '12345':
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

# Admin logout
@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('index'))

# Admin dashboard
@app.route('/admin')
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('login'))
    return render_template('admin_dashboard.html')

# Admin upload
@app.route('/admin/post', methods=['GET', 'POST'])
def admin_post():
    if not session.get('admin'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        category = request.form['category']
        content = request.form['content']
        thumbnail_file = request.files['thumbnail']

        if thumbnail_file:
            filename = secure_filename(thumbnail_file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            thumbnail_file.save(filepath)
            thumbnail_url = url_for('static', filename=f'uploads/{filename}', _external=True)
        else:
            thumbnail_url = ""

        db.collection('poems').add({
            'title': title,
            'category': category,
            'content': content,
            'thumbnail': thumbnail_url
        })
        return redirect(url_for('index'))

    return render_template('admin_post.html')

# Admin edit
@app.route('/admin/edit')
def admin_edit():
    if not session.get('admin'):
        return redirect(url_for('login'))
    poems = load_poems()
    return render_template('admin_edit.html', poems=poems)

# Admin update
@app.route('/admin/update/<poem_id>', methods=['GET', 'POST'])
def admin_update(poem_id):
    if not session.get('admin'):
        return redirect(url_for('login'))
    poem_ref = db.collection('poems').document(poem_id)
    poem = poem_ref.get().to_dict()

    if request.method == 'POST':
        title = request.form['title']
        category = request.form['category']
        content = request.form['content']
        thumbnail_file = request.files['thumbnail']

        thumbnail_url = poem.get('thumbnail', '')
        if thumbnail_file:
            filename = secure_filename(thumbnail_file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            thumbnail_file.save(filepath)
            thumbnail_url = url_for('static', filename=f'uploads/{filename}', _external=True)

        poem_ref.update({
            'title': title,
            'category': category,
            'content': content,
            'thumbnail': thumbnail_url
        })
        return redirect(url_for('admin_edit'))

    return render_template('admin_update.html', poem=poem, poem_id=poem_id)

# Admin delete
@app.route('/admin/delete/<poem_id>')
def admin_delete(poem_id):
    if not session.get('admin'):
        return redirect(url_for('login'))
    db.collection('poems').document(poem_id).delete()
    return redirect(url_for('admin_edit'))

# Category view with poem list
@app.route('/category/<category_name>')
def view_category(category_name):
    poems = load_poems()
    categories = get_categorized_poems(poems)
    poems_in_category = categories.get(category_name, [])
    return render_template('category.html', category=category_name, poems=poems_in_category)

# Individual poem view
@app.route('/poem/<poem_id>')
def view_poem(poem_id):
    doc = db.collection('poems').document(poem_id).get()
    if not doc.exists:
        return "Poem not found", 404
    poem = doc.to_dict()
    return render_template('poem.html', poem=poem)
@app.route('/poem')
def poem_intro():
    return render_template('poem.html')


# Run the app with Render-compatible port binding
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

