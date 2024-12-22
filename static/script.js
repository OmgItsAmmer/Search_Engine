async function searchItems() {
    const query = document.getElementById("searchInput").value.trim();
    const resultsContainer = document.getElementById("resultsContainer");
    resultsContainer.innerHTML = ""; // Clear previous results

    if (!query) {
        resultsContainer.innerHTML = "<p>Please enter a search query.</p>";
        return;
    }

    try {
        // Send a POST request to the Flask backend
        const response = await fetch('/search', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: query })
        });

        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }

        const results = await response.json();

        if (results.length === 0) {
            resultsContainer.innerHTML = "<p>No results found.</p>";
            return;
        }

        // Render the results
        results.forEach(result => {
            const card = document.createElement("div");
            card.className = "card";
            card.textContent = `Document ID: ${result}`; // Replace this with your result formatting
            resultsContainer.appendChild(card);
        });
    } catch (error) {
        console.error(error);
        resultsContainer.innerHTML = "<p>An error occurred while fetching results.</p>";
    }
}
