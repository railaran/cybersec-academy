const API_BASE = "http://localhost:8000/api/v1";
let currentPage = 1, deleteTargetId = null, flagLabId = null;
let labModal, deleteModal, flagModal, toast, searchTimer = null;

document.addEventListener("DOMContentLoaded", () => {
  labModal    = new bootstrap.Modal(document.getElementById("labModal"));
  deleteModal = new bootstrap.Modal(document.getElementById("deleteModal"));
  flagModal   = new bootstrap.Modal(document.getElementById("flagModal"));
  toast       = new bootstrap.Toast(document.getElementById("toast"));
  loadLabs();
});

function debouncedLoad() {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(() => loadLabs(1), 400);
}

async function loadLabs(page = 1) {
  currentPage = page;
  const search = document.getElementById("searchInput").value;
  const cat    = document.getElementById("catFilter").value;
  const diff   = document.getElementById("diffFilter").value;

  const grid = document.getElementById("gridView");
  grid.innerHTML = `<div class="col-12 text-center py-5">
    <div class="spinner-border text-info"></div></div>`;

  try {
    const params = new URLSearchParams({ page, limit: 9, search,
      category: cat, difficulty: diff });
    const res = await fetch(`${API_BASE}/labs?${params}`, { headers: authHeaders() });
    if (!res.ok) throw new Error("Gagal memuat labs");
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
    grid.innerHTML = `<div class="col-12 text-center py-5 text-muted">Belum ada lab</div>`;
    return;
  }
  grid.innerHTML = items.map(l => `
    <div class="col-md-6 col-lg-4">
      <div class="lab-card p-3">
        <div class="d-flex justify-content-between align-items-start mb-2">
          <span class="badge diff-${l.difficulty}">${l.difficulty}</span>
          <span class="badge bg-dark border border-secondary">
            <i class="bi bi-star-fill text-warning"></i> ${l.points}
          </span>
        </div>
        <h6 class="mb-1"><i class="bi bi-terminal text-info"></i> ${l.title}</h6>
        <p class="small text-muted mb-2" style="min-height:40px">
          ${(l.description || "-").substring(0, 90)}${(l.description||"").length > 90 ? "..." : ""}
        </p>
        <div class="d-flex justify-content-between align-items-center mb-2">
          <span class="badge bg-secondary">${l.category}</span>
          <small class="text-muted"><i class="bi bi-clock"></i> ${l.time_limit_min} min</small>
        </div>
        <div class="d-flex gap-1">
          <button class="btn btn-sm btn-outline-success flex-fill"
                  onclick="openFlagModal(${l.id}, '${l.title.replace(/'/g,"\\'")}')">
            <i class="bi bi-flag"></i> Flag
          </button>
          <button class="btn btn-sm btn-outline-info"
                  onclick='openEditModal(${JSON.stringify(l)})'>
            <i class="bi bi-pencil"></i>
          </button>
          <button class="btn btn-sm btn-outline-danger"
                  onclick="openDeleteModal(${l.id}, '${l.title.replace(/'/g,"\\'")}')">
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
      <a class="page-link" href="#" onclick="loadLabs(${i});return false;">${i}</a></li>`;
  }
}

function openCreateModal() {
  document.getElementById("modalTitle").textContent = "Tambah Lab";
  document.getElementById("labForm").reset();
  document.getElementById("labId").value = "";
  labModal.show();
}

function openEditModal(l) {
  document.getElementById("modalTitle").textContent = "Edit Lab";
  document.getElementById("labId").value        = l.id;
  document.getElementById("labTitle").value     = l.title;
  document.getElementById("labCategory").value  = l.category;
  document.getElementById("labDesc").value      = l.description || "";
  document.getElementById("labObjective").value = l.objective || "";
  document.getElementById("labDifficulty").value= l.difficulty;
  document.getElementById("labPoints").value    = l.points;
  document.getElementById("labTime").value      = l.time_limit_min;
  document.getElementById("labImage").value     = l.docker_image || "";
  document.getElementById("labFlag").value      = l.flag || "";
  document.getElementById("labActive").checked  = l.is_active;
  labModal.show();
}

async function saveLab() {
  const id = document.getElementById("labId").value;
  const payload = {
    title:          document.getElementById("labTitle").value,
    category:       document.getElementById("labCategory").value,
    description:    document.getElementById("labDesc").value,
    objective:      document.getElementById("labObjective").value,
    difficulty:     document.getElementById("labDifficulty").value,
    points:         parseInt(document.getElementById("labPoints").value) || 100,
    time_limit_min: parseInt(document.getElementById("labTime").value) || 60,
    docker_image:   document.getElementById("labImage").value || null,
    flag:           document.getElementById("labFlag").value || null,
    is_active:      document.getElementById("labActive").checked,
  };
  const method = id ? "PUT" : "POST";
  const url    = id ? `${API_BASE}/labs/${id}` : `${API_BASE}/labs`;
  try {
    const res = await fetch(url, {
      method,
      headers: { "Content-Type": "application/json", ...authHeaders() },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw new Error((await res.json()).detail || "Gagal menyimpan");
    labModal.hide();
    showToast(id ? "Lab diupdate" : "Lab ditambahkan");
    loadLabs(currentPage);
  } catch (err) { showToast(err.message, "danger"); }
}

function openDeleteModal(id, name) {
  deleteTargetId = id;
  document.getElementById("deleteName").textContent = name;
  deleteModal.show();
}

async function confirmDelete() {
  try {
    const res = await fetch(`${API_BASE}/labs/${deleteTargetId}`, {
      method: "DELETE", headers: authHeaders()
    });
    if (!res.ok) throw new Error("Gagal menghapus");
    deleteModal.hide();
    showToast("Lab dihapus");
    loadLabs(currentPage);
  } catch (err) { showToast(err.message, "danger"); }
}

function openFlagModal(id, name) {
  flagLabId = id;
  document.getElementById("flagLabName").textContent = name;
  document.getElementById("flagInput").value = "";
  document.getElementById("flagResult").innerHTML = "";
  flagModal.show();
}

async function submitFlag() {
  const flag = document.getElementById("flagInput").value;
  const result = document.getElementById("flagResult");
  try {
    const res = await fetch(`${API_BASE}/labs/${flagLabId}/submit`, {
      method: "POST",
      headers: { "Content-Type": "application/json", ...authHeaders() },
      body: JSON.stringify({ flag })
    });
    const data = await res.json();
    result.innerHTML = data.correct
      ? `<span class="text-success"><i class="bi bi-check-circle"></i> ${data.message} (+${data.points})</span>`
      : `<span class="text-danger"><i class="bi bi-x-circle"></i> ${data.message}</span>`;
  } catch (err) {
    result.innerHTML = `<span class="text-danger">${err.message}</span>`;
  }
}


function showToast(msg, type = "success") {
  const el = document.getElementById("toast");
  el.className = `toast align-items-center text-bg-${type} border-0`;
  document.getElementById("toastMsg").textContent = msg;
  toast.show();
}
