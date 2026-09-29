const API_BASE = "http://localhost:8000/api/v1";
let toast;

document.addEventListener("DOMContentLoaded", () => {
  toast = new bootstrap.Toast(document.getElementById("toast"));
  loadAll();
});

async function loadAll() {
  await Promise.all([loadStats(), loadRecent()]);
}

async function loadStats() {
  try {
    const res = await fetch(`${API_BASE}/dashboard/stats`, { headers: authHeaders() });
    if (!res.ok) throw new Error("Gagal memuat stats");
    const s = await res.json();
    document.getElementById("statUsers").textContent   = s.users;
    document.getElementById("statCourses").textContent = s.courses;
    document.getElementById("statLabs").textContent    = s.labs;
    document.getElementById("statQuizzes").textContent = s.quizzes;
    document.getElementById("statTools").textContent   = s.tools;
    document.getElementById("statEvents").textContent  = s.events;
  } catch (err) {
    showToast(err.message, "danger");
  }
}

async function loadRecent() {
  try {
    const res = await fetch(`${API_BASE}/dashboard/recent`, { headers: authHeaders() });
    if (!res.ok) throw new Error("Gagal memuat recent");
    const data = await res.json();
    fill("recentCourses", data.courses);
    fill("recentLabs",    data.labs);
    fill("recentQuizzes", data.quizzes);
    fill("recentTools",   data.tools);
    fill("recentEvents",  data.events);
  } catch (err) {
    showToast(err.message, "danger");
  }
}

function fill(id, items) {
  const ul = document.getElementById(id);
  if (!items || !items.length) {
    ul.innerHTML = `<li class="text-muted">Belum ada data</li>`;
    return;
  }
  ul.innerHTML = items.map(x =>
    `<li><i class="bi bi-dot"></i> ${x.title || "(tanpa judul)"}</li>`
  ).join("");
}


function showToast(msg, type = "success") {
  const el = document.getElementById("toast");
  el.className = `toast align-items-center text-bg-${type} border-0`;
  document.getElementById("toastMsg").textContent = msg;
  toast.show();
}
