# SmartCourse Authentication Implementation

## Overview
Complete authentication system has been added to SmartCourse. Users must now register, login, and be authenticated to perform recommendations and view their dashboard.

## What's Been Added

### 1. **Database Updates** (`database.py`)
- **New `users` table** with fields:
  - `id`: User ID
  - `username`: Unique username
  - `email`: Unique email
  - `password`: Hashed password (using `werkzeug.security`)
  - `created_at`: Registration timestamp

- **Updated `history` table** to include:
  - `user_id`: Foreign key linking to users table
  - History is now per-user instead of global

- **New Functions**:
  - `create_user(username, email, password)`: Register new user
  - `verify_user(username, password)`: Check credentials
  - `get_user(user_id)`: Get user info

### 2. **Authentication in Flask** (`app.py`)
- **JWT Token System**:
  - `generate_token(user_id)`: Creates JWT token valid for 7 days
  - `verify_token(token)`: Validates token and extracts user_id
  - `@login_required`: Decorator to protect routes

- **New API Endpoints**:
  - `POST /api/register`: User registration
  - `POST /api/login`: User login (returns JWT token)
  - `POST /api/logout`: User logout
  - `GET /api/current-user`: Get current user info (requires auth)

- **Protected Routes**:
  - `POST /api/recommend`: Now requires authentication
  - `GET /api/history`: Now returns only user's history
  - `POST /api/save`: Now saves to user's history

- **New Pages**:
  - `GET /login`: Login page
  - `GET /register`: Registration page
  - Updated `/dashboard`: Now requires token parameter

### 3. **Templates**

#### `login.html` (New)
- Clean login form
- Username and password fields
- Error message display
- Link to registration page
- Form validation and JWT token storage

#### `register.html` (New)
- User registration form
- Username, email, password, confirm password fields
- Password validation (min 6 characters)
- Confirmation on match
- Link to login page
- Success message on registration

#### `index.html` (Updated)
- Dynamic navbar showing:
  - **If NOT logged in**: Login, Register, About links
  - **If logged in**: Welcome message, Start Recommendation, Dashboard, About, Logout button
- Authentication-aware content:
  - Shows login/register prompt if not authenticated
  - Shows "Get Course Recommendations" button if authenticated
- Client-side authentication check

### 4. **Frontend Scripts** (`script.js`)
- **Authentication Checks**:
  - `checkAuth()`: Checks localStorage for auth_token
  - `checkAuthOnPageLoad()`: Validates user on page load
  - Redirects to login if token is missing/expired

- **Updated Functions**:
  - `checkAuthAndRecommend()`: Requires auth before recommendations
  - `getRecommendations()`: Sends JWT token with API requests
  - `displayResults()`: Handles null/undefined fields gracefully

- **Session Management**:
  - Stores `auth_token`, `user_id`, `username` in localStorage
  - `logout()`: Clears localStorage and redirects home
  - Automatic redirect to login on 401 responses

### 5. **Dependencies** (`requirements.txt`)
Added:
- `PyJWT`: JWT token generation and verification
- `Werkzeug`: Password hashing (for bcrypt-like security)

## How It Works

### Registration Flow
1. User fills registration form
2. Frontend validates passwords match
3. `POST /api/register` creates user (hashed password)
4. Success → redirects to login page

### Login Flow
1. User enters username and password
2. `POST /api/login` verifies credentials
3. Returns JWT token (7-day expiry)
4. Token stored in `localStorage`
5. Redirects to home page

### Making Recommendations
1. User must be logged in (has valid token)
2. `POST /api/recommend` includes `Authorization: Bearer {token}`
3. Server verifies token and extracts `user_id`
4. Results saved to user's history
5. If token invalid/expired → 401 error → redirect to login

### Logout
1. User clicks logout button
2. localStorage cleared
3. JWT token discarded (no backend state needed)
4. Redirects to home page

## Security Features
✅ **Password Hashing**: Uses werkzeug.security (PBKDF2)  
✅ **JWT Tokens**: 7-day expiration  
✅ **Per-User History**: Users only see their own data  
✅ **Protected Routes**: @login_required decorator  
✅ **Token Validation**: Server-side verification  

## Important: Change Secret Key
⚠️ In `app.py` line 14, change:
```python
app.secret_key = 'your-secret-key-change-this'
```
To a strong random key like:
```python
app.secret_key = 'your-unique-secure-key-here-at-least-32-chars'
```

## Testing the System

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Delete Old Database (to reset)
```bash
rm smartcourse.db
```

### 3. Run Flask App
```bash
python app.py
```

### 4. Test Registration
- Go to: http://localhost:5000/register
- Create account with username, email, password

### 5. Test Login
- Go to: http://localhost:5000/login
- Login with credentials

### 6. Test Protected Features
- Click "Start Recommendation" (only available if logged in)
- Get course recommendations
- Visit dashboard to see history

## Database Schema

### users table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
```

### history table (Updated)
```sql
CREATE TABLE history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    query TEXT,
    model TEXT,
    results TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
```

## Files Modified
- ✅ `database.py` - Added user management
- ✅ `app.py` - Added auth routes and protected endpoints
- ✅ `requirements.txt` - Added PyJWT, Werkzeug
- ✅ `templates/index.html` - Updated with auth UI
- ✅ `templates/login.html` - New
- ✅ `templates/register.html` - New
- ✅ `static/script.js` - Added auth logic

## Next Steps (Optional Enhancements)
- Add email verification
- Add password reset functionality
- Add user profile page
- Add profile picture support
- Rate limiting on login attempts
- Two-factor authentication
- Social login (Google, GitHub, etc.)

---

**System is now fully authenticated! All users must register and login to use recommendations.**
