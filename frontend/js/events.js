const API_BASE = "http://localhost:8000/api/v1";
let currentPage = 1, deleteTargetId = null;
let eventModal, deleteModal, toast, searchTimer = null;

document.addEventListener("DOMContentLoaded", () => {
  eventModal  = new bootstrap.Modal(document.getElementById("eventModal"));
  deleteModal = new bootstrap.Modal(document.getElementById("deleteModal"));
  toast       = new bootstrap.Toast(document.getElementById("toast"));
  loadEvents();
});

function debouncedLoad() {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(() => loadEvents(1), 400);
}

async function loadEvents(page = 1) {
  currentPage = page;
  const search = document.getElementById("searchInput").value;
  const type   = document.getElementById("typeFilter").value;
  const status = document.getElementById("statusFilter").value;
  const grid = document.getElementById("gridView");
  grid.innerHTML = `<div class="col-12 text-center py-5">
    <div class="spinner-border text-info"></div></div>`;
  try {
    const params = new URLSearchParams({ page, limit: 9, search, type, status });
    const res = await fetch(`${API_BASE}/events?${params}`, { headers: authHeaders() });
    if (!res.ok) throw new Error("Gagal memuat events");
    const data = await res.json();
    renderGrid(data.items || []);
    renderPagination(data.total || 0, data.limit || 9);
  } catch (err) {
    grid.innerHTML = `<div class="col-12 text-center text-danger py-5">
      <i class="bi bi-exclamation-triangle"></i> ${err.message}</div>`;
  }
}

function fmtDate(iso) {
  if (!iso) return "-";
  return new Date(iso).toLocaleString("id-ID", { dateStyle: "medium", timeStyle: "short" });
}

function renderGrid(items) {
  const grid = document.getElementById("gridView");
  if (!items.length) {
    grid.innerHTML = `<div class="col-12 text-center py-5 text-muted">Belum ada event</div>`;
    return;
  }
  grid.innerHTML = items.map(e => `
    <div class="col-md-6 col-lg-4">
      <div class="event-card">
        ${e.cover_url
          ? `<img src="${e.cover_url}" style="height:140px;width:100%;object-fit:cover">`
          : `<div class="event-cover"><i class="bi bi-calendar-event"></i></div>`}
        <div class="p-3">
          <div class="d-flex justify-content-between mb-2">
            <span class="badge event-type-${e.type}">${e.type.toUpperCase()}</span>
            <span class="badge ${e.is_published ? 'bg-success' : 'bg-secondary'}">
              ${e.is_published ? 'Published' : 'Draft'}
            </span>
          </div>
          <h6 class="mb-1">${e.title}</h6>
          <p class="small text-muted mb-2" style="min-height:40px">
            ${(e.description || "-").substring(0, 90)}${(e.description||"").length > 90 ? "..." : ""}
          </p>
          <div class="small text-muted mb-2">
            <div><i class="bi bi-geo-alt"></i> ${e.location || "-"}</div>
            <div><i class="bi bi-clock"></i> ${fmtDate(e.start_at)}</div>
            ${e.capacity > 0 ? `<div><i class="bi bi-people"></i> Kuota ${e.capacity}</div>` : ""}
            <div><i class="bi bi-tag"></i> ${e.is_free ? "Gratis" : "Rp " + e.price.toLocaleString("id-ID")}</div>
          </div>
          <div class="d-flex gap-1">
            <button class="btn btn-sm btn-outline-success flex-fill" onclick="registerEvent(${e.id})">
              <i class="bi bi-check-circle"></i> Daftar
            </button>
            <button class="btn btn-sm btn-outline-info" onclick='openEditModal(${JSON.stringify(e)})'>
              <i class="bi bi-pencil"></i>
            </button>
            <button class="btn btn-sm btn-outline-danger"
                    onclick="openDeleteModal(${e.id}, '${e.title.replace(/'/g,"\\'")}')">
              <i class="bi bi-trash"></i>
            </button>
          </div>
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
      <a class="page-link" href="#" onclick="loadEvents(${i});return false;">${i}</a></li>`;
  }
}

function toLocalInput(iso) {
  if (!iso) return "";
  const d = new Date(iso);
  const pad = n => String(n).padStart(2, "0");
  return `${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`;
}

function openCreateModal() {
  document.getElementById("modalTitle").textContent = "Tambah Event";
  document.getElementById("eventForm").reset();
  document.getElementById("eventId").value = "";
  eventModal.show();
}

function openEditModal(e) {
  document.getElementById("modalTitle").textContent = "Edit Event";
  document.getElementById("eventId").value         = e.id;
  document.getElementById("eventTitle").value      = e.title;
  document.getElementById("eventType").value       = e.type;
  document.getElementById("eventDesc").value       = e.description || "";
  document.getElementById("eventLocation").value   = e.location || "";
  document.getElementById("eventStart").value      = toLocalInput(e.start_at);
  document.getElementById("eventEnd").value        = toLocalInput(e.end_at);
  document.getElementById("eventCapacity").value   = e.capacity || 0;
  document.getElementById("eventPrice").value      = e.price || 0;
  document.getElementById("eventFree").checked     = e.is_free;
  document.getElementById("eventCover").value      = e.cover_url || "";
  document.getElementById("eventPublished").checked= e.is_published;
  eventModal.show();
}

async function saveEvent() {
  const id = document.getElementById("eventId").value;
  const payload = {
    title:        document.getElementById("eventTitle").value,
    type:         document.getElementById("eventType").value,
    description:  document.getElementById("eventDesc").value,
    location:     document.getElementById("eventLocation").value || null,
    start_at:     document.getElementById("eventStart").value || null,
    end_at:       document.getElementById("eventEnd").value || null,
    capacity:     parseInt(document.getElementById("eventCapacity").value) || 0,
    price:        parseInt(document.getElementById("eventPrice").value) || 0,
    is_free:      document.getElementById("eventFree").checked,
    cover_url:    document.getElementById("eventCover").value || null,
    is_published: document.getElementById("eventPublished").checked,
  };
  const method = id ? "PUT" : "POST";
  const url    = id ? `${API_BASE}/events/${id}` : `${API_BASE}/events`;
  try {
    const res = await fetch(url, {
      method,
      headers: { "Content-Type": "application/json", ...authHeaders() },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw new Error((await res.json()).detail || "Gagal menyimpan");
    eventModal.hide();
    showToast(id ? "Event diupdate" : "Event ditambahkan");
    loadEvents(currentPage);
  } catch (err) { showToast(err.message, "danger"); }
}

function openDeleteModal(id, name) {
  deleteTargetId = id;
  document.getElementById("deleteName").textContent = name;
  deleteModal.show();
}

async function confirmDelete() {
  try {
    const res = await fetch(`${API_BASE}/events/${deleteTargetId}`, {
      method: "DELETE", headers: authHeaders()
    });
    if (!res.ok) throw new Error("Gagal menghapus");
    deleteModal.hide();
    showToast("Event dihapus");
    loadEvents(currentPage);
  } catch (err) { showToast(err.message, "danger"); }
}

async function registerEvent(id) {
  try {
    const res = await fetch(`${API_BASE}/events/${id}/register`, {
      method: "POST", headers: authHeaders()
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Gagal mendaftar");
    showToast("Berhasil mendaftar event!");
  } catch (err) { showToast(err.message, "danger"); }
}


function showToast(msg, type = "success") {
  const el = document.getElementById("toast");
  el.className = `toast align-items-center text-bg-${type} border-0`;
  document.getElementById("toastMsg").textContent = msg;
  toast.show();
}
