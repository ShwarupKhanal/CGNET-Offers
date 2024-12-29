function checkOffers() {
    const searchInput = document.getElementById("searchInput").value.trim();
    const discountContainer = document.getElementById("discount-container");
    const bonusContainer = document.getElementById("bonus-container");
    const discountOffers = document.getElementById("discount-offers");
    const bonusOffers = document.getElementById("bonus-offers");
    const orderNowButton = document.querySelector(".btn1");

    discountContainer.style.display = "none";
    bonusContainer.style.display = "none";
    orderNowButton.style.display = "none"; 

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
                let hasOffers = false;

                if (data.discountOffers && data.discountOffers.length > 0) {
                    discountContainer.style.display = "block";
                    data.discountOffers.forEach(offer => {
                        const offerElement = document.createElement("p");
                        offerElement.textContent = offer;
                        discountOffers.appendChild(offerElement);
                    });
                    hasOffers = true;
                }

                if (data.bonusOffers && data.bonusOffers.length > 0) {
                    bonusContainer.style.display = "block";
                    data.bonusOffers.forEach(offer => {
                        const offerElement = document.createElement("p");
                        offerElement.textContent = offer;
                        bonusOffers.appendChild(offerElement);
                    });
                    hasOffers = true;
                }

                if (hasOffers) {
                    orderNowButton.style.display = "inline-block";
                } else {
                    alert("No offers available for the given details.");
                }
            }
        })
        .catch(error => {
            console.error("Error fetching offers:", error);
            alert("An error occurred while fetching offers. Please try again.");
        });
}
