function getRecommendations() {
    let query = document.getElementById("query").value;
    let model = document.getElementById("model").value;

    fetch("/api/recommend", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ query, model })
    })
    .then(res => res.json())
    .then(data => {
        let box = document.getElementById("results");
        box.innerHTML = "";

        data.results.forEach(r => {
            box.innerHTML += `
                <div class="card">
                    <h3>${r.title}</h3>
                    <p>${r.description}</p>
                    <strong>Relevance: ${r.score.toFixed(2)}%</strong>
                </div>
            `;
        });
    });
}
