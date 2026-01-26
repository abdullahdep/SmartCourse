// Get token from URL parameter (for recommend and other protected pages)
function getTokenFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('token');
}

// Check if user is authenticated before allowing recommendations
function checkAuthAndRecommend() {
    let token = localStorage.getItem("auth_token");

    // If token is in URL (from redirect), use that
    const urlToken = getTokenFromURL();
    if (urlToken) {
        token = urlToken;
        localStorage.setItem("auth_token", token);
    }

    if (!token) {
        alert("Please login or register to get course recommendations.");
        window.location.href = "/login";
        return;
    }

    getRecommendations();
}

function getRecommendations() {
    let token = localStorage.getItem("auth_token");

    // If token is in URL, use that
    const urlToken = getTokenFromURL();
    if (urlToken) {
        token = urlToken;
    }

    if (!token) {
        alert("Please login first.");
        window.location.href = "/login";
        return;
    }

    let query = document.getElementById("query").value;
    let model = document.getElementById("model").value;

    if (!query.trim()) {
        alert("Please enter a search query");
        return;
    }

    // Show loading animation
    document.getElementById("loadingOverlay").classList.add("active");

    fetch("/api/recommend", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        },
        body: JSON.stringify({ query, model })
    })
        .then(res => {
            if (res.status === 401) {
                alert("Your session has expired. Please login again.");
                localStorage.removeItem("auth_token");
                localStorage.removeItem("user_id");
                localStorage.removeItem("username");
                window.location.href = "/login";
                return;
            }
            return res.json();
        })
        .then(data => {
            // Hide loading animation
            document.getElementById("loadingOverlay").classList.remove("active");
            
            if (data && (data.results || data.tfidf || data.neural)) {
                displayResults(data);
            } else if (data && data.message) {
                alert("Error getting recommendations: " + data.message);
            } else {
                alert("Error getting recommendations. Please try again.");
            }
        })
        .catch(err => {
            document.getElementById("loadingOverlay").classList.remove("active");
            console.error("Error:", err);
            alert("An error occurred while fetching recommendations. Please check your query and try again.");
        });
}

function displayResults(data) {
    let box = document.getElementById("results");
    box.innerHTML = "";

    // Handle both old format (single results) and new format (tfidf, neural, comparison)
    let tfidfResults = data.tfidf || data.results || [];
    let neuralResults = data.neural || [];

    if (tfidfResults.length === 0 && neuralResults.length === 0) {
        box.innerHTML = "<p>No matching courses found.</p>";
        return;
    }

    // Create tabs
    let tabsHTML = `
        <div class="results-tabs">
            <button class="tab-button active" onclick="switchTab('tfidf')">📊 TF-IDF Results</button>
            <button class="tab-button" onclick="switchTab('neural')">🧠 Neural Results</button>
            <button class="tab-button" onclick="switchTab('comparison')">⚖️ Comparison</button>
        </div>
    `;

    // TFIDF Tab Content
    let tfidfHTML = `
        <div id="tfidf-tab" class="tab-content active">
            <h4 style="color: #007bff;">TF-IDF Model Results</h4>
    `;
    
    if (tfidfResults.length > 0) {
        tfidfResults.forEach((r, index) => {
            tfidfHTML += createCardHTML(r, index, 'tfidf');
        });
    } else {
        tfidfHTML += "<p>No results from TF-IDF model.</p>";
    }
    tfidfHTML += "</div>";

    // Neural Tab Content
    let neuralHTML = `
        <div id="neural-tab" class="tab-content">
            <h4 style="color: #28a745;">Neural Model Results</h4>
    `;
    
    if (neuralResults.length > 0) {
        neuralResults.forEach((r, index) => {
            neuralHTML += createCardHTML(r, index, 'neural');
        });
    } else {
        neuralHTML += "<p>No results from Neural model.</p>";
    }
    neuralHTML += "</div>";

    // Comparison Tab Content
    let comparisonHTML = `
        <div id="comparison-tab" class="tab-content">
            <h4>Side-by-Side Comparison</h4>
            <div class="comparison-grid">
                <div class="comparison-column">
                    <h4 class="tfidf">📊 TF-IDF Results</h4>
    `;
    
    if (tfidfResults.length > 0) {
        tfidfResults.forEach((r, index) => {
            comparisonHTML += createCardHTML(r, index + '-tfidf', 'tfidf');
        });
    } else {
        comparisonHTML += "<p>No results from TF-IDF model.</p>";
    }
    
    comparisonHTML += `
                </div>
                <div class="comparison-column">
                    <h4 class="neural">🧠 Neural Results</h4>
    `;
    
    if (neuralResults.length > 0) {
        neuralResults.forEach((r, index) => {
            comparisonHTML += createCardHTML(r, index + '-neural', 'neural');
        });
    } else {
        comparisonHTML += "<p>No results from Neural model.</p>";
    }
    
    comparisonHTML += `
                </div>
            </div>
        </div>
    `;

    // Combine all HTML
    box.innerHTML = tabsHTML + tfidfHTML + neuralHTML + comparisonHTML;

    // Load favorites and update star colors
    loadAndHighlightFavorites(tfidfResults.concat(neuralResults));
}

function createCardHTML(r, index, model) {
    const borderColor = model.includes('tfidf') || model === 'tfidf' ? '#007bff' : '#28a745';
    const scoreBackground = model.includes('tfidf') || model === 'tfidf' ? '#e7f3ff' : '#e8f5e9';
    
    return `
        <div class="card mb-3 p-3 border" data-course-title="${r.courseoffered}" style="border-left: 4px solid ${borderColor};">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div style="flex: 1;">
                    <p><b>${r.courseoffered}</b></p>
                    <progress id="file-progress-${index}" value="${r.score.toFixed(2)}" max="100"></progress> 
                    <span style="background: ${scoreBackground}; padding: 2px 6px; border-radius: 3px;">${r.score.toFixed(2)}%</span>
                    <p style="margin-top: 10px;"><b>Department:</b> ${r.department || 'N/A'}</p>
                    <p><b>University:</b> ${r.title || 'N/A'}</p>
                    <p><b>Description:</b> ${r.description}</p>
                </div>
                <button class="favorite-btn" data-course-index="${index}" data-course-title="${r.courseoffered}" onclick="toggleFavorite('${r.courseoffered}', ${index}, event)" style="background: none; border: none; font-size: 24px; cursor: pointer; padding: 5px; margin-left: 10px;" title="Add to favorites">
                    ⭐
                </button>
            </div>
        </div>
    `;
}

function switchTab(tabName) {
    // Hide all tabs
    document.querySelectorAll(".tab-content").forEach(tab => {
        tab.classList.remove("active");
    });
    
    // Deactivate all buttons
    document.querySelectorAll(".tab-button").forEach(btn => {
        btn.classList.remove("active");
    });
    
    // Show selected tab
    const selectedTab = document.getElementById(tabName + "-tab");
    if (selectedTab) {
        selectedTab.classList.add("active");
    }
    
    // Activate selected button
    event.target.classList.add("active");
}

function toggleFavorite(courseTitle, courseIndex, event) {
    event.preventDefault();
    event.stopPropagation();

    let token = localStorage.getItem("auth_token");
    const urlToken = getTokenFromURL();
    if (urlToken) {
        token = urlToken;
    }

    if (!token) {
        alert("Please login to save favorites.");
        return;
    }

    const button = event.target;
    const isFavorited = button.classList.contains("favorited");

    if (isFavorited) {
        // Remove from favorites
        fetch("/api/unfavorite", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token
            },
            body: JSON.stringify({ course_title: courseTitle })
        })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    button.classList.remove("favorited");
                    button.style.opacity = "0.5";
                    console.log("Removed from favorites");
                }
            })
            .catch(err => console.error("Error removing favorite:", err));
    } else {
        // Add to favorites - get course data from the displayed card
        const cardElement = event.target.closest('.card');
        const courseData = {
            title: courseTitle,
            // You can add more course data here if needed from the card
        };

        fetch("/api/favorite", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token
            },
            body: JSON.stringify({ 
                course_title: courseTitle,
                course_data: courseData
            })
        })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    button.classList.add("favorited");
                    button.style.opacity = "1";
                    console.log("Added to favorites");
                } else {
                    alert(data.message || "Could not add to favorites");
                }
            })
            .catch(err => console.error("Error adding favorite:", err));
    }
}

function loadAndHighlightFavorites(results) {
    let token = localStorage.getItem("auth_token");
    const urlToken = getTokenFromURL();
    if (urlToken) {
        token = urlToken;
    }

    if (!token) {
        return;
    }

    fetch("/api/favorites", {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        }
    })
        .then(res => res.json())
        .then(data => {
            if (data.success && data.favorites) {
                const favoriteNames = data.favorites.map(fav => fav.title);
                
                // Update all favorite buttons
                document.querySelectorAll(".favorite-btn").forEach(button => {
                    const courseTitle = button.getAttribute("data-course-title");
                    if (favoriteNames.includes(courseTitle)) {
                        button.classList.add("favorited");
                        button.style.opacity = "1";
                    } else {
                        button.classList.remove("favorited");
                        button.style.opacity = "0.5";
                    }
                });
            }
        })
        .catch(err => console.error("Error loading favorites:", err));
}

// Check auth on page load for recommend page
function checkAuthOnPageLoad() {
    const token = localStorage.getItem("auth_token");
    const username = localStorage.getItem("username");

    // Update UI if on recommend page
    const queryInput = document.getElementById("query");
    if (queryInput) {
        if (!token) {
            document.body.innerHTML = `
                <div style="max-width: 600px; margin: 50px auto; text-align: center;">
                    <h2>Access Denied</h2>
                    <p>You must be logged in to use the recommendation feature.</p>
                    <a href="/login" style="padding: 10px 20px; background-color: #007bff; color: white; text-decoration: none; border-radius: 4px; display: inline-block; margin-right: 10px;">Login</a>
                    <a href="/register" style="padding: 10px 20px; background-color: #28a745; color: white; text-decoration: none; border-radius: 4px; display: inline-block;">Register</a>
                </div>
            `;
        } else {
            // Add welcome message
            const welcomeDiv = document.createElement("div");
            welcomeDiv.style.cssText = "background-color: #e8f5e9; padding: 15px; margin-bottom: 20px; border-radius: 4px;";
            welcomeDiv.innerHTML = `<strong>Welcome, ${username}!</strong> Get your personalized course recommendations below.`;
            document.body.insertBefore(welcomeDiv, queryInput.parentElement);
        }
    }
}

// Load auth UI on page load
document.addEventListener("DOMContentLoaded", function () {
    checkAuthOnPageLoad();
});
