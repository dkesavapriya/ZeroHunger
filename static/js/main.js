document.addEventListener("DOMContentLoaded", function () {
    checkLoginStatus();
    loadDonations();
    setupRealTimeNotifications();
    });
    
    // ✅ Function to Register a User (Volunteer/Recipient)
    async function registerUser(event) {
    event.preventDefault();
    const formData = {
    name: document.getElementById("name").value,
    email: document.getElementById("email").value,
    password: document.getElementById("password").value,
    address: document.getElementById("address").value,
    role: document.getElementById("role").value
    };
    
    const response = await fetch("/auth/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(formData)
    });
    
    const data = await response.json();
    alert(data.message);
    
    if (response.ok) {
    window.location.href = "/login"; // Redirect to login page
    }
    }
    
    // ✅ Function to Login User
    async function loginUser(event) {
    event.preventDefault();
    
    const formData = {
    email: document.getElementById("login-email").value,
    password: document.getElementById("login-password").value
    };
    
    const response = await fetch("/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(formData)
    });
    
    const data = await response.json();
    
    if (response.ok) {
    localStorage.setItem("token", data.token);
    localStorage.setItem("user_id", data.user_id);
    window.location.href = "/dashboard";
    } else {
    alert(data.message);
    }
    }
    
    // ✅ Function to Fetch & Display Donations
    async function loadDonations() {
    const response = await fetch("/donations", {
    headers: { "Authorization": "Bearer " + localStorage.getItem("token") }
    });
    
    const donations = await response.json();
    const donationContainer = document.getElementById("donation-list");
    donationContainer.innerHTML = "";
    
    donations.forEach(donation => {
    donationContainer.innerHTML += `
    <div class="card">
    <h3>${donation.food_item}</h3>
    <p>Quantity: ${donation.quantity}</p>
    <p>Donor: ${donation.donor_name}</p>
    <button onclick="acceptDonation('${donation.id}')">Accept</button>
    </div>
    `;
    });
    }
    
    // ✅ Function to Accept a Donation
    async function acceptDonation(donationId) {
    const response = await fetch(`/donations/accept/${donationId}`, {
    method: "POST",
    headers: { "Authorization": "Bearer " + localStorage.getItem("token") }
    });
    
    const data = await response.json();
    alert(data.message);
    loadDonations(); // Refresh donation list
    }
    
    // ✅ Function to Check if User is Logged In
    function checkLoginStatus() {
    const token = localStorage.getItem("token");
    if (!token) {
    window.location.href = "/login";
    }
    }
    
    // ✅ Logout Function
    function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("user_id");
    window.location.href = "/login";
    }
    
    // ✅ Real-time Notifications using Socket.io
    function setupRealTimeNotifications() {
    const socket = io("http://127.0.0.1:5000", { query: { user_id: localStorage.getItem("user_id") } });
    
    socket.on("notification", (data) => {
    let notificationBox = document.getElementById("notifications");
    let newNotification = document.createElement("div");
    newNotification.classList.add("notification");
    newNotification.innerHTML = `<p>${data.message}</p>`;
    notificationBox.prepend(newNotification);
    });
    }
    
    // Attach Event Listeners
    document.getElementById("register-form")?.addEventListener("submit", registerUser);
    document.getElementById("login-form")?.addEventListener("submit", loginUser);
    