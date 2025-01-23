document.addEventListener("DOMContentLoaded", function() {
    const urlForm = document.getElementById("url-form");
    const resultDiv = document.getElementById("result");

    urlForm.addEventListener("submit", async function(event) {
        event.preventDefault(); 
        const urlInput = document.getElementById("url").value;
        const slugInput = document.getElementById("slug").value;
        await checkURL(urlInput, slugInput);
    });

    /**
     * Send a POST request to the server with form data.
     * @param {string} url - The URL input value.
     * @param {string} slug - The optional slug input value.
     */
    async function checkURL(url, slug) {
        try {
            const formData = new FormData();
            formData.append("url", url);
            if (slug){
                formData.append("slug", slug);
            }

            const response = await fetch("/url", {
                method: "POST",
                body: formData
            });

            handleResponse(response);
        } catch (error) {
            displayResult(error.message, "red");
        }
    }

    /**
     * Function to handle the response from the server.
     * @param {Response} response - The response object from the fetch request.
     */
    async function handleResponse(response) {
        try {
            const data = await response.json(); 
            if (response.ok) {
                displayResult(`<a href="${data.short_url}" target="_blank" id="result-link">${data.short_url}</a>`, "green"); 
            } else {
                displayResult(data.detail, "red"); 
            }
        } catch (error) {
            displayResult("Error processing response", "red");
        }
    }

    /**
     * Function to display a message in the result div with specified color.
     * @param {string} message - The message to display.
     * @param {string} color - The color of the message (e.g., "green", "red").
     */
    function displayResult(message, color) {
        const resultSection = document.getElementById("result-section");
        const resultText = document.getElementById("result");
        const copyBtn = document.querySelector('.copy-btn');

        resultText.innerHTML = message;
        resultText.style.color = color;

        if(message && color != "red"){
            resultSection.style.display = "flex";
        }else if (color == "red") {
            copyBtn.style.display = "none";
        } else {
            copyBtn.style.display = "flex";            
        }
    }
});

function copyToClipboard() {
    const resultLink = document.getElementById("result-link").textContent;
    navigator.clipboard.writeText(resultLink);
}