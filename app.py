import os
import json
import base64
import requests
from flask import Flask, flash, render_template, request, redirect, url_for, session
from google.oauth2 import service_account
from googleapiclient.discovery import build
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
FOLDER_ID = '19YX8cVSLefa-44D14wH0vcoQAAgs0OA0'

# ✅ Load credentials from environment variable (Base64 JSON string)
encoded_credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON")
if not encoded_credentials:
    raise ValueError("GOOGLE_APPLICATION_CREDENTIALS_JSON environment variable not set")

credentials_info = json.loads(base64.b64decode(encoded_credentials).decode("utf-8"))
credentials = service_account.Credentials.from_service_account_info(credentials_info, scopes=SCOPES)
service = build('drive', 'v3', credentials=credentials)

USER_DB_FILE = 'users.json'
USER_PHOTO_DB = 'user_photos.json'
ADMINS = ['Jagdish']  # Admin username list

if os.path.exists(USER_DB_FILE):
    with open(USER_DB_FILE, 'r') as f:
        users = json.load(f)
else:
    users = {
        "Jagdish": {
            "email": "admin@example.com",
            "password": generate_password_hash("Huda")
        }
    }
    with open(USER_DB_FILE, 'w') as f:
        json.dump(users, f, indent=4)

if os.path.exists(USER_PHOTO_DB):
    with open(USER_PHOTO_DB, 'r') as f:
        user_photos = json.load(f)
else:
    user_photos = {}

def save_users():
    with open(USER_DB_FILE, 'w') as f:
        json.dump(users, f, indent=4)

def save_user_photos():
    with open(USER_PHOTO_DB, 'w') as f:
        json.dump(user_photos, f, indent=4)

def download_drive_file(file_id, filename):
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    response = requests.get(url)
    if response.status_code == 200:
        local_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        with open(local_path, 'wb') as f:
            f.write(response.content)
        return local_path
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = users.get(username)
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('indexx'))
        else:
            flash('Invalid credentials!', 'error')

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if username in users:
            flash('Username already exists!', 'error')
        elif password != confirm_password:
            flash('Passwords do not match!', 'error')
        else:
            users[username] = {
                'email': email,
                'password': generate_password_hash(password)
            }
            save_users()
            flash('Account created successfully!', 'success')
            return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect('/login')

@app.route('/')
def indexx():
    import time
    start_total = time.time()

    if 'username' not in session:
        flash('Please login first.', 'error')
        return redirect('/login')

    search_query = request.args.get('search', '')
    file_type = request.args.get('file_type', 'all')
    page_token = request.args.get('page_token', None)

    if 'page_history' not in session:
        session['page_history'] = []

    if request.args.get('nav') == 'next':
        if page_token:
            session['page_history'].append(page_token)
    elif request.args.get('nav') == 'back':
        if len(session['page_history']) >= 2:
            session['page_history'].pop()
            page_token = session['page_history'][-1]
        elif session['page_history']:
            session['page_history'] = []
            page_token = None

    query = f"'{FOLDER_ID}' in parents and trashed = false"
    if search_query:
        query += f" and name contains '{search_query}'"
    if file_type == 'images':
        query += " and mimeType contains 'image'"
    elif file_type == 'videos':
        query += " and mimeType contains 'video'"

    try:
        start_drive = time.time()
        results = service.files().list(
            q=query,
            fields="files(id, name, mimeType), nextPageToken",
            pageSize=12,
            pageToken=page_token
        ).execute()
        print("⏱️ Time to fetch file list from Google Drive:", round(time.time() - start_drive, 3), "seconds")
    except Exception as e:
        return f"Error fetching files: {e}"

    items = results.get('files', [])
    next_page_token = results.get('nextPageToken', None)
    prev_page_token = True if session.get('page_history') else None

    media = []
    for item in items:
        file_id = item['id']
        name = item['name']
        mime_type = item.get('mimeType', '')
        local_path = os.path.join(app.config['UPLOAD_FOLDER'], name)
        if not os.path.exists(local_path):
            try:
                start_dl = time.time()
                download_drive_file(file_id, name)
                print(f"📥 Downloaded {name} in", round(time.time() - start_dl, 3), "seconds")
            except:
                continue
        full_url = url_for('static', filename=f'uploads/{name}')
        media.append({
            'name': name,
            'mime_type': mime_type,
            'thumb_url': '',
            'full_url': full_url
        })

    all_photos = []
    for photo_list in user_photos.values():
        for photo in photo_list:
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo)
            if os.path.exists(photo_path):
                all_photos.append(photo)

    user_uploaded = user_photos.get(session['username'], [])

    print("⏲️ Total time to load '/' route:", round(time.time() - start_total, 3), "seconds")

    return render_template('index.html', media=media, search_query=search_query,
                           file_type=file_type, next_page_token=next_page_token,
                           prev_page_token=prev_page_token,
                           photos=all_photos, user_uploaded=user_uploaded)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'username' not in session:
        return 'Unauthorized', 401

    username = session['username']

    uploaded_files = request.files.getlist('file')
    if not uploaded_files or uploaded_files == [None]:
        uploaded_files = request.files.getlist('photos')

    saved_files = []
    for photo in uploaded_files:
        if photo and photo.filename:
            filename = secure_filename(photo.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            photo.save(file_path)
            user_photos.setdefault(username, []).append(filename)
            saved_files.append(filename)

    save_user_photos()

    return {'status': 'success', 'files': saved_files}

@app.route('/delete/<filename>')
def delete_file(filename):
    if 'username' not in session:
        flash('Please login first.', 'error')
        return redirect('/login')

    username = session['username']
    user_files = user_photos.get(username, [])

    if filename in user_files or username in ADMINS:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            os.remove(file_path)
        if filename in user_files:
            user_files.remove(filename)
            user_photos[username] = user_files
        else:
            for user, photos in user_photos.items():
                if filename in photos:
                    photos.remove(filename)
                    user_photos[user] = photos
                    break
        save_user_photos()
        flash('File deleted successfully.', 'success')
    else:
        flash('You do not have permission to delete this file.', 'error')

    return redirect('/')

@app.route('/upload_from_google', methods=['POST'])
def upload_from_google():
    if 'username' not in session:
        flash('Please login first.', 'error')
        return redirect('/login')

    file_id = request.form.get('file_id')
    if not file_id:
        flash('File ID is required.', 'error')
        return redirect('/')

    filename = f"{file_id}.jpg"
    saved_path = download_drive_file(file_id, filename)

    if saved_path:
        username = session['username']
        user_photos.setdefault(username, []).append(filename)
        save_user_photos()
        flash('Photo uploaded from Google Drive successfully.', 'success')
    else:
        flash('Failed to download the file from Google Drive.', 'error')

    return redirect('/')

@app.route('/profile')
def profile():
    if 'username' not in session:
        flash('Please login first.', 'error')
        return redirect('/login')

    username = session['username']
    user_info = users.get(username, {})
    photos = user_photos.get(username, [])

    return render_template('profile.html', user_info=user_info, photos=photos)

@app.route('/admin')
def admin_panel():
    if 'username' not in session or session['username'] not in ADMINS:
        flash('Access denied! Admins only.', 'error')
        return redirect('/login')

    return render_template('admin.html', users=users, user_photos=user_photos)

@app.route('/admin/delete_user/<username_to_delete>')
def admin_delete_user(username_to_delete):
    if 'username' not in session or session['username'] not in ADMINS:
        flash('Access denied! Admins only.', 'error')
        return redirect('/login')

    if username_to_delete in users:
        users.pop(username_to_delete)
        user_photos.pop(username_to_delete, None)
        save_users()
        save_user_photos()
        flash(f'User {username_to_delete} deleted successfully.', 'success')
    else:
        flash('User not found.', 'error')

    return redirect('/admin')

if __name__ == '__main__':
    app.run(debug=True)
