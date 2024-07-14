document.addEventListener("DOMContentLoaded", function() {
    const urlForm = document.getElementById("url-form");
    const resultDiv = document.getElementById("result");

    urlForm.addEventListener("submit", async function(event) {
        event.preventDefault(); // Empêche le rechargement de la page
        const urlInput = document.getElementById("url").value;
        await checkURL(urlInput);
    });

    async function checkURL(url) {
        try {
            const formData = new FormData();
            formData.append("url", url);

            const response = await fetch("/url", {
                method: "POST",
                body: formData
            });

            handleResponse(response);
        } catch (error) {
            displayResult(error.message, "red");
        }
    }

    async function handleResponse(response) {
        try {
            const data = await response.json(); 
            if (response.ok) {
                displayResult(`<a href="${data.short_url}" target="_blank">${data.short_url}</a>`, "green"); 
            } else {
                displayResult(data.detail, "red"); 
            }
        } catch (error) {
            displayResult("Error processing response", "red");
        }
    }

    function displayResult(message, color) {
        resultDiv.innerHTML = message;
        resultDiv.style.color = color;
    }
});
