from flask import Flask, request, jsonify, render_template
from database import init_db, save_history, get_history
from preprocessing import preprocess_text
from tfidf_model import tfidf_recommend
from neural_model import neural_recommend
import pandas as pd

app = Flask(__name__)
init_db()
DATABASE = 'smartcourse.db'  # path to your SQLite DB






# Load dataset
df = pd.read_csv("data/courses_cleaned.csv")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/recommend")
def recommend_page():
    return render_template("recommend.html")

@app.route("/dashboard")
def dashboard_page():
    data = get_history()  # returns list of tuples: (query, model, results, timestamp)
    # Optionally, parse results JSON if you want to display top courses
    history = []
    for row in data:
        history.append({
            "query": row[0],
            "model": row[1],
            "results": json.loads(row[2]),  # convert JSON string back to Python object
            "timestamp": row[3]
        })
    return render_template("dashboard.html", history=history)


@app.route("/about")
def about_page():
    return render_template("about.html")


# ---------------------- API ROUTES ----------------------

@app.route("/api/recommend", methods=["POST"])
def recommend():
    data = request.json
    query = data["query"]
    model_type = data["model"]

    clean_query = preprocess_text(query)

    if model_type == "tfidf":
        results = tfidf_recommend(clean_query, df)
    else:
        results = neural_recommend(clean_query, df)

    save_history(query, model_type, results)

    return jsonify({"results": results})


@app.route("/api/history", methods=["GET"])
def history():
    return jsonify(get_history())


@app.route("/api/save", methods=["POST"])
def save():
    data = request.json
    save_history(data["query"], data["model"], data["results"])
    return jsonify({"status": "saved"})


if __name__ == "__main__":
    app.run(debug=True)
