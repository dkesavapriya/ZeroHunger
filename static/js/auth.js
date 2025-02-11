// Handle login form submission
document.addEventListener("DOMContentLoaded", function () {
    console.log("auth.js loaded"); // Debugging

document.getElementById("loginForm").addEventListener("submit", async function (e) {
    e.preventDefault();
    console.log("Login form submitted"); // Add at the top of auth.js
 // Prevent default form submission behavior
    
    // Get email and password from input fields
    let email = document.getElementById("email").value;
    let password = document.getElementById("password").value;
    console.log("Sending login request:", email, password);

    // Send POST request to backend to authenticate the user
    try {
        // Send POST request to backend to authenticate the user
        let response = await fetch("/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        let data = await response.json();  // Parse the response as JSON
        console.log("Server response:", data);

        if (response.ok) {
            // On successful login, store the token in localStorage and redirect to dashboard
            localStorage.setItem("token", data.token);
            window.location.href = "/dashboard";
        } else {
            alert(data.message); // Show backend error message
        }
    } catch (error) {
        console.error("Error:", error);
        alert("An error occurred. Please try again.");
    }
});


// Handle registration form submission
let registerForm = document.getElementById("registerForm");
    if (registerForm) {  // Check if the form exists before adding the event listener
        registerForm.addEventListener("submit", async function (e) {
            e.preventDefault();
            console.log("Register form submitted");  // Prevent default form submission behavior

    // Get form values for name, email, password, and role
    let name = document.getElementById("name").value;
    let email = document.getElementById("email").value;
    let password = document.getElementById("password").value;
    let role = document.getElementById("role").value;

    // Send POST request to backend to register the user
    try {
        let response = await fetch("/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, email, password, role })
        });

        let data = await response.json();

        if (response.ok) {
            alert("Registration successful! Please login.");
            window.location.href = "login.html";
        } else {
            alert(data.message);
        }
    } catch (error) {
        console.error("Error:", error);
        alert("An error occurred. Please try again.");
    }
});
};
});