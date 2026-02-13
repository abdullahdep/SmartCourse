# SmartCourse - Installation Guide

## 📋 System Requirements

- **Python:** 3.10 or higher
- **Operating System:** Windows, macOS, or Linux
- **RAM:** 4 GB minimum (8 GB recommended)
- **Disk Space:** 1 GB (for models and database)
- **Internet:** Required for initial setup

## 🔧 Installation Steps

### Step 1: Clone or Extract Project

```bash
# If you have git
git clone <repository-url>
cd SmartCourse

# Or extract from ZIP
unzip SmartCourse_Prototype.zip
cd SmartCourse
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv env
env\Scripts\activate

# macOS/Linux
python3 -m venv env
source env/bin/activate
```

### Step 3: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt
```

### Step 4: Verify Installation

```bash
# Test Python
python --version

# Test Flask
python -c "import flask; print(flask.__version__)"

# Test ML libraries
python -c "import sklearn, torch, spacy; print('All libraries installed!')"
```

## 🚀 Running the Application

### Option 1: Development Server (Recommended)

```bash
# Activate virtual environment first!
# Windows
env\Scripts\activate
# macOS/Linux
source env/bin/activate

# Run Flask app
python app.py

# Open browser
# Visit: http://localhost:5000
```

### Option 2: Production Server

```bash
# Install production server
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📝 Configuration

### Default Settings

The application comes pre-configured with:

- **Port:** 5000
- **Debug Mode:** Enabled (for development)
- **Database:** SQLite (smartcourse.db)
- **Models:** Pre-trained and serialized

### Changing Configuration

Edit `app.py` to modify:

```python
# Debug mode
app.debug = False  # Set to False for production

# Port
if __name__ == '__main__':
    app.run(port=5000)  # Change port here

# Database
DATABASE = 'smartcourse.db'  # Change database path
```

## 🗄️ Database Setup

### Automatic Setup

The database is created automatically on first run:

```bash
python app.py
```

The application will:
1. Create `smartcourse.db` if it doesn't exist
2. Initialize all tables
3. Load initial data

### Manual Database Reset

```bash
# Remove existing database (WARNING: Deletes all data)
rm smartcourse.db

# Let app recreate it on next run
python app.py
```

## 📦 Dependencies Overview

### Core Framework
```
Flask==2.3.0
Werkzeug==2.3.0
```

### Data Science
```
numpy==1.24.0
pandas==1.5.0
scikit-learn==1.2.0
```

### NLP/ML
```
spacy==3.4.0
sentence-transformers==2.2.0
torch==1.13.0
```

### Database
```
SQLite3 (built-in with Python)
```

### Utilities
```
joblib==1.2.0
PyJWT==2.6.0
```

## 🐛 Troubleshooting

### Issue: ModuleNotFoundError

```
Error: No module named 'flask'
Solution: 
  1. Ensure virtual environment is activated
  2. Run: pip install -r requirements.txt
```

### Issue: Port Already in Use

```
Error: Address already in use
Solution:
  1. Change port in app.py
  2. Or kill process on port 5000
  
Windows:
  netstat -ano | findstr :5000
  taskkill /PID <PID> /F

Linux/macOS:
  lsof -i :5000
  kill -9 <PID>
```

### Issue: Database Locked

```
Error: database is locked
Solution:
  1. Close all Flask instances
  2. Delete .db-journal file
  3. Restart application
```

### Issue: Models Not Loading

```
Error: Cannot load sentence transformers
Solution:
  1. Check models/ folder exists
  2. Verify sentence_model/ is present
  3. Run: pip install sentence-transformers
```

### Issue: Port 5000 Not Accessible

```
Error: Connection refused on localhost:5000
Solution:
  1. Check Flask app is running (no errors in terminal)
  2. Try http://127.0.0.1:5000
  3. Check firewall settings
  4. Try different port: app.run(port=8000)
```

## 📊 Performance Optimization

### For Development

```bash
# Run with auto-reload on file changes
python app.py
```

### For Production

```bash
# Install production dependencies
pip install gunicorn gevent

# Run with multiple workers
gunicorn -w 4 -b 0.0.0.0:5000 --worker-class gevent app:app
```

## 🔐 Security Setup

### Change Default Settings

1. **Disable Debug Mode** (production):
   ```python
   app.debug = False
   ```

2. **Change Secret Key**:
   ```python
   app.secret_key = 'your-secure-key-here'  # Use strong random key
   ```

3. **Set JWT Secret**:
   ```python
   JWT_SECRET = 'your-jwt-secret-key'  # Use strong random key
   ```

## 📝 Sample Test Queries

After starting the application, test with:

1. **Login**
   - Username: testuser
   - Password: password123

2. **Test Search Query**
   - "I want to learn Python for data science"
   - "Web development with React and Node.js"
   - "Machine learning and artificial intelligence"

## 🆘 Getting Help

If you encounter issues:

1. Check this guide first
2. Review error messages carefully
3. Check `requirements.txt` version compatibility
4. Contact supervisor:
   - Email: bilal.saleem@vu.edu.pk
   - Skype: bilalsaleem101

## ✅ Verification Checklist

After installation, verify:

```
□ Python 3.10+ installed
□ Virtual environment created and activated
□ All dependencies installed (pip list)
□ Flask app runs without errors
□ Database created (smartcourse.db exists)
□ Models loaded successfully
□ Can access http://localhost:5000
□ Login works with test credentials
□ Recommendation engine responds
□ Dashboard displays history
```

---

**Installation Complete!** 🎉

You're now ready to run SmartCourse. Start the application with:

```bash
python app.py
```

Then open http://localhost:5000 in your browser.
