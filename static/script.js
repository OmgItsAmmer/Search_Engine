document.getElementById('search-form').addEventListener('submit', function (event) {
    event.preventDefault();
    const query = document.getElementById('query').value;

    // Show loading message
    document.getElementById('loading').style.display = 'block';

    // Send the search query to Flask via a POST request
    fetch('/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: query })
    })
        .then(response => response.json())
        .then(data => {
            // Hide loading message
            document.getElementById('loading').style.display = 'none';

            // Display the search results
            const resultsDiv = document.getElementById('results');
            if (data.length === 0) {
                resultsDiv.innerHTML = '<p>No products found.</p>';
            } else {
                resultsDiv.innerHTML = data.map(product => `
                <div class="card">
                    <img src="${product.image}" alt="${product.title}">
                    <div class="card-content">
                        <div class="card-title">${product.title}</div>
                        <div class="card-gender">Gender: ${product.gender}</div>
                        <div class="card-sub-category">Sub-category: ${product.sub_category}</div>
                        <div class="card-year">Year: ${product.year}</div>
                    </div>
                </div>
            `).join('');
            }
        })
        .catch(error => {
            // Hide loading message and display error
            document.getElementById('loading').style.display = 'none';
            document.getElementById('results').innerHTML = '<p>Error occurred during the search.</p>';
            console.error('Error:', error);
        });
});






























































// async function searchItems() {
//     const query = document.getElementById("searchInput").value.trim();
//     const resultsContainer = document.getElementById("resultsContainer");
//     resultsContainer.innerHTML = ""; // Clear previous results

//     if (!query) {
//         resultsContainer.innerHTML = "<p>Please enter a search query.</p>";
//         return;
//     }

//     try {
//         // Send a POST request to the Flask backend
//         const response = await fetch('/search', {
//             method: 'POST',
//             headers: { 'Content-Type': 'application/json' },
//             body: JSON.stringify({ query: query })
//         });

//         if (!response.ok) {
//             throw new Error(`Error: ${response.statusText}`);
//         }

//         const results = await response.json();

//         if (results.length === 0) {
//             resultsContainer.innerHTML = "<p>No results found.</p>";
//             return;
//         }

//         // Render the results
//         results.forEach(result => {
//             const card = document.createElement("div");
//             card.className = "card";
//             card.textContent = `Document ID: ${result}`; // Replace this with your result formatting
//             resultsContainer.appendChild(card);
//         });
//     } catch (error) {
//         console.error(error);
//         resultsContainer.innerHTML = "<p>An error occurred while fetching results.</p>";
//     }
// }
