// Frontend app.js - clean single implementation
const apiBase = '';

function showSection(id) {
  document.querySelectorAll('#content > section').forEach(s => s.classList.add('d-none'));
  const el = document.getElementById(id);
  if (el) el.classList.remove('d-none');
}

async function fetchJSON(path, opts) {
  const res = await fetch(apiBase + path, opts);
  if (!res.ok) {
    const txt = await res.text().catch(() => null);
    throw new Error(res.status + ' ' + (txt || res.statusText));
  }
  try { return await res.json(); } catch (e) { return null; }
}

async function getRooms() {
  try { return await fetchJSON('/rooms/'); } catch (e) { console.warn('getRooms', e); return []; }
}

async function refreshRooms() {
  try {
    const rooms = await getRooms();
    const tbody = document.querySelector('#roomsTable tbody'); if (!tbody) return; tbody.innerHTML = '';
    rooms.forEach(r => {
      const tr = document.createElement('tr');
      tr.innerHTML = `<td>${r.room_id}</td><td>${r.room_number}</td><td>${r.room_type}</td><td>$${r.rate}</td><td>${r.is_available}</td>`;
      tbody.appendChild(tr);
    });
  } catch (e) { console.warn('refreshRooms', e); }
}

async function loadRoomsIntoSelect() {
  try {
    const rooms = await getRooms();
    const sel = document.getElementById('roomSelect'); if (!sel) return; sel.innerHTML = '';
    rooms.filter(r => r.is_available).forEach(r => {
      const opt = document.createElement('option'); opt.value = r.room_id; opt.textContent = `${r.room_number} (${r.room_type}) - $${r.rate}`; sel.appendChild(opt);
    });
  } catch (e) { console.warn('loadRoomsIntoSelect', e); }
}

async function refreshDashboard() {
  try {
    const rooms = await getRooms().catch(() => []);
    const avail = rooms.filter(r => r.is_available).length;
    const dashAvail = document.getElementById('dashAvail'); if (dashAvail) dashAvail.textContent = avail;
    let active = '-';
    try { const resp = await fetchJSON('/reservations/'); active = Array.isArray(resp) ? resp.length : '-'; } catch (e) { active = '-'; }
    const dashActive = document.getElementById('dashActive'); if (dashActive) dashActive.textContent = active;
    try { const h = await fetchJSON('/health'); const el = document.getElementById('healthStatus'); if (el) el.innerHTML = `MySQL: <strong>${h.mysql}</strong> &nbsp; Mongo: <strong>${h.mongo}</strong>`; } catch (e) { const el = document.getElementById('healthStatus'); if (el) el.textContent = 'unavailable'; }
  } catch (e) { console.warn('refreshDashboard', e); }
}

function loadStaffDemo() {
  const staff = [ { name: 'Alice Brown', role: 'Manager' }, { name: 'John Doe', role: 'Reception' }, { name: 'Priya Singh', role: 'Housekeeping' } ];
  const el = document.getElementById('staffList'); if (!el) return; el.innerHTML = '';
  staff.forEach(s => { const li = document.createElement('li'); li.className = 'list-group-item'; li.textContent = `${s.name} — ${s.role}`; el.appendChild(li); });
}

window.addEventListener('DOMContentLoaded', () => {
  const mapping = { 'nav-home':'home','nav-book':'book','nav-rooms':'rooms','nav-resv':'reservations','nav-pay':'payments','nav-feedback':'feedback','nav-staff':'staff','nav-dashboard':'dashboard','nav-about':'about','nav-contact':'contact' };
  Object.entries(mapping).forEach(([navId, secId]) => { const el = document.getElementById(navId); if (!el) return; el.addEventListener('click', (e) => { e.preventDefault(); showSection(secId); if (secId === 'book') loadRoomsIntoSelect(); if (secId === 'rooms') refreshRooms(); if (secId === 'dashboard') refreshDashboard(); if (secId === 'staff') loadStaffDemo(); }); });

  // booking
  const bookingForm = document.getElementById('bookingForm'); if (bookingForm) bookingForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = { customer_id: parseInt(document.getElementById('customerId').value), room_id: parseInt(document.getElementById('roomSelect').value), check_in: document.getElementById('checkIn').value, check_out: document.getElementById('checkOut').value };
    const out = document.getElementById('bookingResult');
    try { const j = await fetchJSON('/reservations/', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(payload) }); if (out) out.textContent = JSON.stringify(j); } catch (err) { if (out) out.textContent = 'Error: ' + err.message; }
  });

  // reservations
  const btnLookupResv = document.getElementById('btnLookupResv'); if (btnLookupResv) btnLookupResv.addEventListener('click', async () => {
    const id = document.getElementById('lookupResvId').value; if (!id) return alert('Enter reservation id'); const out = document.getElementById('reservationDetail');
    try { const res = await fetch('/reservations/' + id); if (res.status === 404) { if (out) out.textContent = 'Not found'; return; } const j = await res.json(); if (out) out.textContent = JSON.stringify(j, null, 2); } catch (e) { if (out) out.textContent = 'Error: ' + e.message; }
  });

  const btnCancelResv = document.getElementById('btnCancelResv'); if (btnCancelResv) btnCancelResv.addEventListener('click', async () => {
    const id = document.getElementById('lookupResvId').value; if (!id) return alert('Enter reservation id'); if (!confirm('Cancel reservation ' + id + '?')) return; const out = document.getElementById('reservationDetail');
    try { const res = await fetch('/reservations/' + id + '/cancel', { method: 'POST' }); const j = await res.json(); if (out) out.textContent = JSON.stringify(j, null, 2); } catch (e) { if (out) out.textContent = 'Error: ' + e.message; }
  });

  // payments
  const btnPay = document.getElementById('btnPay'); if (btnPay) btnPay.addEventListener('click', async (e) => {
    e.preventDefault();
    const payload = { reservation_id: parseInt(document.getElementById('payResvId').value), amount: parseFloat(document.getElementById('payAmount').value), method: document.getElementById('payMethod').value };
    try { const j = await fetchJSON('/payments/', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(payload) }); alert('Payment recorded: ' + JSON.stringify(j)); } catch (err) { alert('Payment failed: ' + err.message); }
  });

  const btnListPayments = document.getElementById('btnListPayments'); if (btnListPayments) btnListPayments.addEventListener('click', async () => {
    const id = document.getElementById('listPaymentsResv').value; if (!id) return alert('Enter reservation id'); const out = document.getElementById('paymentsList');
    try { const j = await fetchJSON('/payments/reservation/' + id); if (out) out.textContent = JSON.stringify(j, null, 2); } catch (e) { if (out) out.textContent = 'Error: ' + e.message; }
  });

  // feedback
  const btnFeedback = document.getElementById('btnFeedback'); if (btnFeedback) btnFeedback.addEventListener('click', async (e) => {
    e.preventDefault();
    const payload = { customerId: parseInt(document.getElementById('fbCustomer').value), reservationId: parseInt(document.getElementById('fbReservation').value), roomType: document.getElementById('fbRoomType').value, score: parseInt(document.getElementById('fbScore').value), comment: document.getElementById('fbComment').value };
    const out = document.getElementById('feedbackResult');
    try { const j = await fetchJSON('/reviews/', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(payload) }); if (out) out.textContent = JSON.stringify(j); } catch (e) { if (out) out.textContent = 'Error: ' + e.message; }
  });

  const refreshBtn = document.getElementById('refreshRooms'); if (refreshBtn) refreshBtn.addEventListener('click', refreshRooms);

  // initial
  showSection('home'); loadRoomsIntoSelect(); refreshRooms();
});
