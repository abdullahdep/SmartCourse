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
                <div class="card mb-3 p-3 border ">
                    <h3>${r.title}</h3>
                    <p>${r.description}</p>
                    <strong>Relevance: ${r.score.toFixed(2)}%</strong>
                    <p> <b>Department:</b> ${r.department}</p>
                    <p><b>City/Cities:</b> ${r.city}</p>
                    <p><b>Shifts:</b> ${r.shifts}</p>
                    <p><b>Online:</b> ${r.online}</p>
                    <p><b>Admission Dates:</b> ${r.admission_dates}</p>
                    <p><b>Marks Required:</b> ${r.marks_required}</p>
                    <p><b>Labs Available:</b> ${r.labs_available}</p>
                </div>
            `;
        });
    });
}
