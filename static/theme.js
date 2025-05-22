// डार्क मोड टॉगल करने का फंक्शन
function toggleDarkMode() {
  const body = document.body;
  body.classList.toggle("dark-mode");

  if (body.classList.contains("dark-mode")) {
    localStorage.setItem("theme", "dark");
  } else {
    localStorage.setItem("theme", "light");
  }
}

// DOM लोड होने के बाद बटन इवेंट और थीम सेट करना
document.addEventListener("DOMContentLoaded", () => {
  // डार्क बटन से थीम बदले
  const darkBtn = document.getElementById("darkBtn");
  if (darkBtn) {
    darkBtn.addEventListener("click", toggleDarkMode);
  }

  // पेज लोड पर थीम लागू करें
  if (localStorage.getItem("theme") === "dark") {
    document.body.classList.add("dark-mode");
  }
});


// kdfjhkgjhdzlkgjl;zdf   upadate dark mode 
function toggleDarkMode() {
  const body = document.body;
  body.classList.toggle("dark-mode");  // body टैग में 'dark-mode' क्लास जोड़ता/हटाता है

  // लोकल स्टोरेज में थीम स्टोर करता है
  localStorage.setItem("theme", body.classList.contains("dark-mode") ? "dark" : "light");
}
document.addEventListener("DOMContentLoaded", () => {
  if (localStorage.getItem("theme") === "dark") {
    document.body.classList.add("dark-mode");
  }
});
