/*document.getElementById("register-form").addEventListener("submit", function (event) {
    event.preventDefault();

    let name = document.getElementById("name").value;
    let email = document.getElementById("email").value;
    let password = document.getElementById("password").value;
    let role = document.getElementById("role").value;

    fetch("/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: name, email: email, password: password, role: role })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("register-message").innerText = data.message;
        if (data.success) {
            window.location.href = "/login";
        }
    });
});*/
