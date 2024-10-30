// Add any client-side JavaScript functionality here
console.log("Eco-Sentry JavaScript loaded");

// Example: Fade out flash messages after 5 seconds
document.addEventListener("DOMContentLoaded", function() {
    const flashMessages = document.querySelectorAll(".alert");
    flashMessages.forEach(function(message) {
        setTimeout(function() {
            message.style.transition = "opacity 1s";
            message.style.opacity = 0;
        }, 5000);
    });
});