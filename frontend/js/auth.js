import { api, setToken } from "./api.js";

// switch between login/register tabs
window.switchTab = function(tab) {
    document.getElementById("login-form").style.display = tab === "login" ? "block" : "none";
    document.getElementById("register-form").style.display = tab === "register" ? "block" : "none";
    document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
    event.target.classList.add("active");
}

// show/hide student id field based on role
document.getElementById("reg-role").addEventListener("change", (e) => {
    document.getElementById("student-fields").style.display =
        e.target.value === "student" ? "block" : "none";
});

// handle login
window.handleLogin = async function() {
    const email = document.getElementById("login-email").value;
    const password = document.getElementById("login-password").value;

    try {
        const data = await api.post("/auth/login", { email, password });

        sessionStorage.setItem('access_token', data.access_token);

        setToken(data.access_token);

        const payload = JSON.parse(atob(data.access_token.split(".")[1]));
        const role = payload.role;

        if (role === "student") window.location.href = "student.html";
        else if (role === "company") window.location.href = "company.html";
        else if (role === "coordinator") window.location.href = "coordinator.html";

    } catch (err) {
        document.getElementById("error-msg").textContent = err.message;
    }
}

// handle register
window.handleRegister = async function() {
    const body = {
        email: document.getElementById("reg-email").value,
        password: document.getElementById("reg-password").value,
        full_name: document.getElementById("reg-fullname").value,
        role: document.getElementById("reg-role").value,
    };

    if (body.role === "student") {
        body.student_id = document.getElementById("reg-student-id").value;
    }

    try {
        await api.post("/auth/register", body);
        alert("Registered successfully! Please login.");
        switchTab("login");
    } catch (err) {
        document.getElementById("error-msg").textContent = err.message;
    }
}