// Telegram WebApp API integratsiyasi
const tg = window.Telegram.WebApp;
tg.expand(); // Ilovani to‘liq ekran qilish

// Login, Register, Upload va Admin tarif form logikasi
document.addEventListener("DOMContentLoaded", () => {
  // Login form
  const loginForm = document.querySelector("form[action='/login']");
  if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const formData = new FormData(loginForm);
      const response = await fetch("/login", {
        method: "POST",
        body: formData
      });
      const result = await response.json();
      alert(result.message);
    });
  }

  // Register form
  const registerForm = document.querySelector("form[action='/register']");
  if (registerForm) {
    registerForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const formData = new FormData(registerForm);
      const response = await fetch("/register", {
        method: "POST",
        body: formData
      });
      const result = await response.json();
      alert(result.message);
    });
  }

  // Upload form
  const uploadForm = document.querySelector("form[action='/upload']");
  if (uploadForm) {
    uploadForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const formData = new FormData(uploadForm);
      const response = await fetch("/upload", {
        method: "POST",
        body: formData
      });
      const result = await response.json();
      alert(result.message);
    });
  }

  // Admin tarif form
  const tariffForm = document.getElementById("tariffForm");
  if (tariffForm) {
    tariffForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const formData = new FormData(tariffForm);
      const response = await fetch("/admin/tariffs", {
        method: "POST",
        body: formData
      });
      const result = await response.json();
      alert(result.message);
    });
  }
});

// Premium obuna funksiyasi
function subscribe(plan) {
  const formData = new FormData();
  formData.append("plan", plan);

  fetch("/subscribe", {
    method: "POST",
    body: formData
  })
  .then(res => res.json())
  .then(data => alert(data.message));
}
