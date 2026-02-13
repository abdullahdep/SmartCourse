# SmartCourse - Technical Architecture

## System Design Document

**Version:** 1.0  
**Last Updated:** February 13, 2026  
**Audience:** Developers, Technical Reviewers, System Architects

---

## 📋 Table of Contents

1. [System Architecture](#system-architecture)
2. [Data Flow](#data-flow)
3. [Component Details](#component-details)
4. [Database Schema](#database-schema)
5. [API Architecture](#api-architecture)
6. [Machine Learning Pipeline](#machine-learning-pipeline)
7. [Security Architecture](#security-architecture)
8. [Deployment Architecture](#deployment-architecture)
9. [Performance Considerations](#performance-considerations)

---

## 🏗️ System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Client Layer                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │   Browser    │  │   Mobile     │  │   CLI/API    │           │
│  │   (HTML/CSS) │  │   (Future)   │  │   Clients    │           │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘           │
│         │                 │                 │                    │
│         └─────────────────┼─────────────────┘                    │
│                           │                                      │
│                  HTTP/REST over TLS                              │
│                           │                                      │
└───────────────────────────┼──────────────────────────────────────┘
                            │
┌───────────────────────────┼──────────────────────────────────────┐
│                    API Gateway Layer                             │
│                  (Flask Application)                             │
│  ┌──────────────────────────────────────────────┐               │
│  │        Route Handlers & Request Processing   │               │
│  │  ┌────────────┐  ┌────────────┐  ┌────────┐ │               │
│  │  │ /api/auth  │  │ /api/rec   │  │ /api/  │ │               │
│  │  │            │  │ ommend     │  │ user   │ │               │
│  │  └────────────┘  └────────────┘  └────────┘ │               │
│  └─────────┬──────────────┬──────────────┬──────┘               │
│            │              │              │                       │
└────────────┼──────────────┼──────────────┼───────────────────────┘
             │              │              │
             │              │              │
      ┌──────┴──────┐  ┌────┴─────┐  ┌────┴─────┐
      │             │  │          │  │          │
      │         ┌───┴──┴──┐  ┌────┴──┴──┐       │
      │         │         │  │          │       │
┌─────▼──┐  ┌──▼──┐  ┌───▼──┴───┐   ┌──▼─┐  ┌──▼────┐
│Business│  │Data │  │NLP/ML    │   │Auth│  │Cache  │
│Logic   │  │Access │ │Pipeline  │   │Mgmt│  │Layer  │
│Layer   │  │Layer  │  │           │   │    │  │      │
└─────┬──┘  └──┬───┘  └─────┬──────┘   └──┬─┘  └──┬───┘
      │        │            │             │      │
      └────────┴────────────┼─────────────┴──────┘
                            │
      ┌─────────────────────┴──────────────────────┐
      │      Database & Storage Layer              │
      │  ┌──────────────┐  ┌──────────────┐        │
      │  │   SQLite DB  │  │  File System │        │
      │  │              │  │  (Models,    │        │
      │  │ - Users      │  │  Embeddings) │        │
      │  │ - Courses    │  │              │        │
      │  │ - History    │  │              │        │
      │  │ - Favorites  │  │              │        │
      │  └──────────────┘  └──────────────┘        │
      │                                            │
      └────────────────────────────────────────────┘
```

### Layered Architecture Pattern

**4-Tier Layered Architecture:**

```
┌──────────────────────────────┐
│   Presentation Layer         │  (Templates: HTML, CSS, JS)
│   - User Interface           │  - Responsive design
│   - Request Handling         │  - User interaction
└──────────────┬───────────────┘
               │
┌──────────────▼───────────────┐
│   Application/API Layer      │  (Flask endpoints)
│   - Route Handlers           │  - Business logic
│   - Request Validation       │  - Response formatting
└──────────────┬───────────────┘
               │
┌──────────────▼───────────────┐
│   Business Logic Layer       │  (ML models)
│   - Recommendations          │  - TF-IDF matching
│   - NLP Processing           │  - Neural scoring
│   - Data Validation          │  - Preprocessing
└──────────────┬───────────────┘
               │
┌──────────────▼───────────────┐
│   Data Access Layer          │  (Database queries)
│   - CRUD Operations          │  - SQLite interface
│   - Query Optimization       │  - Data persistence
└──────────────────────────────┘
```

---

## 📊 Data Flow

### 1. Course Recommendation Flow

```
User Input
    ↓
[HTML Form]
    ↓
[JavaScript Handler] (script.js)
    ↓ (AJAX POST request)
┌─────────────────────────────┐
│ POST /api/recommend         │
│ Payload: {query, model}     │
└────────────┬────────────────┘
             ↓
┌─────────────────────────────┐
│ Flask Route Handler         │ (app.py)
│ - Extract query & model     │
│ - Validate JWT token        │
│ - Verify user exists        │
└────────────┬────────────────┘
             ↓
┌─────────────────────────────┐
│ Query Preprocessing         │ (preprocessing.py)
│ - Tokenization              │
│ - Lemmatization             │
│ - Stopword removal          │
│ - Text normalization        │
└────────────┬────────────────┘
             ↓
         ┌───┴────┐
         │ Model? │
         └───┬────┘
         ╱       ╲
    TF-IDF     Neural
        │         │
    ┌───▼──┐  ┌───▼──────┐
    │ TF-  │  │ Sentence  │
    │ IDF  │  │ Transform │
    │Model │  │ Model     │
    └───┬──┘  └───┬───────┘
        │         │
    ┌───▼─────────▼──┐
    │ Load Features  │
    │ from Disk      │
    │ (joblib/npy)   │
    └───┬────────────┘
        │
    ┌───▼──────────────────────┐
    │ Compute Similarity       │
    │ - Cosine similarity      │
    │ - Euclidean distance     │
    │ - Score normalization    │
    └───┬──────────────────────┘
        │
    ┌───▼─────────────────────┐
    │ Rank Results            │
    │ - Top 10 courses        │
    │ - Calculate relevance   │
    │ - Sort by score         │
    └───┬─────────────────────┘
        │
    ┌───▼──────────────┐
    │ Fetch Details    │
    │ from Database    │
    │ (course info)    │
    └───┬──────────────┘
        │
    ┌───▼────────────────────┐
    │ Save to History        │
    │ - Record query         │
    │ - Store timestamp      │
    │ - Log results          │
    └───┬────────────────────┘
        │
    ┌───▼──────────────────┐
    │ Format Response      │
    │ - JSON payload       │
    │ - Include metadata   │
    │ - Add timestamps     │
    └───┬──────────────────┘
        │
    ┌───▼─────────────────┐
    │ HTTP Response       │
    │ Status: 200         │
    │ Body: JSON results  │
    └───┬─────────────────┘
        │
        ↓ (JavaScript handler)
    Display Results
        ↓
    Update DOM
        ↓
    Show Course Cards
        ↓
    User Views Results
```

### 2. User Authentication Flow

```
Registration Request
    ↓
[Register Form]
    ↓
[JavaScript Handler]
    ↓
┌──────────────────────┐
│ POST /api/register   │
│ Payload: {user, pwd} │
└──────────┬───────────┘
           ↓
┌──────────────────────────┐
│ Input Validation         │
│ - Email format           │
│ - Password strength      │
│ - Duplicate check        │
└──────────┬───────────────┘
           ↓
┌──────────────────────────┐
│ Hash Password            │ (Werkzeug)
│ - Generate salt          │
│ - PBKDF2 hashing         │
└──────────┬───────────────┘
           ↓
┌──────────────────────────┐
│ Store in Database        │ (SQLite)
│ - users table            │
│ - Add timestamp          │
└──────────┬───────────────┘
           ↓
┌──────────────────────────┐
│ Return Success Response  │
│ Status: 201              │
└──────────┬───────────────┘
           ↓
       Display Success

Login Request
    ↓
[Login Form]
    ↓
[JavaScript Handler]
    ↓
┌──────────────────────┐
│ POST /api/login      │
│ Payload: {user, pwd} │
└──────────┬───────────┘
           ↓
┌──────────────────────────┐
│ Query Database           │
│ - Find user by email     │
└──────────┬───────────────┘
           ↓
┌──────────────────────────┐
│ Verify Password          │
│ - Werkzeug check_pw      │
│ - Compare hashes         │
└──────────┬───────────────┘
           ↓
┌──────────────────────────┐
│ Generate JWT Token       │ (PyJWT)
│ - User ID in payload     │
│ - 24-hour expiration     │
│ - Secret key signing     │
└──────────┬───────────────┘
           ↓
┌──────────────────────────┐
│ Return Token             │
│ Status: 200              │
│ Body: {token}            │
└──────────┬───────────────┘
           ↓
    Store Token (localStorage)
           ↓
    Update UI (logged in state)
```

### 3. Dashboard Data Flow

```
User Requests Dashboard
    ↓
[Check Auth Token]
    ↓
┌──────────────────────────┐
│ Verify JWT Token         │
│ - Check expiration       │
│ - Validate signature     │
│ - Extract user ID        │
└──────────┬───────────────┘
           ↓
┌──────────────────────────┐
│ GET /api/history         │
│ (3 parallel requests)    │
└──────────┬───────────────┘
    ┌──────┼──────┐
    │      │      │
┌───▼──┐┌───▼──┐┌───▼──┐
│GET   ││GET   ││GET   │
│/api/ ││/api/ ││admin?│
│favor││history
│ites ││      ││      │
└───┬──┘└───┬──┘└───┬──┘
    │      │      │
    └──────┼──────┘
           ↓
┌──────────────────────────┐
│ Fetch from Database      │
│ - User's searches        │
│ - User's favorites       │
│ - User's admin status    │
└──────────┬───────────────┘
           ↓
┌──────────────────────────┐
│ Format & Combine Data    │
│ - Sort by timestamp      │
│ - Add metadata           │
│ - Prepare JSON           │
└──────────┬───────────────┘
           ↓
┌──────────────────────────┐
│ Send Response            │
└──────────┬───────────────┘
           ↓
[JavaScript Merge Results]
           ↓
[Render Dashboard Tabs]
           ↓
    Display to User
```

---

## 🔧 Component Details

### Frontend Components

**1. Application Structure (index.html)**
```
Header (Navbar)
├── Logo
├── Navigation Links
│  ├── Home
│  ├── Recommendations
│  ├── About
│  └── Account (if logged in)
└── Auth Buttons (Login/Register)

Main Content
├── Hero Section
│  ├── Title
│  ├── Subtitle
│  └── CTA Button
├── Features Grid
│  ├── Feature Card 1 (Dual Models)
│  ├── Feature Card 2 (Smart Search)
│  └── Feature Card 3 (Dashboard)
└── Call-to-Action Section

Footer
├── Links
├── Copyright
└── Contact Info
```

**2. Recommendation Interface (recommend.html)**
```
Search Section
├── Input Field (Query)
├── Model Selector (TF-IDF / Neural)
├── Submit Button
└── Clear Button

Results Section (Tab: TF-IDF)
├── Loading Spinner
├── Result Cards (10 courses)
│  ├── Rank Badge
│  ├── Course Title
│  ├── University
│  ├── Relevance Score (%)
│  ├── City/Country
│  └── Actions (Favorite, Details)
└── Pagination Controls

Results Section (Tab: Neural)
├── Loading Spinner
├── Result Cards (10 courses)
├── Relevance Scores
└── Comparison Option

Comparison Section (Tab: Comparison)
├── Side-by-side Model Results
├── Difference Analysis
└── Model Performance Metrics
```

**3. Dashboard (dashboard.html)**
```
User Info Section
├── Username
├── Email
├── Member Since Date
└── Logout Button

Tabs Section
├── History Tab
│  ├── Search Query
│  ├── Date/Time
│  ├── Model Used
│  ├── Top Result
│  └── Delete Option
├── Favorites Tab
│  ├── Course Cards
│  ├── Remove Button
│  └── Edit Notes
└── Profile Tab
   ├── Account Settings
   └── Preferences
```

### Backend Components

**1. Flask Application (app.py)**
```python
Flask App
├── Route Handlers
│  ├── GET /                  → index.html
│  ├── GET /login            → login.html
│  ├── GET /register         → register.html
│  ├── GET /recommend        → recommend.html
│  ├── GET /dashboard        → dashboard.html
│  ├── GET /admin-login      → admin-login.html
│  ├── POST /api/register    → User registration
│  ├── POST /api/login       → JWT token generation
│  ├── POST /api/recommend   → Get recommendations
│  ├── GET /api/history      → Get search history
│  ├── POST /api/favorite    → Save favorite
│  ├── POST /api/unfavorite  → Remove favorite
│  ├── GET /api/favorites    → List favorites
│  └── More endpoints...
├── Middleware
│  ├── CORS configuration
│  ├── JSON request parsing
│  └── Error handling
└── Error Handlers
   ├── 400 Bad Request
   ├── 401 Unauthorized
   ├── 404 Not Found
   └── 500 Server Error
```

**2. Database Module (database.py)**
```python
Database Interface
├── Initialization Functions
│  ├── init_db()           → Create tables if needed
│  └── seed_data()         → Load initial courses
├── User Management
│  ├── create_user()       → Register new user
│  ├── get_user()          → Fetch user by ID
│  └── verify_password()   → Check credentials
├── Course Management
│  ├── get_course()        → Fetch course details
│  ├── search_courses()    → Query course database
│  └── get_all_courses()   → Bulk retrieve
├── History Management
│  ├── add_to_history()    → Record search
│  └── get_history()       → Retrieve searches
├── Favorites Management
│  ├── add_favorite()      → Save favorite
│  ├── remove_favorite()   → Delete favorite
│  └── get_favorites()     → List saved courses
└── Admin Functions
   ├── get_all_users()     → Admin user list
   └── update_courses()    → Bulk course update
```

**3. Preprocessing Pipeline (preprocessing.py)**
```python
Text Processing
├── tokenize()          → Split into words
├── remove_stopwords()  → Remove common words
├── lemmatize()         → Normalize to base form
├── clean_text()        → Remove special chars
└── preprocess_query()  → Full pipeline
```

**4. TF-IDF Model (tfidf_model.py)**
```python
TF-IDF Recommendation
├── load_vectorizer()   → Load from joblib
├── load_features()     → Load pre-computed
├── vectorize_query()   → Convert query
├── compute_similarity()→ Cosine similarity
└── get_recommendations()→ Top 10 courses
```

**5. Neural Model (neural_model.py)**
```python
Neural Recommendation
├── load_encoder()      → Load sentence model
├── load_embeddings()   → Load course vectors
├── encode_query()      → Generate embedding
├── compute_similarity()→ Cosine similarity
└── get_recommendations()→ Top 10 courses
```

---

## 💾 Database Schema

### SQLite Database (smartcourse.db)

```sql
-- Users Table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_admin BOOLEAN DEFAULT FALSE
);

-- Courses Table
CREATE TABLE courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    code VARCHAR(50),
    university VARCHAR(255),
    department VARCHAR(255),
    city VARCHAR(100),
    country VARCHAR(100),
    description TEXT,
    difficulty VARCHAR(50),
    duration VARCHAR(100),
    rating FLOAT,
    reviews_count INTEGER,
    prerequisites TEXT,
    enrolment_requirements TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Search History Table
CREATE TABLE search_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    query VARCHAR(500) NOT NULL,
    model VARCHAR(50) NOT NULL,  -- 'tfidf' or 'neural'
    top_result_id INTEGER,
    results_count INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (top_result_id) REFERENCES courses(id)
);

-- Favorites Table
CREATE TABLE favorites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    notes TEXT,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, course_id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (course_id) REFERENCES courses(id)
);

-- Indices for Performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_courses_title ON courses(title);
CREATE INDEX idx_history_user_id ON search_history(user_id);
CREATE INDEX idx_favorites_user_id ON favorites(user_id);
CREATE INDEX idx_favorites_course_id ON favorites(course_id);
```

### Data Statistics

| Table | Records | Purpose |
|-------|---------|---------|
| users | 50+ | User accounts |
| courses | 8,500+ | Course catalog |
| search_history | 500+ | Query tracking |
| favorites | 200+ | User saved items |

---

## 🔌 API Architecture

### REST API Design

**Base URL:** `http://localhost:5000/api`

### Endpoint Categories

#### 1. Authentication Endpoints

**POST /register**
```
Request:
{
    "email": "user@example.com",
    "password": "SecurePass123!"
}

Response (201):
{
    "message": "User created successfully",
    "user_id": 1
}

Response (400):
{
    "error": "Email already registered"
}
```

**POST /login**
```
Request:
{
    "email": "user@example.com",
    "password": "SecurePass123!"
}

Response (200):
{
    "token": "eyJhbGc...",
    "user_id": 1
}

Response (401):
{
    "error": "Invalid credentials"
}
```

#### 2. Recommendation Endpoints

**POST /recommend**
```
Request:
{
    "query": "I want to learn Python programming",
    "model": "neural"  // or "tfidf"
}

Headers:
{
    "Authorization": "Bearer {token}"
}

Response (200):
{
    "results": [
        {
            "rank": 1,
            "course_id": 123,
            "title": "Python for Beginners",
            "university": "MIT",
            "relevance_score": 0.92,
            "city": "Cambridge",
            "country": "USA"
        },
        ...
    ],
    "query": "I want to learn Python programming",
    "model": "neural",
    "timestamp": "2024-02-13T10:30:00Z"
}
```

#### 3. History Endpoints

**GET /history**
```
Headers:
{
    "Authorization": "Bearer {token}"
}

Response (200):
{
    "history": [
        {
            "id": 1,
            "query": "Web Development",
            "model": "tfidf",
            "created_at": "2024-02-13T10:30:00Z",
            "top_result": {
                "id": 456,
                "title": "React Web Development"
            }
        },
        ...
    ]
}
```

#### 4. Favorites Endpoints

**POST /favorite**
```
Request:
{
    "course_id": 123,
    "notes": "Really interested in this"
}

Response (201):
{
    "message": "Added to favorites"
}
```

**GET /favorites**
```
Response (200):
{
    "favorites": [
        {
            "id": 1,
            "course_id": 123,
            "title": "Python for Beginners",
            "notes": "Really interested",
            "added_at": "2024-02-13T10:30:00Z"
        },
        ...
    ]
}
```

### API Security

**Authentication Method:**
```
All protected endpoints require:
Authorization: Bearer <JWT_TOKEN>

JWT Token Structure:
Header: {
    "alg": "HS256",
    "typ": "JWT"
}
Payload: {
    "user_id": 1,
    "iat": 1707835800,
    "exp": 1707922200
}
Signature: HMACSHA256(header + payload, secret_key)
```

**Error Response Format:**
```json
{
    "error": "Error description",
    "status": 400,
    "timestamp": "2024-02-13T10:30:00Z"
}
```

---

## 🤖 Machine Learning Pipeline

### TF-IDF Model Architecture

```
Training Pipeline:
Raw Text → Tokenization → Cleaning → TF-IDF Vectorization → Features

Inference Pipeline:
User Query → Preprocess → Vectorize → Cosine Similarity → Rank

Components:
├── Vectorizer (scikit-learn CountVectorizer + TfidfTransformer)
├── Features (500-dimensional sparse matrix)
├── Query Processing
│  ├── Tokenize
│  ├── Remove stopwords
│  └── Lemmatize
└── Similarity Computation
   ├── Convert query to vector
   ├── Calculate cosine similarity with all courses
   └── Return top 10 by score
```

**Mathematical Foundation:**

$$
\text{TF-IDF}(t, d) = \text{TF}(t, d) \times \text{IDF}(t)
$$

where:
- TF (Term Frequency) = frequency of term t in document d
- IDF (Inverse Document Frequency) = log(N / df) where N = total docs, df = docs with term

**Similarity Metric:**

$$
\text{cosine\_similarity}(a, b) = \frac{a \cdot b}{||a|| \times ||b||}
$$

### Neural Model Architecture

```
Training Pipeline:
Course Text → Sentence Transformer → Dense Vector (384D) → Store Embedding

Inference Pipeline:
User Query → Encode → Vector (384D) → Cosine Similarity → Rank

Components:
├── Pre-trained Model (sentence-transformers)
│  └── "distiluse-base-multilingual-cased-v2"
├── Embeddings (384-dimensional dense vectors)
├── Query Processing
│  ├── Tokenization
│  ├── Subword tokenization (BPE)
│  └── Model encoding
└── Similarity Computation
   ├── Convert query to embedding
   ├── Calculate cosine similarity
   └── Return top 10 by score
```

**Model Details:**

```
Sentence-Transformers Architecture:
Input Text
    ↓
Tokenizer (Wordpiece, max_length=128)
    ↓
DistilBERT Encoder (6 layers, 768 hidden, 12 heads)
    ↓
Mean Pooling (reduce to [CLS])
    ↓
Normalization (L2 norm)
    ↓
384-dimensional Vector Output
```

**Advantages over TF-IDF:**
- Semantic understanding (not just keywords)
- Handles synonyms and paraphrasing
- Better for complex, intent-based queries
- Context-aware representations

### Model Comparison

| Aspect | TF-IDF | Neural |
|--------|--------|--------|
| **Speed** | < 50ms | 200-500ms |
| **Keywords** | Excellent | Good |
| **Semantics** | Poor | Excellent |
| **Synonyms** | None | Handled well |
| **Memory** | 20MB | 400MB |
| **Interpretability** | High | Low |
| **Training Data** | Uses corpus | Pre-trained |

### Training Workflow

```
1. Data Preparation
   └─ Load 8,500 courses
   └─ Extract text fields (title + description)
   └─ Clean and normalize

2. TF-IDF Training
   └─ Build vocabulary (max 5000 features)
   └─ Compute TF-IDF for all courses
   └─ Save vectorizer and features

3. Neural Encoding
   └─ Load pre-trained sentence-transformers
   └─ Encode all course texts
   └─ Save embeddings as numpy array

4. Validation
   └─ Test on sample queries
   └─ Verify both models working
   └─ Check response times

5. Deployment
   └─ Move models to /models directory
   └─ Load at application startup
   └─ Ready for inference
```

---

## 🔐 Security Architecture

### Security Layers

```
Application Security
├── Input Validation
│  ├── Email format validation
│  ├── Password strength checks
│  ├── Query length limits
│  └── SQL injection prevention
├── Authentication
│  ├── Password hashing (PBKDF2)
│  ├── JWT token generation
│  ├── Token validation
│  └── Expiration checking
├── Authorization
│  ├── Token verification on protected routes
│  ├── User ownership validation
│  └── Admin privilege checking
└── Data Protection
   ├── HTTPS ready
   ├── Secure headers
   └── CORS configuration
```

### Password Security

**Hashing Algorithm:**
```python
# Werkzeug uses PBKDF2 with:
- Algorithm: PBKDF2-SHA256
- Iterations: 200,000
- Salt length: 16 bytes
- Output length: 32 bytes

Example:
Original: "SecurePass123!"
Hashed:   "pbkdf2:sha256:260000$..."
```

**Password Requirements:**
- Minimum 8 characters
- Mix of uppercase and lowercase
- At least one number
- Recommended: special characters

### JWT Token Security

**Token Structure:**
```
Header.Payload.Signature

Header: {
    "alg": "HS256",
    "typ": "JWT"
}

Payload: {
    "user_id": 1,
    "email": "user@example.com",
    "iat": 1707835800,        # issued at
    "exp": 1707922200         # expires in 24 hours
}

Signature: HMAC_SHA256(
    base64(header) + "." + base64(payload),
    SECRET_KEY
)
```

**Token Validation:**
1. Check signature with secret key
2. Verify expiration time
3. Extract user_id from payload
4. Verify user exists in database

### SQL Injection Prevention

**Parameterized Queries:**
```python
# ✅ Safe: Uses parameterized query
cursor.execute(
    "SELECT * FROM courses WHERE title LIKE ?",
    (f"%{search_term}%",)
)

# ❌ Unsafe: String concatenation
cursor.execute(f"SELECT * FROM courses WHERE title LIKE '%{search_term}%'")
```

### CORS Configuration

```python
from flask_cors import CORS

CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000"],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

### Security Headers

```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000
```

---

## 🚀 Deployment Architecture

### Development Deployment

```
Development Server:
python app.py

├── Flask Development Server
│  ├── Threaded: True
│  ├── Host: localhost
│  ├── Port: 5000
│  └── Debug: True
├── SQLite Database
│  └── File: smartcourse.db
└── Models
   ├── TF-IDF: /models/tfidf_vectorizer.joblib
   └── Neural: /models/sentence_model/
```

### Production Deployment (Recommended)

```
Web Server (Gunicorn)
    ↓
WSGI Application (Flask)
    ↓
Reverse Proxy (Nginx) [Optional]
    ↓
Static Files (CSS, JS)
    ↓
SQLite Database
    ↓
Pre-trained Models

Command:
gunicorn -w 4 -b 0.0.0.0:5000 app:app

Options:
-w 4            → 4 worker processes
-b 0.0.0.0:5000 → Bind to all interfaces, port 5000
--timeout 60    → 60 second timeout
--access-logfile access.log
--error-logfile error.log
```

### Deployment Checklist

```
Pre-deployment:
[ ] All tests passing
[ ] Environment variables set (.env)
[ ] Database migration completed
[ ] Static files collected
[ ] Models pre-loaded and tested

Deployment:
[ ] Deploy code to server
[ ] Create virtual environment
[ ] Install dependencies
[ ] Run database initialization
[ ] Start application with gunicorn
[ ] Configure reverse proxy (nginx)
[ ] Set up SSL/TLS certificates
[ ] Configure firewall rules

Post-deployment:
[ ] Smoke test all endpoints
[ ] Monitor error logs
[ ] Check performance metrics
[ ] Verify backups working
[ ] Document deployment steps
```

### Scalability Considerations

**Current Limitations:**
- Single machine deployment
- Models loaded in memory
- SQLite (not distributed)
- No caching layer

**Future Improvements:**
1. **Database:** PostgreSQL with connection pooling
2. **Caching:** Redis for frequently accessed data
3. **Models:** Load models on-demand
4. **Queue:** Celery for async tasks
5. **Monitoring:** Prometheus + Grafana
6. **Load Balancing:** Nginx/HAProxy for multiple instances

---

## ⚡ Performance Considerations

### Response Time Targets

```
Homepage:        < 500ms
Login/Register:  < 1 second
Recommendation:  < 2 seconds
    ├─ TF-IDF:   < 200ms
    ├─ Neural:   < 500ms
    └─ Query:    < 300ms
Dashboard:       < 1.5 seconds
API Endpoint:    < 1 second
```

### Optimization Strategies

**1. Database Optimization**
```
Index Strategy:
- Primary keys (automatic)
- user_id in all user-related tables
- course_id in all course-related tables
- Email in users table (for login)
- Query analysis and EXPLAIN plans
```

**2. Model Optimization**
```
TF-IDF:
- Pre-computed features (5000-dimensional)
- Loaded once at startup
- Sparse matrix storage (joblib)

Neural:
- Pre-trained model (no training)
- Embeddings pre-computed and stored
- 384-dimensional vectors (numpy)
```

**3. Caching Strategy**
```
Recommended Cache Points:
- Course list (TTL: 1 hour)
- User profile (TTL: 30 minutes)
- Popular searches (TTL: 1 hour)
- Static assets (HTTP cache headers)
```

**4. Frontend Optimization**
```
- Minified CSS and JavaScript
- Image optimization
- Lazy loading for results
- Pagination (10 results per page)
- Async API calls (no page reload)
```

### Bottleneck Analysis

| Component | Current | Bottleneck | Solution |
|-----------|---------|------------|----------|
| Neural Model | 200-500ms | Model encoding | Pre-encode or cache |
| Database | < 50ms | None | N/A |
| API Route | < 100ms | None | N/A |
| Frontend | < 200ms | JS execution | Optimize JS bundle |

### Monitoring & Metrics

**Key Performance Indicators (KPIs):**
```
- API Response Time (target: < 1s)
- Model Inference Time (target: < 500ms)
- Database Query Time (target: < 50ms)
- Page Load Time (target: < 2s)
- Error Rate (target: < 1%)
- Uptime (target: > 99.5%)
```

**Monitoring Tools (Recommended):**
- Application: Application Performance Monitoring (APM)
- Database: Query logs and slow query analysis
- Frontend: Browser DevTools and Lighthouse
- Infrastructure: Server metrics (CPU, memory, disk)

---

## 📚 Technical Stack Summary

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| **Frontend** | HTML5 | 5.0 | Structure |
| | CSS3 | 3.0 | Styling |
| | JavaScript | ES6+ | Interactivity |
| | Bootstrap | 5.0 | Responsive framework |
| **Backend** | Python | 3.10+ | Runtime |
| | Flask | 2.3.0 | Web framework |
| | SQLite | 3 | Database |
| **ML/NLP** | scikit-learn | 1.2.0 | TF-IDF |
| | sentence-transformers | 2.2.0 | Neural embeddings |
| | spaCy | 3.4.0 | Text processing |
| | numpy | 1.24.0 | Numerical ops |
| | pandas | 1.5.0 | Data processing |
| **Security** | PyJWT | 2.6.0 | JWT tokens |
| | Werkzeug | 2.3.0 | Password hashing |
| **Utilities** | joblib | 1.2.0 | Model serialization |

---

## 🔗 Integration Points

```
Frontend ↔ Backend
- AJAX POST/GET requests
- JSON request/response format
- Authorization header (JWT token)
- CORS headers for cross-origin

Backend ↔ Database
- SQLite3 Python module
- Parameterized queries
- Connection pooling (optional)
- Transaction management

Backend ↔ Models
- Joblib serialization (TF-IDF)
- Numpy arrays (Embeddings)
- In-memory loading at startup
- Deterministic seeding (for consistency)

Models ↔ Data
- Feature vectors from text
- Similarity computations
- Score normalization
- Result ranking
```

---

## 🎯 Conclusion

SmartCourse uses a modern, layered architecture that separates concerns into:

1. **Presentation Layer:** Responsive web interface
2. **API Layer:** RESTful endpoints with JWT auth
3. **Business Logic:** ML models and NLP processing
4. **Data Access:** SQLite queries and file I/O
5. **Storage:** SQLite database and pre-trained models

This design ensures:
- ✅ Scalability for future growth
- ✅ Security with JWT and password hashing
- ✅ Performance with optimized models
- ✅ Maintainability with clear separation of concerns
- ✅ Extensibility for new features

---

**Document Version:** 1.0  
**Last Updated:** February 13, 2026  
**Technical Lead:** Muhammad Bilal (bilal.saleem@vu.edu.pk)

---

For more information, see:
- [README.md](README.md) - Project overview
- [INSTALLATION.md](INSTALLATION.md) - Setup guide
- [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - API reference
- [USER_GUIDE.md](USER_GUIDE.md) - User manual
- [PROTOTYPE_IMPLEMENTATION_GUIDE.md](PROTOTYPE_IMPLEMENTATION_GUIDE.md) - Implementation details
