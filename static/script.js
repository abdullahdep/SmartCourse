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
        if (data && data.results) {
            displayResults(data.results);
        } else if (data && data.message) {
            alert("Error getting recommendations: " + data.message);
        } else {
            alert("Error getting recommendations. Please try again.");
        }
    })
    .catch(err => {
        console.error("Error:", err);
        alert("An error occurred while fetching recommendations. Please check your query and try again.");
    });
}

function displayResults(results) {
    let box = document.getElementById("results");
    box.innerHTML = "";

    if (results.length === 0) {
        box.innerHTML = "<p>No matching courses found.</p>";
        return;
    }

    results.forEach(r => {
        box.innerHTML += `
            <div class="card mb-3 p-3 border">
                <h3>${r.title}</h3>
                <p>${r.description}</p>
                <strong>Relevance: ${r.score.toFixed(2)}%</strong>
                <p><b>Department:</b> ${r.department || 'N/A'}</p>
                <p><b>City/Cities:</b> ${r.city || 'N/A'}</p>
                <p><b>Shifts:</b> ${r.shifts || 'N/A'}</p>
                <p><b>Online:</b> ${r.online || 'N/A'}</p>
                <p><b>Admission Dates:</b> ${r.admission_dates || 'N/A'}</p>
                <p><b>Marks Required:</b> ${r.marks_required || 'N/A'}</p>
                <p><b>Labs Available:</b> ${r.labs_available || 'N/A'}</p>
            </div>
        `;
    });
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
document.addEventListener("DOMContentLoaded", function() {
    checkAuthOnPageLoad();
});
