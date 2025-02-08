document.getElementById("login-form").addEventListener("submit", function (event) {
    event.preventDefault();

    let email = document.getElementById("email").value;
    let password = document.getElementById("password").value;

    fetch("/auth/login", {
        method: "POST",
        headers: {
            
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ email: email, password: password })
    })
    .then(response => {
        console.log("Response:", response);
        return response.json();
    })
    .then(data => {
        if (data.token) {
            localStorage.setItem("token", data.token);
            
            window.location.href = "/dashboard";
        } else {
            alert(data.error || "Login failed");
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
});