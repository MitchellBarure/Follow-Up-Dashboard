/*
app.js
This script handles all the frontend logic for the Follow-up Dashboard by:
1. Dynamically filling in the records table
2. Enabling users to filter through and update records
3. Validating user input and providing error messages
*/

const API_BASE = "http://localhost:8080"; // change to your domain when deployed

let allRecords = [];

// DOM elements
const statusMessageEl = document.getElementById("statusMessage");
const tableBodyEl = document.getElementById("recordsTableBody");
const searchInputEl = document.getElementById("searchInput");
const statusFilterEl = document.getElementById("statusFilter");
const categoryFilterEl = document.getElementById("categoryFilter");
const clearFiltersBtn = document.getElementById("clearFiltersBtn");

const selectedIdEl = document.getElementById("selectedId");
const updateStatusEl = document.getElementById("updateStatus");
const updateNotesEl = document.getElementById("updateNotes");
const updateFormEl = document.getElementById("updateForm");

// Helpers
function setStatusMessage(text, type = "") {
    statusMessageEl.textContent = text || "";
    statusMessageEl.className = "status-message"; // reset
    if (type) {
        statusMessageEl.classList.add(type);
    }
}

function fetchRecords() {
    setStatusMessage("Loading records...", "");
    fetch(`${API_BASE}/api/records`)
        .then((res) => {
            if (!res.ok) {
                throw new Error(`Failed to load records (HTTP ${res.status})`);
            }
            return res.json();
        })
        .then((data) => {
            allRecords = Array.isArray(data) ? data : [];
            renderTable();
            setStatusMessage(`Loaded ${allRecords.length} records.`, "success");
        })
        .catch((err) => {
            console.error(err);
            setStatusMessage("Error loading records. Please try again.", "error");
        });
}
// Helper function to normalize text to ensure small differences don't break the filtering
function normalizeValue(str) {
    return (str || "")
        .toString()
        .trim()
        .toLowerCase()
        .replace(/[\s_]+/g, "");
}

function renderTable() {
    const searchTerm = (searchInputEl.value || "").toLowerCase().trim();

    //Normalize the filter values
    const statusFilter = normalizeValue(statusFilterEl.value);
    const categoryFilter = normalizeValue(categoryFilterEl.value);

    const filtered = allRecords.filter((record) => {
        // Search by name/phone number
        const matchesSearch =
            !searchTerm ||
            (record.Name && record.Name.toLowerCase().includes(searchTerm)) ||
            (record.Phone && record.Phone.toLowerCase().includes(searchTerm));

        //Normalize the record fields
        const recordStatus = normalizeValue(record.Status);
        const recordCategory = normalizeValue(record.Category);

        // Filter by the status & category of the records
        const matchesStatus =
            !statusFilter || recordStatus === statusFilter;

        const matchesCategory =
            !categoryFilter || recordCategory === categoryFilter;

        return matchesSearch && matchesStatus && matchesCategory;
    });

    tableBodyEl.innerHTML = "";

    if (filtered.length === 0) {
        const row = document.createElement("tr");
        const cell = document.createElement("td");
        cell.colSpan = 9;
        cell.textContent = "No records found.";
        row.appendChild(cell);
        tableBodyEl.appendChild(row);
        return;
    }

    filtered.forEach((record) => {
        const tr = document.createElement("tr");

        tr.innerHTML = `
      <td>${record.id || ""}</td>
      <td>${record.Name || ""}</td>
      <td>${record.Phone || ""}</td>
      <td>${record.AssignedTo || ""}</td>
      <td>${record.Category || ""}</td>
      <td>${record.Status || ""}</td>
      <td>${record.LastUpdated || ""}</td>
      <td>${record.Notes || ""}</td>
      <td><button class="action-btn" data-id="${record.id}">Select</button></td>
    `;

        tableBodyEl.appendChild(tr);
    });
}


function handleSelectClick(event) {
    const btn = event.target.closest(".action-btn");
    if (!btn) return;

    const id = btn.getAttribute("data-id");
    const record = allRecords.find((r) => r.id === id);
    if (!record) {
        setStatusMessage("Selected record could not be found in memory.", "error");
        return;
    }

    // Fill the update panel
    selectedIdEl.value = record.id || "";
    updateStatusEl.value = record.Status || "";
    updateNotesEl.value = record.Notes || "";

    setStatusMessage(`Selected record ${record.id} for update.`, "success");
}

function handleUpdateSubmit(event) {
    event.preventDefault();

    const recordId = selectedIdEl.value;
    const newStatus = updateStatusEl.value;
    const newNotes = updateNotesEl.value || "";

    if (!recordId) {
        setStatusMessage("Please select a record from the table first.", "error");
        return;
    }

    if (!newStatus) {
        setStatusMessage("Please choose a new status.", "error");
        return;
    }

    // Updated notes validation
    if (newNotes.length > 500) {
        setStatusMessage("Notes are too long (max 500 characters).", "error");
        return;
    }

    const body = {
        status: newStatus,
        notes: newNotes,
    };

    setStatusMessage(`Updating record ${recordId}...`, "");

    fetch(`${API_BASE}/api/records/${encodeURIComponent(recordId)}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
    })
        .then((res) => res.json().then((data) => ({ ok: res.ok, status: res.status, data })))
        .then(({ ok, status, data }) => {
            if (!ok) {
                const msg = data && data.error ? data.error : `Update failed (HTTP ${status})`;
                throw new Error(msg);
            }

            setStatusMessage("Record updated successfully.", "success");

            // Refresh records from backend so we see latest data + timestamp
            fetchRecords();
        })
        .catch((err) => {
            console.error(err);
            setStatusMessage(`Error updating record: ${err.message}`, "error");
        });
}

function clearFilters() {
    searchInputEl.value = "";
    statusFilterEl.value = "";
    categoryFilterEl.value = "";
    renderTable();
}

// Event listeners
searchInputEl.addEventListener("input", () => {
    renderTable();
});

statusFilterEl.addEventListener("change", () => {
    renderTable();
});

categoryFilterEl.addEventListener("change", () => {
    renderTable();
});

clearFiltersBtn.addEventListener("click", () => {
    clearFilters();
});

tableBodyEl.addEventListener("click", handleSelectClick);
updateFormEl.addEventListener("submit", handleUpdateSubmit);

// Initial load
document.addEventListener("DOMContentLoaded", () => {
    fetchRecords();
});
