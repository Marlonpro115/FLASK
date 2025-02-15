document.getElementById("togglePassword").addEventListener("click", function () {
    let passwordInput = document.getElementById("password");
    let icon = this.querySelector("i");

    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        icon.classList.remove("bi-eye");
        icon.classList.add("bi-eye-slash");
    } else {
        passwordInput.type = "password";
        icon.classList.remove("bi-eye-slash");
        icon.classList.add("bi-eye");
    }
});

document.getElementById("recoveryForm").addEventListener("submit", function () {
    let button = document.getElementById("sendButton");
    let buttonText = document.getElementById("buttonText");
    let spinner = document.getElementById("loadingSpinner");

    button.disabled = true;
    buttonText.textContent = "Enviando...";
    spinner.classList.remove("d-none");
});

document.getElementById("registerForm").addEventListener("submit", function (event) {
    let password = document.getElementById("password").value;
    let confirmPassword = document.getElementById("password_confirm").value;
    let passwordMismatch = document.getElementById("passwordMismatch");

    if (password !== confirmPassword) {
        event.preventDefault();
        passwordMismatch.classList.remove("d-none");
        return;
    } else {
        passwordMismatch.classList.add("d-none");
    }

    let button = document.getElementById("registerButton");
    let buttonText = document.getElementById("buttonText");
    let spinner = document.getElementById("loadingSpinner");

    button.disabled = true;
    buttonText.textContent = "Registrando...";
    spinner.classList.remove("d-none");
});