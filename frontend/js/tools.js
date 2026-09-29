const API_BASE = "http://localhost:8000/api/v1";
let currentPage = 1, deleteTargetId = null;
let toolModal, deleteModal, toast, searchTimer = null;

document.addEventListener("DOMContentLoaded", () => {
  toolModal   = new bootstrap.Modal(document.getElementById("toolModal"));
  deleteModal = new bootstrap.Modal(document.getElementById("deleteModal"));
  toast       = new bootstrap.Toast(document.getElementById("toast"));
  loadTools();
});

function debouncedLoad() {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(() => loadTools(1), 400);
}

async function loadTools(page = 1) {
  currentPage = page;
  const search = document.getElementById("searchInput").value;
  const cat    = document.getElementById("catFilter").value;
  const plat   = document.getElementById("platFilter").value;
  const grid = document.getElementById("gridView");
  grid.innerHTML = `<div class="col-12 text-center py-5">
    <div class="spinner-border text-info"></div></div>`;
  try {
    const params = new URLSearchParams({ page, limit: 12, search,
      category: cat, platform: plat });
    const res = await fetch(`${API_BASE}/tools?${params}`, { headers: authHeaders() });
    if (!res.ok) throw new Error("Gagal memuat tools");
    const data = await res.json();
    renderGrid(data.items || []);
    renderPagination(data.total || 0, data.limit || 12);
  } catch (err) {
    grid.innerHTML = `<div class="col-12 text-center text-danger py-5">
      <i class="bi bi-exclamation-triangle"></i> ${err.message}</div>`;
  }
}

function renderGrid(items) {
  const grid = document.getElementById("gridView");
  if (!items.length) {
    grid.innerHTML = `<div class="col-12 text-center py-5 text-muted">Belum ada tool</div>`;
    return;
  }
  grid.innerHTML = items.map(t => `
    <div class="col-md-6 col-lg-4">
      <div class="tool-card p-3">
        <div class="d-flex align-items-start gap-2 mb-2">
          <i class="bi bi-terminal-fill tool-icon"></i>
          <div class="flex-grow-1">
            <h6 class="mb-0">${t.name}</h6>
            <small class="text-muted">${t.category} • ${t.platform}</small>
          </div>
          ${t.is_open_source ? '<span class="badge bg-success">OSS</span>' : ''}
        </div>
        <p class="small text-muted mb-2" style="min-height:40px">
          ${(t.description || "-").substring(0, 100)}${(t.description||"").length > 100 ? "..." : ""}
        </p>
        ${t.install_cmd ? `<code class="cmd">$ ${t.install_cmd}</code>` : ""}
        <div class="d-flex gap-1 mt-3">
          ${t.homepage ? `<a href="${t.homepage}" target="_blank" class="btn btn-sm btn-outline-info flex-fill">
            <i class="bi bi-box-arrow-up-right"></i> Site</a>` : ""}
          <button class="btn btn-sm btn-outline-warning" onclick='openEditModal(${JSON.stringify(t)})'>
            <i class="bi bi-pencil"></i>
          </button>
          <button class="btn btn-sm btn-outline-danger"
                  onclick="openDeleteModal(${t.id}, '${t.name.replace(/'/g,"\\'")}')">
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
      <a class="page-link" href="#" onclick="loadTools(${i});return false;">${i}</a></li>`;
  }
}

function openCreateModal() {
  document.getElementById("modalTitle").textContent = "Tambah Tool";
  document.getElementById("toolForm").reset();
  document.getElementById("toolId").value = "";
  toolModal.show();
}

function openEditModal(t) {
  document.getElementById("modalTitle").textContent = "Edit Tool";
  document.getElementById("toolId").value        = t.id;
  document.getElementById("toolName").value      = t.name;
  document.getElementById("toolCategory").value  = t.category;
  document.getElementById("toolDesc").value      = t.description || "";
  document.getElementById("toolHome").value      = t.homepage || "";
  document.getElementById("toolPlatform").value  = t.platform;
  document.getElementById("toolInstall").value   = t.install_cmd || "";
  document.getElementById("toolUsage").value     = t.usage_hint || "";
  document.getElementById("toolOpen").checked    = t.is_open_source;
  document.getElementById("toolActive").checked  = t.is_active;
  toolModal.show();
}

async function saveTool() {
  const id = document.getElementById("toolId").value;
  const payload = {
    name:           document.getElementById("toolName").value,
    category:       document.getElementById("toolCategory").value,
    description:    document.getElementById("toolDesc").value,
    homepage:       document.getElementById("toolHome").value || null,
    platform:       document.getElementById("toolPlatform").value,
    install_cmd:    document.getElementById("toolInstall").value || null,
    usage_hint:     document.getElementById("toolUsage").value || null,
    is_open_source: document.getElementById("toolOpen").checked,
    is_active:      document.getElementById("toolActive").checked,
  };
  const method = id ? "PUT" : "POST";
  const url    = id ? `${API_BASE}/tools/${id}` : `${API_BASE}/tools`;
  try {
    const res = await fetch(url, {
      method,
      headers: { "Content-Type": "application/json", ...authHeaders() },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw new Error((await res.json()).detail || "Gagal menyimpan");
    toolModal.hide();
    showToast(id ? "Tool diupdate" : "Tool ditambahkan");
    loadTools(currentPage);
  } catch (err) { showToast(err.message, "danger"); }
}

function openDeleteModal(id, name) {
  deleteTargetId = id;
  document.getElementById("deleteName").textContent = name;
  deleteModal.show();
}

async function confirmDelete() {
  try {
    const res = await fetch(`${API_BASE}/tools/${deleteTargetId}`, {
      method: "DELETE", headers: authHeaders()
    });
    if (!res.ok) throw new Error("Gagal menghapus");
    deleteModal.hide();
    showToast("Tool dihapus");
    loadTools(currentPage);
  } catch (err) { showToast(err.message, "danger"); }
}


function showToast(msg, type = "success") {
  const el = document.getElementById("toast");
  el.className = `toast align-items-center text-bg-${type} border-0`;
  document.getElementById("toastMsg").textContent = msg;
  toast.show();
}
