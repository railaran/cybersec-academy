const API_BASE = "http://localhost:8000/api/v1";
let currentPage = 1, deleteTargetId = null, activeQuiz = null;
let quizModal, deleteModal, attemptModal, toast, searchTimer = null;

document.addEventListener("DOMContentLoaded", () => {
  quizModal    = new bootstrap.Modal(document.getElementById("quizModal"));
  deleteModal  = new bootstrap.Modal(document.getElementById("deleteModal"));
  attemptModal = new bootstrap.Modal(document.getElementById("attemptModal"));
  toast        = new bootstrap.Toast(document.getElementById("toast"));
  loadQuizzes();
});

function debouncedLoad() {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(() => loadQuizzes(1), 400);
}

async function loadQuizzes(page = 1) {
  currentPage = page;
  const search = document.getElementById("searchInput").value;
  const diff   = document.getElementById("diffFilter").value;
  const grid = document.getElementById("gridView");
  grid.innerHTML = `<div class="col-12 text-center py-5">
    <div class="spinner-border text-info"></div></div>`;
  try {
    const params = new URLSearchParams({ page, limit: 9, search, difficulty: diff });
    const res = await fetch(`${API_BASE}/quizzes?${params}`, { headers: authHeaders() });
    if (!res.ok) throw new Error("Gagal memuat quiz");
    const data = await res.json();
    renderGrid(data.items || []);
    renderPagination(data.total || 0, data.limit || 9);
  } catch (err) {
    grid.innerHTML = `<div class="col-12 text-center text-danger py-5">
      <i class="bi bi-exclamation-triangle"></i> ${err.message}</div>`;
  }
}

function renderGrid(items) {
  const grid = document.getElementById("gridView");
  if (!items.length) {
    grid.innerHTML = `<div class="col-12 text-center py-5 text-muted">Belum ada quiz</div>`;
    return;
  }
  grid.innerHTML = items.map(q => `
    <div class="col-md-6 col-lg-4">
      <div class="quiz-card p-3">
        <div class="d-flex justify-content-between align-items-start mb-2">
          <span class="badge diff-${q.difficulty}">${q.difficulty}</span>
          <small class="text-muted"><i class="bi bi-clock"></i> ${q.time_limit_min} min</small>
        </div>
        <h6 class="mb-1"><i class="bi bi-question-circle text-warning"></i> ${q.title}</h6>
        <p class="small text-muted mb-2" style="min-height:40px">
          ${(q.description || "-").substring(0, 90)}${(q.description||"").length > 90 ? "..." : ""}
        </p>
        <div class="d-flex justify-content-between align-items-center mb-2">
          <span class="badge bg-secondary">${q.category}</span>
          <small class="text-muted">Pass: ${q.pass_score}%</small>
        </div>
        <div class="d-flex gap-1">
          <button class="btn btn-sm btn-outline-success flex-fill" onclick="startAttempt(${q.id})">
            <i class="bi bi-play-fill"></i> Mulai
          </button>
          <button class="btn btn-sm btn-outline-info" onclick='openEditModal(${JSON.stringify(q)})'>
            <i class="bi bi-pencil"></i>
          </button>
          <button class="btn btn-sm btn-outline-danger"
                  onclick="openDeleteModal(${q.id}, '${q.title.replace(/'/g,"\\'")}')">
            <i class="bi bi-trash"></i>
          </button>
        </div>
      </div>
    </div>
  `).join("");
}

function renderPagination(total, limit) {
  const pages = Math.ceil(total / limit);
  const ul = document.getElementById("pagination");
  ul.innerHTML = "";
  for (let i = 1; i <= pages; i++) {
    ul.innerHTML += `<li class="page-item ${i === currentPage ? 'active' : ''}">
      <a class="page-link" href="#" onclick="loadQuizzes(${i});return false;">${i}</a></li>`;
  }
}

function openCreateModal() {
  document.getElementById("modalTitle").textContent = "Tambah Quiz";
  document.getElementById("quizForm").reset();
  document.getElementById("quizId").value = "";
  quizModal.show();
}

function openEditModal(q) {
  document.getElementById("modalTitle").textContent = "Edit Quiz";
  document.getElementById("quizId").value       = q.id;
  document.getElementById("quizTitle").value    = q.title;
  document.getElementById("quizDifficulty").value = q.difficulty;
  document.getElementById("quizDesc").value     = q.description || "";
  document.getElementById("quizCategory").value = q.category || "general";
  document.getElementById("quizTime").value     = q.time_limit_min;
  document.getElementById("quizPass").value     = q.pass_score;
  quizModal.show();
}

async function saveQuiz() {
  const id = document.getElementById("quizId").value;
  const payload = {
    title:          document.getElementById("quizTitle").value,
    difficulty:     document.getElementById("quizDifficulty").value,
    description:    document.getElementById("quizDesc").value,
    category:       document.getElementById("quizCategory").value,
    time_limit_min: parseInt(document.getElementById("quizTime").value) || 15,
    pass_score:     parseInt(document.getElementById("quizPass").value) || 70,
  };
  const method = id ? "PUT" : "POST";
  const url    = id ? `${API_BASE}/quizzes/${id}` : `${API_BASE}/quizzes`;
  try {
    const res = await fetch(url, {
      method,
      headers: { "Content-Type": "application/json", ...authHeaders() },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw new Error((await res.json()).detail || "Gagal menyimpan");
    quizModal.hide();
    showToast(id ? "Quiz diupdate" : "Quiz ditambahkan");
    loadQuizzes(currentPage);
  } catch (err) { showToast(err.message, "danger"); }
}

function openDeleteModal(id, name) {
  deleteTargetId = id;
  document.getElementById("deleteName").textContent = name;
  deleteModal.show();
}

async function confirmDelete() {
  try {
    const res = await fetch(`${API_BASE}/quizzes/${deleteTargetId}`, {
      method: "DELETE", headers: authHeaders()
    });
    if (!res.ok) throw new Error("Gagal menghapus");
    deleteModal.hide();
    showToast("Quiz dihapus");
    loadQuizzes(currentPage);
  } catch (err) { showToast(err.message, "danger"); }
}

async function startAttempt(quizId) {
  try {
    const res = await fetch(`${API_BASE}/quizzes/${quizId}`, { headers: authHeaders() });
    if (!res.ok) throw new Error("Gagal memuat quiz");
    activeQuiz = await res.json();

    document.getElementById("attemptTitle").textContent = activeQuiz.title;
    const body = document.getElementById("attemptBody");
    if (!activeQuiz.questions?.length) {
      body.innerHTML = `<p class="text-muted">Quiz ini belum punya pertanyaan.</p>`;
      document.getElementById("submitQuizBtn").disabled = true;
    } else {
      document.getElementById("submitQuizBtn").disabled = false;
      body.innerHTML = activeQuiz.questions.map((q, i) => `
        <div class="mb-3">
          <p class="mb-2"><strong>${i + 1}. ${q.text}</strong>
            <span class="badge bg-secondary">${q.points} poin</span></p>
          ${q.answers.map(a => `
            <label class="answer-row d-block">
              <input type="radio" name="q_${q.id}" value="${a.id}">
              ${a.text}
            </label>
          `).join("")}
        </div>
      `).join("");
    }
    attemptModal.show();
  } catch (err) { showToast(err.message, "danger"); }
}

async function submitAttempt() {
  if (!activeQuiz) return;
  const answers = {};
  activeQuiz.questions.forEach(q => {
    const sel = document.querySelector(`input[name="q_${q.id}"]:checked`);
    if (sel) answers[q.id] = parseInt(sel.value);
  });
  try {
    const res = await fetch(`${API_BASE}/quizzes/${activeQuiz.id}/submit`, {
      method: "POST",
      headers: { "Content-Type": "application/json", ...authHeaders() },
      body: JSON.stringify({ answers })
    });
    const data = await res.json();
    showToast(`Score: ${data.score}% — ${data.passed ? "LULUS" : "GAGAL"}`,
              data.passed ? "success" : "warning");
    attemptModal.hide();
  } catch (err) { showToast(err.message, "danger"); }
}


function showToast(msg, type = "success") {
  const el = document.getElementById("toast");
  el.className = `toast align-items-center text-bg-${type} border-0`;
  document.getElementById("toastMsg").textContent = msg;
  toast.show();
}
