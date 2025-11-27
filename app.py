from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from tensorflow.keras.models import load_model
from gradcam import generate_gradcam_heatmap
from authlib.integrations.flask_client import OAuth
from werkzeug.security import generate_password_hash, check_password_hash
import cv2
import numpy as np
from PIL import Image
import os
from datetime import datetime
import sqlite3
from functools import wraps
from dotenv import load_dotenv


load_dotenv()  # Loads the variables from the .env file

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')  # Change this!
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# OAuth setup for Google
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id= os.getenv('GOOGLE_CLIENT_ID'),  # Replace with your Google Client ID
    client_secret= os.getenv('GOOGLE_CLIENT_SECRET'),  # Replace with your Google Client Secret
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

# Load models once at startup
MODELS = {
    "resnet": load_model("models/pneumonia_resnet50_0.80(21Nov25).keras"),
    "densenet": load_model("models/pneumonia_densenet121_0.91(21Nov25).keras"),
    "vgg": load_model("models/pneumonia_vgg16_0.96(21Nov25).keras")
}

IMG_SIZE = (224, 224)

# Database setup
def init_db():
    conn = sqlite3.connect('pneumonia_detection.db')
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT,
        name TEXT,
        google_id TEXT UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # History table
    c.execute('''CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        image_filename TEXT NOT NULL,
        heatmap_filename TEXT NOT NULL,
        model_used TEXT NOT NULL,
        prediction TEXT NOT NULL,
        confidence REAL NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )''')
    
    conn.commit()
    conn.close()

init_db()

# User class
class User(UserMixin):
    def __init__(self, id, email, name):
        self.id = id
        self.email = email
        self.name = name

@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect('pneumonia_detection.db')
    c = conn.cursor()
    c.execute('SELECT id, email, name FROM users WHERE id = ?', (user_id,))
    user = c.fetchone()
    conn.close()
    if user:
        return User(user[0], user[1], user[2])
    return None

# Optional login decorator (allows guests)
def optional_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        return f(*args, **kwargs)
    return decorated_function

def process_image(image_path):
    img = Image.open(image_path).convert("RGB")
    img = img.resize(IMG_SIZE)
    img = np.array(img) / 255.0
    return np.expand_dims(img, axis=0)

@app.route("/")
@optional_login
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    return render_template("login.html")

@app.route("/register")
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    return render_template("register.html")

@app.route("/auth/google")
def google_login():
    redirect_uri = url_for('google_callback', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route("/auth/google/callback")
def google_callback():
    token = google.authorize_access_token()
    user_info = token.get('userinfo')
    
    if user_info:
        conn = sqlite3.connect('pneumonia_detection.db')
        c = conn.cursor()
        
        # Check if user exists
        c.execute('SELECT id, email, name FROM users WHERE google_id = ?', (user_info['sub'],))
        user = c.fetchone()
        
        if not user:
            # Create new user
            c.execute('INSERT INTO users (email, name, google_id) VALUES (?, ?, ?)',
                     (user_info['email'], user_info.get('name', ''), user_info['sub']))
            conn.commit()
            user_id = c.lastrowid
            user = (user_id, user_info['email'], user_info.get('name', ''))
        
        conn.close()
        
        user_obj = User(user[0], user[1], user[2])
        login_user(user_obj)
        flash('Successfully logged in with Google!', 'success')
        return redirect(url_for('index'))
    
    flash('Failed to log in with Google', 'error')
    return redirect(url_for('login'))

@app.route("/auth/register", methods=["POST"])
def register_user():
    email = request.form.get('email')
    password = request.form.get('password')
    name = request.form.get('name')
    
    if not email or not password or not name:
        flash('All fields are required', 'error')
        return redirect(url_for('register'))
    
    conn = sqlite3.connect('pneumonia_detection.db')
    c = conn.cursor()
    
    # Check if user exists
    c.execute('SELECT id FROM users WHERE email = ?', (email,))
    if c.fetchone():
        conn.close()
        flash('Email already registered', 'error')
        return redirect(url_for('register'))
    
    # Create user
    password_hash = generate_password_hash(password)
    c.execute('INSERT INTO users (email, password_hash, name) VALUES (?, ?, ?)',
             (email, password_hash, name))
    conn.commit()
    user_id = c.lastrowid
    conn.close()
    
    user_obj = User(user_id, email, name)
    login_user(user_obj)
    flash('Registration successful!', 'success')
    return redirect(url_for('index'))

@app.route("/auth/login", methods=["POST"])
def login_user_route():
    email = request.form.get('email')
    password = request.form.get('password')
    
    if not email or not password:
        flash('Email and password are required', 'error')
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('pneumonia_detection.db')
    c = conn.cursor()
    c.execute('SELECT id, email, name, password_hash FROM users WHERE email = ?', (email,))
    user = c.fetchone()
    conn.close()
    
    if user and check_password_hash(user[3], password):
        user_obj = User(user[0], user[1], user[2])
        login_user(user_obj)
        flash('Successfully logged in!', 'success')
        return redirect(url_for('index'))
    
    flash('Invalid email or password', 'error')
    return redirect(url_for('login'))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Successfully logged out', 'success')
    return redirect(url_for('index'))

@app.route("/predict", methods=["POST"])
@optional_login
def predict():
    if "image" not in request.files:
        return "No image uploaded", 400

    image = request.files["image"]
    model_name = request.form["model_name"]
    
    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{image.filename}"
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(image_path)

    img_array = process_image(image_path)

    model = MODELS[model_name]
    prob = float(model.predict(img_array)[0][0])

    label = "PNEUMONIA" if prob > 0.5 else "NORMAL"
    confidence = prob * 100 if prob > 0.5 else (1 - prob) * 100

    # Generate Grad-CAM heatmap
    heatmap = generate_gradcam_heatmap(model, img_array)

    # Load original image and preserve aspect ratio
    original = cv2.imread(image_path)
    original = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
    
    # Get original dimensions
    orig_h, orig_w = original.shape[:2]
    
    # Resize heatmap to match original dimensions
    heatmap_resized = cv2.resize(heatmap, (orig_w, orig_h))
    heatmap_resized = np.uint8(255 * heatmap_resized)

    # Apply colormap
    heatmap_colored = cv2.applyColorMap(heatmap_resized, cv2.COLORMAP_JET)

    # Overlay heatmap on the original image
    overlay = cv2.addWeighted(original, 0.6, heatmap_colored, 0.4, 0)

    # Save output
    heatmap_filename = f"gradcam_{filename}"
    heatmap_path = os.path.join(app.config['UPLOAD_FOLDER'], heatmap_filename)
    cv2.imwrite(heatmap_path, cv2.cvtColor(overlay, cv2.COLOR_RGB2BGR))
    
    # Save to history if user is logged in
    if current_user.is_authenticated:
        conn = sqlite3.connect('pneumonia_detection.db')
        c = conn.cursor()
        c.execute('''INSERT INTO history 
                    (user_id, image_filename, heatmap_filename, model_used, prediction, confidence)
                    VALUES (?, ?, ?, ?, ?, ?)''',
                 (current_user.id, filename, heatmap_filename, model_name.upper(), label, confidence))
        conn.commit()
        conn.close()

    return render_template(
        "index.html",
        prediction=label,
        confidence=round(confidence, 2),
        model_used=model_name.upper(),
        preview_image=f"uploads/{filename}",
        heatmap_image=f"uploads/{heatmap_filename}"
    )

@app.route("/history")
@login_required
def history():
    conn = sqlite3.connect('pneumonia_detection.db')
    c = conn.cursor()
    c.execute('''SELECT image_filename, heatmap_filename, model_used, prediction, 
                        confidence, created_at 
                 FROM history 
                 WHERE user_id = ? 
                 ORDER BY created_at DESC''', (current_user.id,))
    records = c.fetchall()
    conn.close()
    
    history_data = []
    for record in records:
        history_data.append({
            'image': f"uploads/{record[0]}",
            'heatmap': f"uploads/{record[1]}",
            'model': record[2],
            'prediction': record[3],
            'confidence': record[4],
            'date': record[5]
        })
    
    return render_template("history.html", history=history_data)

@app.route("/delete-history/<int:record_id>", methods=["POST"])
@login_required
def delete_history(record_id):
    conn = sqlite3.connect('pneumonia_detection.db')
    c = conn.cursor()
    
    # Get filenames before deleting
    c.execute('SELECT image_filename, heatmap_filename FROM history WHERE id = ? AND user_id = ?',
             (record_id, current_user.id))
    record = c.fetchone()
    
    if record:
        # Delete files
        try:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], record[0]))
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], record[1]))
        except:
            pass
        
        # Delete from database
        c.execute('DELETE FROM history WHERE id = ? AND user_id = ?', (record_id, current_user.id))
        conn.commit()
        flash('Record deleted successfully', 'success')
    
    conn.close()
    return redirect(url_for('history'))

if __name__ == "__main__":
    app.run(debug=True)