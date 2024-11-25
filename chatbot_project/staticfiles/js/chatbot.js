document.getElementById("send-btn").addEventListener("click", function (event) {
    // Prevent the default action of the button (like page reload)
    event.preventDefault();

    // Get the user input value
    const userInput = document.getElementById("user-input").value.trim();

    if (userInput === "") {
        alert("Please enter a question.");
        return;  // If the input is empty, stop the function
    }

    // Send the message to the server using Fetch API
    fetch("/chatbot/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")  // CSRF token for security
        },
        body: JSON.stringify({ message: userInput })
    })
    .then((response) => response.json())
    .then((data) => {
        // Add user input and bot response to the chat log
        const chatLog = document.getElementById("chat-log");
        chatLog.innerHTML += `<p><strong>User:</strong> ${userInput}</p>`;
        chatLog.innerHTML += `<p><strong>Bot:</strong> ${data.response}</p>`;

        // Scroll the chat log to the bottom to show the latest messages
        chatLog.scrollTop = chatLog.scrollHeight;

        // Clear the input field for the next message
        document.getElementById("user-input").value = "";
    })
    .catch((error) => {
        console.error("Error:", error);
        alert("There was an error with your request. Please try again.");
    });
});

// Helper function to get CSRF token from cookies (for Django CSRF protection)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split("; ");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].split("=");
            if (cookie[0] === name) {
                cookieValue = decodeURIComponent(cookie[1]);
                break;
            }
        }
    }
    return cookieValue;
}
