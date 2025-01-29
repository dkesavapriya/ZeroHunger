const socket = io("http://127.0.0.1:5000", {
    query: { user_id: localStorage.getItem("user_id") },
});

socket.on("new_donation", (data) => {
    alert(data.message); // Show a popup for new donation
});

socket.on("donation_accepted", (data) => {
    alert(data.message); // Show a popup when donation is accepted
});
