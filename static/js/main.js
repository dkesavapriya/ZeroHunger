function acceptDonation(donationId) {
    fetch(`/donations/accept/${donationId}`, {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${localStorage.getItem("jwt_token")}`,
        },
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.message) {
                alert(data.message);
            } else {
                alert("Failed to accept donation.");
            }
        })
        .catch((error) => {
            console.error("Error:", error);
        });
}
