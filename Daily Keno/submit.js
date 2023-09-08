// submit.js
document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("kenoForm");

    form.addEventListener("submit", function(event) {
        event.preventDefault();

        const formData = new FormData(form);
        const jsonData = Object.fromEntries(formData);

        fetch("/add_entry", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(jsonData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                alert("Entry added successfully.");
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            alert("An error occurred: " + error);
        });
    });
});
