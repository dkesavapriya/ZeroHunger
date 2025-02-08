document.addEventListener("DOMContentLoaded", async function () {
    const token = localStorage.getItem("token");
    if (!token) {
        console.log("No token found, redirecting to login...");
        window.location.href = "login.html";  // ✅ Redirect to login if no token
    } else {
        console.log("Token found, loading dashboard...");
    }
    
    await fetchDonations();
    await fetchNotifications();
    await fetchDashboardStats();
    });
    
    // ✅ Fetch Donations from the Backend
    async function fetchDonations() {
    let response = await fetch("/donations", {
    headers: { "Authorization": "Bearer " + localStorage.getItem("token") }
    });
    
    let data = await response.json();
    let donationList = document.getElementById("donation-list");
    donationList.innerHTML = "";
    
    data.forEach(donation => {
    let donationItem = document.createElement("div");
    donationItem.classList.add("donation");
    donationItem.innerHTML = `
    <h3>${donation.food_item} - ${donation.quantity}</h3>
    <p><strong>Donor:</strong> ${donation.donor_name}</p>
    <p><strong>Location:</strong> ${donation.location}</p>
    <button class="accept-btn" data-id="${donation.id}">Accept</button>
    `;
    donationList.appendChild(donationItem);
    });
    
    // Add event listener for accepting donations
    document.addEventListener("click", function (event) {
    if (event.target.classList.contains("accept-btn")) {
    let donationId = event.target.getAttribute("data-id");
    acceptDonation(donationId);
    }
    });
    }
    
    // ✅ Accept a Donation
    async function acceptDonation(donationId) {
    let response = await fetch(`/donations/accept/${donationId}`, {
    method: "POST",
    headers: { "Authorization": "Bearer " + localStorage.getItem("token") }
    });
    
    let result = await response.json();
    alert(result.message);
    fetchDonations(); // Refresh the donation list after accepting
    }
    
    // ✅ Fetch Dashboard Stats
    async function fetchDashboardStats() {
    try {
    let response = await fetch("/dashboard/stats", {
    headers: {
    "Authorization": "Bearer " + localStorage.getItem("token"),
    }
    });
    let data = await response.json();
    
    document.getElementById("total-donations").innerText = data.total_donations;
    document.getElementById("accepted-donations").innerText = data.accepted_donations;
    document.getElementById("pending-donations").innerText = data.pending_donations;
    document.getElementById("user-donations").innerText = data.user_donations;
    document.getElementById("user-accepted").innerText = data.user_accepted;
    } catch (error) {
    console.error("Error fetching dashboard stats:", error);
    }
    }
    
    // ✅ Fetch Notifications
    async function fetchNotifications() {
    let response = await fetch("/notifications", {
    headers: { "Authorization": "Bearer " + localStorage.getItem("token") }
    });
    
    let data = await response.json();
    let notificationList = document.getElementById("notification-list");
    notificationList.innerHTML = "";
    
    data.forEach(notification => {
    let li = document.createElement("li");
    li.textContent = notification.message;
    notificationList.appendChild(li);
    });
    }
    
    // ✅ Logout User
    function logout() {
    localStorage.removeItem("token");
    window.location.href = "login.html";
    }