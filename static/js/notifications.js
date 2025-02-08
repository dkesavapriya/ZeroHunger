// Fetch notifications on page load
document.addEventListener("DOMContentLoaded", function () {
    fetchNotifications(); // Initial fetch when page loads

    // Real-time UI with Socket.io
    const socket = io("http://127.0.0.1:5000");

    // Listen for new donation notifications
    socket.on("new_donation", function (data) {
        alert(data.message);  // Show real-time donation alert
        fetchNotifications();  // Refresh notifications list
    });

    // Listen for donation acceptance notifications
    socket.on("donation_accepted", function (data) {
        alert(data.message);  // Notify donor about acceptance
        fetchNotifications();  // Refresh notifications list
    });
});

// Fetch notifications from backend
async function fetchNotifications() {
    let response = await fetch("/notifications", {
        headers: { "Authorization": "Bearer " + localStorage.getItem("token") }
    });

    let data = await response.json();
    let notificationList = document.getElementById("notificationList");
    notificationList.innerHTML = "";  // Clear current notifications

    // Loop through notifications and add them to the list
    data.notifications.forEach(notification => {
        let li = document.createElement("li");
        li.textContent = notification.message;
        notificationList.appendChild(li);
    });
}
