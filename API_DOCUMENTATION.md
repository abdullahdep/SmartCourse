# SmartCourse - API Documentation

## 📚 Table of Contents
1. [Authentication](#authentication)
2. [Recommendations](#recommendations)
3. [History & Favorites](#history--favorites)
4. [User Management](#user-management)
5. [Error Handling](#error-handling)

---

## Authentication

### POST /api/register
Register a new user account.

**Request:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Response (Success - 200):**
```json
{
  "success": true,
  "message": "User registered successfully",
  "user_id": 1,
  "username": "john_doe"
}
```

**Response (Error - 400):**
```json
{
  "success": false,
  "message": "Username already exists"
}
```

**Required Fields:**
- `username` (string, 3-20 characters)
- `email` (string, valid email format)
- `password` (string, minimum 6 characters)

---

### POST /api/login
Authenticate user and receive JWT token.

**Request:**
```json
{
  "username": "john_doe",
  "password": "securepassword123"
}
```

**Response (Success - 200):**
```json
{
  "success": true,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user_id": 1,
  "username": "john_doe"
}
```

**Response (Error - 401):**
```json
{
  "success": false,
  "message": "Invalid credentials"
}
```

**How to Use Token:**
Include in all authenticated requests as Bearer token:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

### POST /api/logout
Invalidate current session.

**Request:**
```
POST /api/logout
Authorization: Bearer <token>
```

**Response (Success - 200):**
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

---

## Recommendations

### POST /api/recommend
Get course recommendations based on natural language query.

**Request:**
```json
{
  "query": "I want to learn Python for data science",
  "model": "neural"
}
```

**Request Parameters:**
- `query` (string, required) - Natural language description of learning goal
- `model` (string, optional) - "tfidf" or "neural" (default: "neural")

**Response (Success - 200):**
```json
{
  "success": true,
  "query": "I want to learn Python for data science",
  "selected_model": "neural",
  "tfidf": [
    {
      "title": "Python Data Science Course",
      "department": "Computer Science",
      "city": "New York",
      "description": "Learn Python for data analysis and visualization",
      "score": 92,
      "id": 145
    },
    ...9 more results
  ],
  "neural": [
    {
      "title": "Data Science with Python",
      "department": "Data Science",
      "city": "San Francisco",
      "description": "Comprehensive data science using Python",
      "score": 88,
      "id": 203
    },
    ...9 more results
  ],
  "comparison": {
    "tfidf_first": true,
    "top_3_overlap": 2
  }
}
```

**Model Differences:**

| Aspect | TF-IDF | Neural |
|--------|--------|--------|
| Best for | Keyword-based queries | Semantic/conceptual queries |
| Speed | Fast (< 100ms) | Medium (200-500ms) |
| Accuracy | Good for technical terms | Better for intent-based searches |

**Example Queries:**

```bash
# Keyword-based (TF-IDF excels)
"Python Flask REST API development"

# Semantic (Neural excels)
"I want to build web applications using modern JavaScript"
```

---

## History & Favorites

### GET /api/history
Retrieve user's search history.

**Request:**
```
GET /api/history
Authorization: Bearer <token>
```

**Response (Success - 200):**
```json
{
  "success": true,
  "history": [
    {
      "id": 1,
      "query": "I want to learn Python",
      "model": "neural",
      "results": {
        "tfidf": [...],
        "neural": [...]
      },
      "timestamp": "2026-02-13T10:30:45"
    },
    {
      "id": 2,
      "query": "Web development with React",
      "model": "tfidf",
      "results": {...},
      "timestamp": "2026-02-13T09:15:22"
    }
  ],
  "total_searches": 2
}
```

**Pagination:**
```
GET /api/history?page=1&limit=10
```

---

### GET /api/favorites
Get user's saved favorite courses.

**Request:**
```
GET /api/favorites
Authorization: Bearer <token>
```

**Response (Success - 200):**
```json
{
  "success": true,
  "favorites": [
    {
      "id": 145,
      "title": "Python Data Science Course",
      "department": "Computer Science",
      "city": "New York",
      "description": "Learn Python for data analysis",
      "saved_at": "2026-02-13T10:30:45"
    },
    {
      "id": 203,
      "title": "Advanced Machine Learning",
      "department": "Data Science",
      "city": "Boston",
      "description": "Deep dive into ML algorithms",
      "saved_at": "2026-02-13T09:15:22"
    }
  ],
  "total_favorites": 2
}
```

---

### POST /api/favorite
Save a course to favorites.

**Request:**
```json
{
  "course_id": 145
}
```

**Response (Success - 200):**
```json
{
  "success": true,
  "message": "Course added to favorites",
  "course_id": 145
}
```

**Response (Error - 400):**
```json
{
  "success": false,
  "message": "Course already in favorites"
}
```

---

### POST /api/unfavorite
Remove a course from favorites.

**Request:**
```json
{
  "course_id": 145
}
```

**Response (Success - 200):**
```json
{
  "success": true,
  "message": "Course removed from favorites",
  "course_id": 145
}
```

---

## User Management

### GET /api/profile
Get current user profile.

**Request:**
```
GET /api/profile
Authorization: Bearer <token>
```

**Response (Success - 200):**
```json
{
  "success": true,
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "created_at": "2026-02-01T12:00:00",
    "total_searches": 5,
    "total_favorites": 3
  }
}
```

---

### DELETE /api/history/{id}
Delete a specific search from history.

**Request:**
```
DELETE /api/history/1
Authorization: Bearer <token>
```

**Response (Success - 200):**
```json
{
  "success": true,
  "message": "History entry deleted",
  "id": 1
}
```

---

## Admin Endpoints

### POST /api/admin-login
Admin authentication.

**Request:**
```json
{
  "username": "admin",
  "password": "admin_password"
}
```

**Response (Success - 200):**
```json
{
  "success": true,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "admin_name": "Administrator"
}
```

---

### POST /api/upload-csv
Upload new course dataset (admin only).

**Request:**
```
POST /api/upload-csv
Authorization: Bearer <admin_token>
Content-Type: multipart/form-data

File: courses.csv
```

**Response (Success - 200):**
```json
{
  "success": true,
  "message": "Dataset uploaded and models trained",
  "courses_added": 450,
  "training_time": "45 seconds"
}
```

---

## Error Handling

### Common Error Codes

| Status | Error | Solution |
|--------|-------|----------|
| 400 | Bad Request | Check request format |
| 401 | Unauthorized | Provide valid JWT token |
| 404 | Not Found | Resource doesn't exist |
| 500 | Server Error | Contact support |

### Error Response Format

```json
{
  "success": false,
  "error": "error_code",
  "message": "Human readable error message",
  "timestamp": "2026-02-13T10:30:45"
}
```

### Example Error Responses

**Missing Authorization:**
```json
{
  "success": false,
  "message": "Authorization header missing"
}
```

**Invalid Token:**
```json
{
  "success": false,
  "message": "Invalid or expired token"
}
```

**Course Not Found:**
```json
{
  "success": false,
  "message": "Course with id 9999 not found"
}
```

---

## Rate Limiting

Current rate limits:
- **Recommendations:** 30 requests per minute per user
- **History:** 60 requests per minute per user
- **Other endpoints:** 100 requests per minute per user

**Rate Limit Response (429):**
```json
{
  "success": false,
  "message": "Rate limit exceeded. Try again after 60 seconds"
}
```

---

## Testing the API

### Using cURL

```bash
# Register
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@example.com","password":"pass123"}'

# Login
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"pass123"}'

# Get Recommendations
curl -X POST http://localhost:5000/api/recommend \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"query":"Python for data science","model":"neural"}'

# Get History
curl http://localhost:5000/api/history \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Using Postman

1. Import API collection
2. Set environment variables:
   - `base_url`: http://localhost:5000
   - `token`: Your JWT token
3. Run requests from collection

---

## WebSocket Events (Future Enhancement)

Coming in v2.0:
- Real-time recommendation updates
- Live search suggestions
- Collaborative filtering

---

**Last Updated:** February 13, 2026
**API Version:** 1.0
**Maintainer:** Muhammad Bilal (bilal.saleem@vu.edu.pk)
