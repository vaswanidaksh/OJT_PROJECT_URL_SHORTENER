
document.querySelectorAll(".nav-link").forEach(link => {
    link.addEventListener("click", function() {
        const target = this.getAttribute("data-target");

        document.querySelectorAll(".section").forEach(sec => sec.classList.remove("active"));
        document.getElementById(target).classList.add("active");
    });
});


document.getElementById("login-btn")?.addEventListener("click", function() {
    window.location.href = "login.html";
});

document.getElementById("loginForm")?.addEventListener("submit", function(e) {
    e.preventDefault();

    let user = document.getElementById("username").value;
    let pass = document.getElementById("password").value;

    if (!user || !pass) {
        alert("Please fill all fields");
        return;
    }

    alert("Login Success!");
    window.location.href = "ojt.html";
});
 function showSection(section) {
            document.getElementById('main').classList.add('hidden');
            document.getElementById('about').classList.add('hidden');
            document.getElementById(section).classList.remove('hidden');
        }
