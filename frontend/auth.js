const API_URL = "http://127.0.0.1:8000";

function showLogin() {
    document.getElementById('loginForm').classList.remove('hidden');
    document.getElementById('signupForm').classList.add('hidden');
    document.getElementById('authSubtitle').innerText = "Welcome to your student portal";
    document.getElementById('authToggleText').innerHTML = 'Need an account? <a href="#" onclick="showSignup()">Sign Up</a>';
    document.querySelectorAll('.tab')[0].classList.add('active');
    document.querySelectorAll('.tab')[1].classList.remove('active');
}

function showSignup() {
    document.getElementById('loginForm').classList.add('hidden');
    document.getElementById('signupForm').classList.remove('hidden');
    document.getElementById('authSubtitle').innerText = "Join Academia today";
    document.getElementById('authToggleText').innerHTML = 'Already have an account? <a href="#" onclick="showLogin()">Login</a>';
    document.querySelectorAll('.tab')[0].classList.remove('active');
    document.querySelectorAll('.tab')[1].classList.add('active');
}

// Handle Login
document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;
    const role = document.getElementById('loginRole').value;

    try {
        const response = await fetch(`${API_URL}/login?username=${username}&password=${password}`, {
            method: 'POST'
        });

        const data = await response.json();

        if (response.ok) {
            localStorage.setItem('username', username);
            localStorage.setItem('role', data.role);
            alert("Login Successful!");
            window.location.href = "dashboard.html";
        } else {
            alert(data.detail || "Login failed");
        }
    } catch (err) {
        alert("Server error. Make sure backend is running.");
    }
});

// Handle Signup
document.getElementById('signupForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('signupUsername').value;
    const password = document.getElementById('signupPassword').value;
    const confirm = document.getElementById('signupConfirm').value;
    const role = document.getElementById('signupRole').value;

    if (password !== confirm) {
        alert("Passwords do not match!");
        return;
    }

    try {
        const response = await fetch(`${API_URL}/signup`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password, role })
        });

        const data = await response.json();

        if (response.ok) {
            alert("Account created successfully! Please login.");
            showLogin();
        } else {
            alert(data.detail || "Signup failed");
        }
    } catch (err) {
        alert("Server error. Make sure backend is running.");
    }
});
