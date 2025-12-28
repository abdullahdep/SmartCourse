from flask import Flask, request, jsonify, render_template, session, redirect
from database import init_db, save_history, get_history, create_user, verify_user, get_user, verify_admin
from preprocessing import preprocess_text
from tfidf_model import tfidf_recommend
from neural_model import neural_recommend
import pandas as pd
import json
import jwt
from datetime import datetime, timedelta, timezone
from functools import wraps
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'  # Change this to a secure key
init_db()
DATABASE = 'smartcourse.db'  # path to your SQLite DB

# Load dataset
df = pd.read_csv("data/courses_cleaned.csv")

# Function to retrain models when new CSV is uploaded
def retrain_models(df_new):
    """Retrain TF-IDF and Neural models with new data"""
    import joblib
    import numpy as np
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sentence_transformers import SentenceTransformer
    
    try:
        # Retrain TF-IDF
        corpus = df_new['Course Description'].fillna('').tolist()
        vectorizer = TfidfVectorizer(ngram_range=(1,2), max_features=5000)
        tfidf_matrix = vectorizer.fit_transform(corpus)
        
        import os
        os.makedirs("models", exist_ok=True)
        np.savez_compressed("models/tfidf_features.npz", tfidf_matrix.toarray())
        joblib.dump(vectorizer, "models/tfidf_vectorizer.joblib")
        
        # Retrain Neural model embeddings
        model = SentenceTransformer("all-MiniLM-L6-v2")
        embeddings = model.encode(corpus, convert_to_tensor=False)
        np.save("models/course_embeddings.npy", embeddings)
        
        # Reload global df for immediate use
        global df
        df = df_new
        
    except Exception as e:
        print(f"Error retraining models: {str(e)}")
        raise

# Helper function to generate JWT token
def generate_token(user_id):
    from datetime import timezone
    payload = {
        'user_id': user_id,
        'exp': datetime.now(timezone.utc) + timedelta(days=7)
    }
    token = jwt.encode(payload, app.secret_key, algorithm='HS256')
    return token

# Helper function to verify JWT token
def verify_token(token):
    try:
        data = jwt.decode(token, app.secret_key, algorithms=['HS256'])
        return data.get('user_id')
    except:
        return None

# Decorator to check if user is authenticated
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"success": False, "message": "Authentication required"}), 401
        
        # Remove "Bearer " prefix if present
        if token.startswith("Bearer "):
            token = token[7:]
        
        user_id = verify_token(token)
        if not user_id:
            return jsonify({"success": False, "message": "Invalid or expired token"}), 401
        
        return f(user_id, *args, **kwargs)
    return decorated_function

# Helper function to check authentication for page routes
def check_auth_for_pages():
    """Check if user is authenticated for page routes. Redirect to login if not."""
    token = request.args.get('token')
    if not token:
        return redirect('/login')
    
    user_id = verify_token(token)
    if not user_id:
        return redirect('/login')
    
    return user_id

# ---------------------- AUTH ROUTES ----------------------

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/register")
def register_page():
    return render_template("register.html")

@app.route("/api/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    
    if not username or not email or not password:
        return jsonify({"success": False, "message": "Missing required fields"}), 400
    
    if len(password) < 6:
        return jsonify({"success": False, "message": "Password must be at least 6 characters"}), 400
    
    if create_user(username, email, password):
        return jsonify({"success": True, "message": "User registered successfully"})
    else:
        return jsonify({"success": False, "message": "Username or email already exists"}), 400

@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    if not username or not password:
        return jsonify({"success": False, "message": "Missing username or password"}), 400
    
    user = verify_user(username, password)
    if user:
        token = generate_token(user['id'])
        return jsonify({
            "success": True,
            "token": token,
            "user_id": user['id'],
            "username": user['username']
        })
    else:
        return jsonify({"success": False, "message": "Invalid username or password"}), 401

@app.route("/api/logout", methods=["POST"])
def logout():
    # Since we're using JWT, logout is handled on client side by deleting the token
    return jsonify({"success": True, "message": "Logged out successfully"})

# ---------------------- ADMIN ROUTES ----------------------

@app.route("/admin-login")
def admin_login_page():
    return render_template("admin-login.html")

@app.route("/admin-dashboard")
def admin_dashboard_page():
    # Admin dashboard doesn't need token in URL - it checks localStorage in template
    return render_template("admin-dashboard.html")

@app.route("/api/admin-login", methods=["POST"])
def admin_login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    if not username or not password:
        return jsonify({"success": False, "message": "Missing username or password"}), 400
    
    if verify_admin(username, password):
        import hashlib
        import time
        # Generate a simple admin token
        token_data = f"{username}:{int(time.time())}"
        token = hashlib.sha256(token_data.encode()).hexdigest()
        return jsonify({
            "success": True,
            "token": token,
            "admin_name": username
        })
    else:
        return jsonify({"success": False, "message": "Invalid admin credentials"}), 401

@app.route("/api/upload-csv", methods=["POST"])
def upload_csv():
    admin_token = request.headers.get('Authorization')
    if not admin_token or not admin_token.startswith("Bearer "):
        return jsonify({"success": False, "message": "Admin authentication required"}), 401
    
    # Check if file is in request
    if 'file' not in request.files:
        return jsonify({"success": False, "message": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"success": False, "message": "No file selected"}), 400
    
    if not file.filename.endswith('.csv'):
        return jsonify({"success": False, "message": "Only CSV files are allowed"}), 400
    
    try:
        # Read and validate CSV
        df_new = pd.read_csv(file)
        
        # Check required columns
        required_columns = ["University", "Department", "City/Cities", "Course Description", 
                          "shifts", "online", "Admission dates", "Marks required", "Labs Avalible"]
        missing_columns = [col for col in required_columns if col not in df_new.columns]
        if missing_columns:
            return jsonify({
                "success": False, 
                "message": f"CSV missing required columns: {', '.join(missing_columns)}"
            }), 400
        
        # Save the cleaned CSV
        df_new.to_csv("data/courses_cleaned.csv", index=False)
        
        # Retrain models
        retrain_models(df_new)
        
        return jsonify({
            "success": True,
            "message": f"CSV uploaded successfully! {len(df_new)} courses loaded and models retrained."
        })
        
    except pd.errors.ParserError:
        return jsonify({"success": False, "message": "Invalid CSV format"}), 400
    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500

@app.route("/api/current-user", methods=["GET"])
@login_required
def current_user(user_id):
    user = get_user(user_id)
    if user:
        return jsonify({"success": True, "user": user})
    else:
        return jsonify({"success": False, "message": "User not found"}), 404

# ---------------------- PAGE ROUTES ----------------------

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/recommend")
def recommend_page():
    auth_result = check_auth_for_pages()
    if isinstance(auth_result, int):
        # User is authenticated, auth_result is user_id
        return render_template("recommend.html")
    else:
        # Not authenticated, auth_result is a redirect response
        return auth_result

@app.route("/dashboard")
def dashboard_page():
    auth_result = check_auth_for_pages()
    if isinstance(auth_result, int):
        # User is authenticated
        user_id = auth_result
        data = get_history(user_id)  # Get history only for this user
        # Optionally, parse results JSON if you want to display top courses
        history = []
        for row in data:
            history.append({
                "query": row[0],
                "model": row[1],
                "results": json.loads(row[2]),  # convert JSON string back to Python object
                "timestamp": row[3]
            })
        return render_template("dashboard.html", history=history, enumerate=enumerate)
    else:
        # Not authenticated, auth_result is a redirect response
        return auth_result


@app.route("/about")
def about_page():
    return render_template("about.html")


# ---------------------- API ROUTES ----------------------

@app.route("/api/recommend", methods=["POST"])
@login_required
def recommend(user_id):
    data = request.json
    query = data["query"]
    model_type = data["model"]

    clean_query = preprocess_text(query)

    if model_type == "tfidf":
        results = tfidf_recommend(clean_query, df)
    else:
        results = neural_recommend(clean_query, df)

    save_history(user_id, query, model_type, results)

    return jsonify({"results": results})


@app.route("/api/history", methods=["GET"])
@login_required
def history(user_id):
    data = get_history(user_id)
    return jsonify({"success": True, "history": data})


@app.route("/api/save", methods=["POST"])
@login_required
def save(user_id):
    data = request.json
    save_history(user_id, data["query"], data["model"], data["results"])
    return jsonify({"status": "saved"})


if __name__ == "__main__":
    app.run(debug=True)
