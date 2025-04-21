document.addEventListener("DOMContentLoaded", function () {
    console.log("JavaScript Loaded!");  // Debugging

    // Fetch food items when a category is clicked
    document.addEventListener("click", function (e) {
        if (e.target.classList.contains("category-btn")) {
            const categoryName = e.target.textContent.trim();
            console.log("Category Clicked:", categoryName);  // Debugging

            fetch(`/get-food-items/?category=${categoryName}`)
                .then(response => response.json())
                .then(data => {
                    let foodContainer = document.querySelector("#food-items");
                    if (!foodContainer) {
                        console.warn("Food items container not found!");
                        return;
                    }

                    foodContainer.innerHTML = ""; // Clear previous items

                    if (data.food_items.length > 0) {
                        data.food_items.forEach(food => {
                            let foodCard = document.createElement("div");
                            foodCard.classList.add("food-card");
                            foodCard.innerHTML = `
                                <img src="${food.image}" alt="${food.name}" class="food-image">
                                <h4>${food.name}</h4>
                                <p>₹${food.price}</p>
                                <button class="add-to-cart" data-food-id="${food.id}">Add to Cart</button>
                            `;
                            foodContainer.appendChild(foodCard);
                        });
                    } else {
                        foodContainer.innerHTML = "<p>No food items available for this category.</p>";
                    }
                })
                .catch(error => console.error("Error fetching food items:", error));
        }
    });

    // Fetch subcategories based on selected category
    document.addEventListener("click", function (e) {
        if (e.target.classList.contains("category-btn")) {
            const categoryId = e.target.getAttribute("data-category-id");
            console.log("Fetching Subcategories for Category ID:", categoryId);

            fetch(`/get-subcategories/${categoryId}/`)
                .then(response => response.json())
                .then(data => {
                    let subcategoryContainer = document.querySelector("#subcategory-container");
                    if (!subcategoryContainer) {
                        console.warn("Subcategory container not found!");
                        return;
                    }

                    subcategoryContainer.innerHTML = ""; // Clear existing subcategories
                    data.subcategories.forEach(subcategory => {
                        let btn = document.createElement("button");
                        btn.classList.add("subcategory-btn");
                        btn.setAttribute("data-subcategory-id", subcategory.id);
                        btn.textContent = subcategory.name;
                        subcategoryContainer.appendChild(btn);
                    });
                })
                .catch(error => console.error("Error fetching subcategories:", error));
        }
    });

    // Add to cart functionality
    document.addEventListener("click", function (e) {
        if (e.target.classList.contains("add-to-cart")) {
            const foodId = e.target.getAttribute("data-food-id");
            console.log("Adding to Cart:", foodId);

            fetch("/add-to-cart/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken()
                },
                body: JSON.stringify({ food_id: foodId })
            })
            .then(response => response.json())
            .then(data => {
                document.querySelector("#cart-count").textContent = data.cart_count;
                alert("Item added to cart!");
            })
            .catch(error => console.error("Error adding to cart:", error));
        }
    });

    // Increase/Decrease item quantity in cart
    document.addEventListener("click", function (e) {
        if (e.target.classList.contains("cart-quantity-btn")) {
            const foodId = e.target.getAttribute("data-food-id");
            const action = e.target.getAttribute("data-action");
            console.log("Updating Cart:", foodId, action);

            fetch("/update-cart/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken()
                },
                body: JSON.stringify({ food_id: foodId, action: action })
            })
            .then(response => response.json())
            .then(data => {
                let quantityElement = document.querySelector(`#quantity-${foodId}`);
                let totalAmountElement = document.querySelector("#total-amount");

                if (quantityElement) quantityElement.textContent = data.new_quantity;
                if (totalAmountElement) totalAmountElement.textContent = data.total_amount;
            })
            .catch(error => console.error("Error updating cart:", error));
        }
    });

    // Function to get CSRF Token
    function getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value || "";
    }
});
