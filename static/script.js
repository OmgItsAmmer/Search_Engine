// Handling Search Form Submission

document.getElementById('search-form').addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent default form submission

    const query = document.getElementById('query').value; // Get the search query

    // Show loading message
    document.getElementById('loading').style.display = 'block';

    // Send the search query to Flask via a POST request
    fetch('/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: query }) // Send query as JSON body
    })
    .then(response => response.json()) // Parse the response as JSON
    .then(data => {
        // Hide loading message
        document.getElementById('loading').style.display = 'none';

        // Handle the results
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
                        <div class="card-year">Year: ${Math.trunc(product.year)}</div>
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

// Handling Item Submission (Add Item Form)
document.querySelector('form[action="/submit"]').addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent default form submission

    // Get the values from the form
    const title = document.querySelector('input[name="title"]').value;
    const gender = document.querySelector('select[name="gender"]').value;
    const category = document.querySelector('select[name="category"]').value;
    const subCategory = document.querySelector('input[name="subcategory"]').value;
    const year = parseInt(document.querySelector('input[name="year"]').value, 10);
    const imageUrl = document.querySelector('input[name="image_url"]').value;

    // Basic validation
    if (!title || !gender || !category || !subCategory || isNaN(year) || !imageUrl) {
        alert('Please fill in all the fields.');
        return;
    }

    // Show loading message
    document.getElementById('loading').style.display = 'block';

    // Send the item data to Flask via a POST request
    fetch('/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            title: title,
            gender: gender,
            category: category,
            subCategory: subCategory,
            year: year,
            image_url: imageUrl
        })
    })
    .then(response => response.json()) // Parse the response as JSON
    .then(data => {
        // Hide loading message
        document.getElementById('loading').style.display = 'none';

        if (data.status === 'success') {
            alert('Item added successfully!');
            // Optionally, reset form or close offcanvas
            document.querySelector('form[action="/submit"]').reset();
        } else {
            alert('Error adding item: ' + data.message);
        }
    })
    .catch(error => {
        // Hide loading message and display error
        document.getElementById('loading').style.display = 'none';
        alert('Error: ' + error);
    });
});
