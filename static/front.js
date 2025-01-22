function checkOffers() {
    const searchInput = document.getElementById("searchInput").value.trim();
    const discountContainer = document.getElementById("discount-container");
    const bonusContainer = document.getElementById("bonus-container");
    const discountOffers = document.getElementById("discount-offers");
    const bonusOffers = document.getElementById("bonus-offers");

    discountContainer.style.display = "none";
    bonusContainer.style.display = "none";

    discountOffers.innerHTML = "";
    bonusOffers.innerHTML = "";

    if (!searchInput) {
        alert("Please enter a valid input (Account ID, User ID, or Phone).");
        return;
    }

    const params = new URLSearchParams({ search: searchInput });

    fetch(`/offers?${params.toString()}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Server error: ${response.status} - ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                if (data.offer1 && data.offer1.length > 0) {
                    discountContainer.style.display = "block";
                    const offerElement = document.createElement("p");
                    offerElement.textContent = data.offer1;
                    discountOffers.appendChild(offerElement);
                }

                if (data.offer2 && data.offer2.length > 0) {
                    bonusContainer.style.display = "block";
                    const offerElement = document.createElement("p");
                    offerElement.textContent = data.offer2;
                    bonusOffers.appendChild(offerElement);
                }

                if (!data.offer1 && !data.offer2) {
                    alert("No offers available for the given details.");
                }
            }
        })
        .catch(error => {
            console.error("Error fetching offers:", error);
            alert("An error occurred while fetching offers. Please try again.");
        });
}