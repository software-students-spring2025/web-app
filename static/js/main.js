/* main.js - Handles frontend interactions for Travel Match */

document.addEventListener("DOMContentLoaded", () => {
    setupLoginForm();
    setupRegisterForm();
    setupPreferencesForm();
    setupLogoutButton();
    fetchMatches();
});

// Handle login form submission
function setupLoginForm() {
    const loginForm = document.querySelector("form[action='/login']");
    if (loginForm) {
        loginForm.addEventListener("submit", async (event) => {
            event.preventDefault();
            const formData = new FormData(loginForm);
            const response = await fetch("/api/auth/login", {
                method: "POST",
                body: formData
            });
            const result = await response.json();
            if (result.success) {
                window.location.href = "/profile";
            } else {
                alert("Login failed. Please try again.");
            }
        });
    }
}

// Handle registration form submission
function setupRegisterForm() {
    const registerForm = document.querySelector("form[action='/register']");
    if (registerForm) {
        registerForm.addEventListener("submit", async (event) => {
            event.preventDefault();
            const formData = new FormData(registerForm);
            const response = await fetch("/api/auth/register", {
                method: "POST",
                body: formData
            });
            const result = await response.json();
            if (result.success) {
                window.location.href = "/login";
            } else {
                alert("Registration failed. Please try again.");
            }
        });
    }
}

// Handle preferences form submission
function setupPreferencesForm() {
    const preferencesForm = document.querySelector("form[action='/preferences']");
    if (preferencesForm) {
        preferencesForm.addEventListener("submit", async (event) => {
            event.preventDefault();
            const formData = new FormData(preferencesForm);
            const response = await fetch("/api/preferences", {
                method: "POST",
                body: formData
            });
            const result = await response.json();
            if (result.success) {
                alert("Preferences updated successfully!");
            } else {
                alert("Failed to update preferences.");
            }
        });
    }
}

// Handle logout functionality
function setupLogoutButton() {
    const logoutBtn = document.getElementById("logout-btn");
    if (logoutBtn) {
        logoutBtn.addEventListener("click", async () => {
            await fetch("/api/auth/logout", { method: "POST" });
            window.location.href = "/login";
        });
    }
}

// Fetch and display matches dynamically
async function fetchMatches() {
    const matchesContainer = document.getElementById("matches-container");
    if (matchesContainer) {
        const response = await fetch("/api/matches");
        const matches = await response.json();
        matchesContainer.innerHTML = "";
        matches.forEach(match => {
            matchesContainer.innerHTML += `
                <div class="card mt-3">
                    <div class="card-body">
                        <h5 class="card-title">${match.username}</h5>
                        <p class="card-text">Preferences: ${match.preferences}</p>
                        <a href="/profile/${match.id}" class="btn btn-primary">View Profile</a>
                    </div>
                </div>`;
        });
    }
}
