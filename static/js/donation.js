// Fetch and display donations when the page is loaded
document.addEventListener("DOMContentLoaded", function () {
    fetch("/donations/all")
        .then(response => response.json())
        .then(data => {
            let list = document.getElementById("donation-list");
            list.innerHTML = ""; // Clear any existing donations in the list

            // Iterate through each donation and display it
            data.donations.forEach(donation => {
                let li = document.createElement("li");
                li.innerHTML = `
                    <strong>${donation.food_type}</strong> - ${donation.quantity}
                    <br> Location: ${donation.location}
                    <br> Donor: ${donation.donor}
                    <br> 
                    ${donation.accepted_by ? "Accepted by: " + donation.accepted_by : '<button onclick="acceptDonation(' + donation.id + ')">Accept</button>'}
                `;
                list.appendChild(li);  // Add the donation to the list
            });
        })
        .catch(error => console.error("Error fetching donations:", error));  // Handle any errors in the fetch
});

// Function to accept a donation
function acceptDonation(donationId) {
    fetch(`/donations/accept/${donationId}`, {
        method: "POST",
        headers: {
            "Authorization": "Bearer " + localStorage.getItem("token"),
            "Content-Type": "application/json"
        }
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);  // Show the response message after accepting the donation
        location.reload();  // Reload the page to update the donations list
    })
    .catch(error => console.error("Error accepting donation:", error));  // Handle errors while accepting donation
}
