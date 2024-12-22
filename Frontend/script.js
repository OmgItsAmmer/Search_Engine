
// Sample Data for Search Results
const items = [
    {
        name: "Laptop",
        description: "A high performance laptop for professionals.",
        image: "https://via.placeholder.com/300x150?text=Laptop"
    },
    {
        name: "Tshirt",
        description: "A sleek Tshirt with the latest features.",
        image: "https://via.placeholder.com/300x150?text=Tshirt"
    },
    {
        name: "Headphones",
        description: "Noise-cancelling over-ear headphones.",
        image: "https://via.placeholder.com/300x150?text=Headphones"
    },
    {
        name: "Camera",
        description: "A DSLR camera for capturing stunning photos.",
        image: "https://via.placeholder.com/300x150?text=Camera"
    },
    {
        name: "Smartwatch",
        description: "A smartwatch to track your fitness and notifications.",
        image: "https://via.placeholder.com/300x150?text=Smartwatch"
    },

    {
        name: "Laptop",
        description: "A high performance laptop for professionals.",
        image: "https://via.placeholder.com/300x150?text=Laptop"
    },
    {
        name: "Tshirt",
        description: "A sleek Tshirt with the latest features.",
        image: "https://via.placeholder.com/300x150?text=Tshirt"
    },
    {
        name: "Headphones",
        description: "Noise-cancelling over-ear headphones.",
        image: "https://via.placeholder.com/300x150?text=Headphones"
    },
    {
        name: "Camera",
        description: "A DSLR camera for capturing stunning photos.",
        image: "https://via.placeholder.com/300x150?text=Camera"
    },
    {
        name: "Smartwatch",
        description: "A smartwatch to track your fitness and notifications.",
        image: "https://via.placeholder.com/300x150?text=Smartwatch"
    },

    {
        name: "Laptop",
        description: "A high performance laptop for professionals.",
        image: "https://via.placeholder.com/300x150?text=Laptop"
    },
    {
        name: "Tshirt",
        description: "A sleek Tshirt with the latest features.",
        image: "https://via.placeholder.com/300x150?text=Tshirt"
    },
    {
        name: "Headphones",
        description: "Noise-cancelling over-ear headphones.",
        image: "https://via.placeholder.com/300x150?text=Headphones"
    },
    {
        name: "Camera",
        description: "A DSLR camera for capturing stunning photos.",
        image: "https://via.placeholder.com/300x150?text=Camera"
    },
    {
        name: "Smartwatch",
        description: "A smartwatch to track your fitness and notifications.",
        image: "https://via.placeholder.com/300x150?text=Smartwatch"
    },

    {
        name: "Laptop",
        description: "A high performance laptop for professionals.",
        image: "https://via.placeholder.com/300x150?text=Laptop"
    },
    {
        name: "Tshirt",
        description: "A sleek Tshirt with the latest features.",
        image: "https://via.placeholder.com/300x150?text=Tshirt"
    },
    {
        name: "Headphones",
        description: "Noise-cancelling over-ear headphones.",
        image: "https://via.placeholder.com/300x150?text=Headphones"
    },
    {
        name: "Camera",
        description: "A DSLR camera for capturing stunning photos.",
        image: "https://via.placeholder.com/300x150?text=Camera"
    },
    {
        name: "Smartwatch",
        description: "A smartwatch to track your fitness and notifications.",
        image: "https://via.placeholder.com/300x150?text=Smartwatch"
    }
];

// Function to Perform Search
function searchItems() {
    const query = document.getElementById("searchInput").value.toLowerCase();
    const resultsContainer = document.getElementById("resultsContainer");
    resultsContainer.innerHTML = ""; // Clear previous results

    const filteredItems = items.filter(item =>
        item.name.toLowerCase().includes(query) ||
        item.description.toLowerCase().includes(query)
    );

    if (filteredItems.length === 0) {
        resultsContainer.innerHTML = "<p>No results found.</p>";
        return;
    }

    filteredItems.forEach(item => {
        const card = document.createElement("div");
        card.className = "card";
        card.innerHTML = `
                    <img src="${item.image}" alt="${item.name}">
                    <div class="card-content">
                        <div class="card-title">${item.name}</div>
                        <div class="card-description">${item.description}</div>
                    </div>
                `;
        resultsContainer.appendChild(card);
    });
}
