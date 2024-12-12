function checkOffers() {
    const userId = document.getElementById("userId").value.trim();
    const offerContainer = document.getElementById("offer-container");
    
    if (!userId) {
      offerContainer.textContent = "Please enter a valid user ID.";
      return;
    }
  
    fetch(`http://127.0.0.1:5000/offers/${userId}`)
      .then(response => {
        if (!response.ok) {
          throw new Error(`Server error: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        offerContainer.innerHTML = "";
        if (data.error) {
          offerContainer.textContent = data.error;
        } else {
          // Use 'data.offers' since the backend returns an object with 'offers' key
          data.offers.forEach(offer => {
            const offerElement = document.createElement("p");
            offerElement.textContent = offer;
            offerContainer.appendChild(offerElement);
          });
        }
      })
      .catch(error => {
        console.error("Error fetching offers:", error);
        offerContainer.textContent = "An error occurred. Please try again.";
      });
  }
  