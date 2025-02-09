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
        alert("Please enter a valid input (Account ID, User ID, or Phone). ");
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
            let hasOffers = false;

            if (data.offer1 && data.offer1.length > 0) {
                discountContainer.style.display = "block";
                const offerElement = document.createElement("p");
                offerElement.textContent = data.offer1;
                discountOffers.appendChild(offerElement);
                hasOffers = true;
            }

            if (data.offer2 && data.offer2.length > 0) {
                bonusContainer.style.display = "block";
                const offerElement = document.createElement("p");
                offerElement.textContent = data.offer2;
                bonusOffers.appendChild(offerElement);
                hasOffers = true;
            }

            if (!hasOffers) {
                discountContainer.style.display = "block";
                bonusContainer.style.display = "block";

                discountOffers.innerHTML = `
                    <p>Rs.10,999 - 150Mbps - 12 Month Internet Plan</p>
                    <p>Rs.11,999 - 250Mbps - 12 Month Internet Plan</p>
                    <p>Rs.12,999 - 350Mbps - 12 Month Internet Plan</p>
                `;

                bonusOffers.innerHTML = `
                    <p>Rs.13,999 - 157Mbps - 12 Month Internet+IPTV Plan</p>
                    <p>Rs.14,999 - 257Mbps - 12 Month Internet+IPTV Plan</p>
                    <p>Rs.15,999 - 357Mbps - 12 Month Internet+IPTV Plan</p>
                `;
            }
        })
        .catch(error => {
            console.error("Error fetching offers:", error);
            alert("An error occurred while fetching offers. Please try again.");
        });
}
