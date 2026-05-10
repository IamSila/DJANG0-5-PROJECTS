
// Get CSRF token for Django
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

// Export Modal Functionality
const exportModal = document.getElementById('exportModal');
const exportForm = document.getElementById('exportForm');
const cancelExportBtn = document.getElementById('cancelExportBtn');
const exportMembersBtn = document.getElementById('exportMembersBtn');

// Open modal when export button is clicked
if (exportMembersBtn) {
    exportMembersBtn.addEventListener('click', function(e) {
        e.preventDefault();
        if (exportModal) {
            exportModal.style.display = 'flex';
        }
    });
}

// Close modal function
function closeExportModal() {
    if (exportModal) {
        exportModal.style.display = 'none';
        if (exportForm) {
            exportForm.reset();
        }
    }
}

// Close modal when cancel button is clicked
if (cancelExportBtn) {
    cancelExportBtn.addEventListener('click', closeExportModal);
}

// Close modal when clicking close button
const modalCloseBtn = exportModal?.querySelector('.close-modal');
if (modalCloseBtn) {
    modalCloseBtn.addEventListener('click', closeExportModal);
}

// Close modal when clicking outside
window.addEventListener('click', function(event) {
    if (event.target === exportModal) {
        closeExportModal();
    }
});

// Handle form submission
if (exportForm) {
    exportForm.addEventListener('submit', function(e) {
        const formatSelect = document.getElementById('id_format');
        const selectedFormat = formatSelect?.value;
        
        if (!selectedFormat) {
            e.preventDefault();
            alert('Please select a format');
            return;
        }
        
        // Show loading state on the submit button
        const submitBtn = this.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = 'Processing...';
        submitBtn.disabled = true;
        
        // Close modal immediately
        closeExportModal();
        
        // Re-enable button after form submission
        setTimeout(() => {
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        }, 2000);
    });
}

// Select all functionality
const selectAllCheckbox = document.getElementById('selectAllMembers');
if (selectAllCheckbox) {
    selectAllCheckbox.addEventListener('change', function() {
        const checkboxes = document.querySelectorAll('.member-checkbox');
        checkboxes.forEach(cb => {
            cb.checked = this.checked;
        });
    });
}

// Search functionality
const searchInput = document.getElementById('searchMembers');
if (searchInput) {
    searchInput.addEventListener('keyup', function() {
        const searchText = this.value.toLowerCase();
        const tableRows = document.querySelectorAll('#membersTableBody tr');
        
        tableRows.forEach(row => {
            const text = row.textContent.toLowerCase();
            if (text.includes(searchText)) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    });
}

// Quick download function
function downloadMembers(format) {
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = "{% url 'export_members' %}";
    
    const csrfInput = document.createElement('input');
    csrfInput.type = 'hidden';
    csrfInput.name = 'csrfmiddlewaretoken';
    csrfInput.value = csrftoken;
    form.appendChild(csrfInput);
    
    const formatInput = document.createElement('input');
    formatInput.type = 'hidden';
    formatInput.name = 'format';
    formatInput.value = format;
    form.appendChild(formatInput);
    
    document.body.appendChild(form);
    form.submit();
    document.body.removeChild(form);
}

// Make functions globally available
window.closeExportModal = closeExportModal;
window.downloadMembers = downloadMembers;





// Import Members form
document.addEventListener('DOMContentLoaded', function() {
    const uploadBtn = document.getElementById('uploadMembersBtn');
    const importModal = document.getElementById('importModal');
    const cancelBtn = document.getElementById('cancelImportBtn');
    
    // Open modal when upload button is clicked
    if (uploadBtn) {
        uploadBtn.addEventListener('click', function() {
            importModal.style.display = 'flex';
        });
    }
    
    // Close modal on cancel
    if (cancelBtn) {
        cancelBtn.addEventListener('click', function() {
            importModal.style.display = 'none';
        });
    }
    
    // Close modal on X button
    const closeBtn = importModal?.querySelector('.close');
    if (closeBtn) {
        closeBtn.addEventListener('click', function() {
            importModal.style.display = 'none';
        });
    }
    
    // Close modal when clicking outside
    window.addEventListener('click', function(event) {
        if (event.target === importModal) {
            importModal.style.display = 'none';
        }
    });
});