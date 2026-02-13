# SmartCourse - User Guide

## 🎯 Getting Started

Welcome to SmartCourse! This guide will help you discover your perfect courses using AI-powered recommendations.

---

## 📌 Table of Contents

1. [Creating an Account](#creating-an-account)
2. [Logging In](#logging-in)
3. [Finding Courses](#finding-courses)
4. [Understanding Results](#understanding-results)
5. [Managing Your Dashboard](#managing-your-dashboard)
6. [Comparing Models](#comparing-models)
7. [Tips & Tricks](#tips--tricks)
8. [FAQ](#faq)

---

## Creating an Account

### Step-by-Step Registration

1. **Visit SmartCourse Homepage**
   - Open http://localhost:5000 in your browser
   - Click "Create Free Account" button

2. **Fill Registration Form**
   - **Username:** Choose a unique username (3-20 characters)
   - **Email:** Enter your valid email address
   - **Password:** Create a strong password (minimum 6 characters)

3. **Submit & Verify**
   - Click "Create Account"
   - You'll be redirected to login page

4. **Login with Your Credentials**
   - Enter username and password
   - Click "Login"
   - You're now ready to find courses!

**Account Tips:**
- ✓ Use a memorable username
- ✓ Use a strong password with mix of letters, numbers, symbols
- ✓ Keep your password secure

---

## Logging In

### Quick Login

1. Click "Sign In" on homepage
2. Enter your username
3. Enter your password
4. Click "Login"

**Remember Me:** Check the option to stay logged in (coming in v2.0)

### Forgot Password? (Coming Soon)
- Feature available in v2.0
- For now, contact: bilal.saleem@vu.edu.pk

---

## Finding Courses

### Step 1: Go to Recommendations

After logging in:
- Click "Get Recommendations" in navigation
- Or click "Start Exploring" button on homepage

### Step 2: Describe What You Want to Learn

In the text area, describe your learning goal naturally:

**Example Queries:**

```
✓ "I want to learn Python for data science"
✓ "Web development with React and Node.js"
✓ "Machine learning and artificial intelligence"
✓ "Mobile app development for iOS"
✓ "Digital marketing with Google Analytics"
```

**Tips for Better Results:**
- Be specific about your goals
- Mention programming languages or tools
- Include your experience level if relevant
- Describe the outcome you want

### Step 3: Choose Your Model

**Two options available:**

**🔹 TF-IDF (Faster)**
- Best for: Specific technical keywords
- Speed: Very fast (< 100ms)
- Use when: Searching for specific technologies, languages, tools
- Example: "Python Flask REST API"

**🔹 Neural (More Accurate)**
- Best for: Intent-based, semantic queries
- Speed: Medium (200-500ms)
- Use when: Describing your learning goal broadly
- Example: "I want to build web applications"

**Which Should I Choose?**

| Your Query Type | Choose |
|-----------------|--------|
| "Learn [Language]" | TF-IDF |
| "I want to..." | Neural |
| "Build [Project]" | TF-IDF |
| "Understand [Concept]" | Neural |
| "Course in [Specific Tool]" | TF-IDF |
| "How to become [Role]" | Neural |

### Step 4: Get Results

Click "Get Recommendations" button

The system will:
- Analyze your query
- Search through 8,500+ courses
- Return top 10 matches
- Calculate relevance scores

---

## Understanding Results

### Course Card Components

Each recommended course shows:

```
┌─────────────────────────────────────────┐
│  Course Title                     [❤️]  │
│  By: University Name                    │
│  Department: Subject Area               │
│                                         │
│  📝 Description: Full course description│
│                                         │
│  ⭐ Relevance Score: 87%               │
│  ▓▓▓▓▓▓▓▓▓░                           │
│                                         │
│  📍 City  📚 Department  ⏱️ Duration  │
└─────────────────────────────────────────┘
```

### Relevance Score Explained

**What is it?**
A percentage (0-100%) showing how relevant the course is to your query.

**How to interpret:**
- **90-100%:** Excellent match - highly relevant
- **75-89%:** Very good match - recommended
- **60-74%:** Good match - worth exploring
- **Below 60%:** Okay match - might be less relevant

**Why scores differ between models:**
- TF-IDF: Based on keyword matching
- Neural: Based on semantic meaning
- Different models see "relevance" differently

### Saving Courses

**To Save a Course:**

1. Click the ❤️ heart icon on any course card
2. Course added to your "Favorites"
3. Access anytime from Dashboard

**To Remove from Favorites:**

1. Click the ❤️ heart icon again
2. Course removed from favorites
3. Heart becomes outlined ☆

---

## Managing Your Dashboard

### Dashboard Features

**Three Main Sections:**

#### 1. Search History Tab
Shows all your previous searches:
- Search query
- Date and time
- Model used (TF-IDF or Neural)
- Top 3 results from each model

**Actions:**
- ✓ View full results
- ✓ Delete search entry
- ✓ Re-run same search

**How to Use:**
- Easily revisit previous searches
- Compare queries over time
- Learn what works best for you

#### 2. Favorites Tab
Your saved courses:
- All courses you've bookmarked
- Organized by save date
- Quick access anytime

**Actions:**
- ✓ View course details
- ✓ Remove from favorites
- ✓ Export as list

#### 3. Comparison Tab (Coming Soon)
See side-by-side results from both models for the same query

---

## Comparing Models

### When to Use Model Comparison

**TF-IDF vs Neural:**

**Try TF-IDF when:**
```
✓ "Python 3 course"
✓ "React.js tutorial"
✓ "SQL database training"
✓ Very specific technical queries
```

**Try Neural when:**
```
✓ "I want to learn coding"
✓ "How to become a data scientist"
✓ "Web development skills"
✓ Broader, intent-based queries
```

### Reading Comparison Results

**TF-IDF typically:**
- Returns exact keyword matches first
- Great for technical courses
- Very precise but less flexible

**Neural typically:**
- Returns contextually relevant courses
- Great for conceptual queries
- More flexible interpretation

**Key Insight:** If results differ greatly between models, try rephrasing your query or combine both result sets.

---

## Tips & Tricks

### 🎯 Search Tips

1. **Be Specific**
   - ❌ "Programming"
   - ✓ "Python web development with Django"

2. **Use Natural Language**
   - ❌ "ML AI DL NLP"
   - ✓ "I want to learn machine learning for natural language processing"

3. **Include Context**
   - ❌ "Java course"
   - ✓ "Java for building Android mobile apps"

4. **Try Multiple Queries**
   - Same topic, different phrasing
   - See what the models find

### 💡 Best Practices

1. **Start Broad, Then Narrow**
   - First search: "I want to learn web development"
   - Second search: "Web development with Python Flask"

2. **Compare Model Results**
   - Run same query with both models
   - Combine best results from each

3. **Check Prerequisites**
   - Many advanced courses require basics
   - Look for course sequences

4. **Read Descriptions Carefully**
   - Check if it matches your level
   - Verify course duration/format
   - Check university reputation

5. **Save Interesting Courses**
   - Build your learning playlist
   - Organize by topic or order
   - Review before deciding

### ⚡ Quick Searches

**Learn a Language:**
```
"I want to learn [Language] from beginner to advanced"
```

**Career Change:**
```
"I want to transition to [Career] from [Current Background]"
```

**Skill Development:**
```
"I want to develop [Skill] for [Purpose]"
```

**Project-Based Learning:**
```
"I want to build [Project Type] using [Technology]"
```

---

## FAQ

### General Questions

**Q: How are courses ranked?**
A: By relevance score calculated by the AI model based on your query. Top results match best with your learning goal.

**Q: Can I search without logging in?**
A: No, you need an account to use recommendations. Create a free account to get started.

**Q: How many courses can I save?**
A: Unlimited! Save as many as you want to your Favorites.

**Q: Can I export my favorites?**
A: Yes! From Dashboard > Favorites, click "Export" (coming in v2.0).

### Search & Results Questions

**Q: Why are my results different each time?**
A: Each search is processed fresh. Results are deterministic (consistent) but may vary based on query phrasing or model selection.

**Q: What's the difference between TF-IDF and Neural?**
A: 
- TF-IDF: Matches exact keywords
- Neural: Understands meaning
- Use whichever gives better results for your query

**Q: Why didn't my course show up?**
A: Results show top 10 most relevant. Your course might be ranked lower. Try rephrasing your query.

**Q: Can I see more than 10 results?**
A: Currently showing top 10. Feature to expand results coming in v2.0.

### Technical Questions

**Q: Is my data secure?**
A: Yes! Password stored securely, JWT tokens for authentication, HTTPS recommended for production.

**Q: What if I forget my username?**
A: Contact support at bilal.saleem@vu.edu.pk

**Q: Can I change my password?**
A: Coming in v2.0. For now, contact support.

**Q: How often is the course database updated?**
A: Currently static at 8,500+ courses. Admin uploads new data periodically.

### Usage Questions

**Q: How many searches can I do?**
A: Unlimited! No search limit per user.

**Q: Can I collaborate with friends?**
A: Not yet. Share your favorites via email for now.

**Q: Is there a mobile app?**
A: Website is mobile-responsive. Native apps coming in v2.0.

**Q: What data do you collect?**
A: Only searches, favorites, and account info. No personal browsing data.

---

## Troubleshooting

### Not Getting Good Results?

1. **Try the other model**
   - If TF-IDF, try Neural
   - Each sees relevance differently

2. **Rephrase your query**
   - Be more specific
   - Add more context
   - Mention technologies

3. **Search multiple times**
   - Same query might find different results due to ranking

4. **Check your search terms**
   - Spelling matters
   - Use common course names
   - Add "course" or "tutorial"

### Account Issues

1. **Can't Login?**
   - Check username/password
   - Username is case-sensitive
   - Try reset password (coming soon)

2. **Account Locked?**
   - Not currently (coming in v2.0)
   - Contact support if needed

3. **Forgot Username?**
   - Check your registration email
   - Contact support

### Technical Issues

1. **Slow Results?**
   - Neural model is slower (normal)
   - Try TF-IDF for faster results
   - Check internet connection

2. **Page Not Loading?**
   - Refresh the page
   - Clear browser cache
   - Try different browser

3. **Can't Save to Favorites?**
   - Refresh page
   - Check browser console for errors
   - Contact support

---

## Contact & Support

**Need Help?**
- **Email:** bilal.saleem@vu.edu.pk
- **Supervisor:** Muhammad Bilal
- **Skype:** bilalsaleem101

**Report a Bug:**
Include:
- What you were doing
- What happened
- Expected behavior
- Browser/device info

---

## What's Coming in v2.0?

- 🔐 Password reset functionality
- 📊 Advanced analytics dashboard
- 🤝 Social features (share, collaborate)
- 📱 Mobile app
- 🌙 Dark mode
- ⭐ User ratings system
- 📧 Email notifications
- 🎓 Prerequisite recommendations
- 🔄 Continuous learning paths
- 🌐 Multi-language support

---

**Happy Learning! 🚀**

Start discovering courses that match your goals. The SmartCourse team is here to help you succeed!

**Version:** 1.0  
**Last Updated:** February 13, 2026
