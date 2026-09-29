// Dipanggil di atas setiap halaman (kecuali login.html)
(function guard() {
  const token = localStorage.getItem("access_token");
  const path = window.location.pathname.split("/").pop() || "index.html";
  if (!token && path !== "login.html") {
    window.location.href = "login.html";
  }
})();

function currentUser() {
  try { return JSON.parse(localStorage.getItem("user") || "null"); }
  catch { return null; }
}

function logout() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("user");
  window.location.href = "login.html";
}

function authHeaders() {
  const token = localStorage.getItem("access_token");
  return token ? { "Authorization": `Bearer ${token}` } : {};
}

// Auto logout kalau 401
window.addEventListener("load", () => {
  const origFetch = window.fetch;
  window.fetch = async (...args) => {
    const res = await origFetch(...args);
    if (res.status === 401) {
      const url = String(args[0] || "");
      if (url.includes("/api/")) {
        logout();
      }
    }
    return res;
  };
});
