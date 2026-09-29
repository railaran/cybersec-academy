const API_BASE = "http://localhost:8000/api/v1";
let currentPage = 1;
let deleteTargetId = null;
let userModal, deleteModal, toast;

document.addEventListener("DOMContentLoaded", () => {
  userModal   = new bootstrap.Modal(document.getElementById("userModal"));
  deleteModal = new bootstrap.Modal(document.getElementById("deleteModal"));
  toast       = new bootstrap.Toast(document.getElementById("toast"));
  loadUsers();
});

async function loadUsers(page = 1) {
  currentPage = page;
  const search = document.getElementById("searchInput").value;
  const role   = document.getElementById("roleFilter").value;
  const tbody  = document.getElementById("userTable");
  tbody.innerHTML = `<tr><td colspan="6" class="text-center py-4">
    <div class="spinner-border spinner-border-sm"></div> Loading...
  </td></tr>`;
  try {
    const params = new URLSearchParams({ page, limit: 10, search, role });
    const res  = await fetch(`${API_BASE}/users?${params}`, { headers: authHeaders() });
    if (!res.ok) throw new Error("Gagal memuat data");
    const data = await res.json();
    renderTable(data.items || []);
    renderPagination(data.total || 0, data.limit || 10);
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="6" class="text-center text-danger py-4">
      <i class="bi bi-exclamation-triangle"></i> ${err.message}
    </td></tr>`;
  }
}

function renderTable(users) {
  const tbody = document.getElementById("userTable");
  if (!users.length) {
    tbody.innerHTML = `<tr><td colspan="6" class="text-center py-4 text-muted">
      Tidak ada data user
    </td></tr>`;
    return;
  }
  tbody.innerHTML = users.map((u, i) => `
    <tr>
      <td>${(currentPage - 1) * 10 + i + 1}</td>
      <td><i class="bi bi-person-circle"></i> ${u.full_name || u.username}</td>
      <td>${u.email}</td>
      <td><span class="badge badge-${u.role}">${u.role}</span></td>
      <td><span class="badge ${u.is_active ? 'bg-success' : 'bg-secondary'}">
        ${u.is_active ? 'Aktif' : 'Nonaktif'}</span></td>
      <td>
        <button class="btn btn-sm btn-outline-info" onclick='openEditModal(${JSON.stringify(u)})'>
          <i class="bi bi-pencil"></i>
        </button>
        <button class="btn btn-sm btn-outline-danger"
                onclick="openDeleteModal(${u.id}, '${u.full_name || u.username}')">
          <i class="bi bi-trash"></i>
        </button>
      </td>
    </tr>
  `).join("");
}

function renderPagination(total, limit) {
  const pages = Math.ceil(total / limit);
  const ul = document.getElementById("pagination");
  ul.innerHTML = "";
  for (let i = 1; i <= pages; i++) {
    ul.innerHTML += `<li class="page-item ${i === currentPage ? 'active' : ''}">
      <a class="page-link" href="#" onclick="loadUsers(${i});return false;">${i}</a></li>`;
  }
}

function openCreateModal() {
  document.getElementById("modalTitle").textContent = "Tambah User";
  document.getElementById("userForm").reset();
  document.getElementById("userId").value = "";
  userModal.show();
}

function openEditModal(user) {
  document.getElementById("modalTitle").textContent = "Edit User";
  document.getElementById("userId").value       = user.id;
  document.getElementById("userName").value     = user.full_name || user.username;
  document.getElementById("userEmail").value    = user.email;
  document.getElementById("userPassword").value = "";
  document.getElementById("userRole").value     = user.role;
  document.getElementById("userActive").checked = user.is_active;
  userModal.show();
}

async function saveUser() {
  const id = document.getElementById("userId").value;
  const payload = {
    full_name: document.getElementById("userName").value,
    email:     document.getElementById("userEmail").value,
    role:      document.getElementById("userRole").value,
    is_active: document.getElementById("userActive").checked,
  };
  const password = document.getElementById("userPassword").value;
  if (password) payload.password = password;
  const method = id ? "PUT" : "POST";
  const url    = id ? `${API_BASE}/users/${id}` : `${API_BASE}/users`;
  try {
    const res = await fetch(url, {
      method,
      headers: { "Content-Type": "application/json", ...authHeaders() },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw new Error((await res.json()).detail || "Gagal menyimpan");
    userModal.hide();
    showToast(id ? "User berhasil diupdate" : "User berhasil ditambahkan");
    loadUsers(currentPage);
  } catch (err) { showToast(err.message, "danger"); }
}

function openDeleteModal(id, name) {
  deleteTargetId = id;
  document.getElementById("deleteName").textContent = name;
  deleteModal.show();
}

async function confirmDelete() {
  try {
    const res = await fetch(`${API_BASE}/users/${deleteTargetId}`, {
      method: "DELETE", headers: authHeaders()
    });
    if (!res.ok) throw new Error("Gagal menghapus user");
    deleteModal.hide();
    showToast("User berhasil dihapus");
    loadUsers(currentPage);
  } catch (err) { showToast(err.message, "danger"); }
}


function showToast(msg, type = "success") {
  const el = document.getElementById("toast");
  el.className = `toast align-items-center text-bg-${type} border-0`;
  document.getElementById("toastMsg").textContent = msg;
  toast.show();
}
