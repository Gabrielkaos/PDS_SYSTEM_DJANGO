
document.addEventListener('DOMContentLoaded', function() {
    const selectAllCheckbox = document.getElementById('selectAllCheckbox');
    const formCheckboxes = document.querySelectorAll('.form-select-checkbox');
    const bulkActionsBar = document.getElementById('bulkActionsBar');
    const selectedCountSpan = document.getElementById('selectedCount');
    const bulkExportBtn = document.getElementById('bulkExportBtn');
    const bulkDeleteBtn = document.getElementById('bulkDeleteBtn');
    const cancelBulkBtn = document.getElementById('cancelBulkBtn');
    
    
    function updateBulkActionsBar() {
        const selectedCheckboxes = document.querySelectorAll('.form-select-checkbox:checked');
        const count = selectedCheckboxes.length;
        
        if (count > 0) {
            bulkActionsBar.style.display = 'flex';
            selectedCountSpan.textContent = count;
        } else {
            bulkActionsBar.style.display = 'none';
            selectAllCheckbox.checked = false;
        }
    }
    
    
    if (selectAllCheckbox) {
        selectAllCheckbox.addEventListener('change', function() {
            formCheckboxes.forEach(checkbox => {
                checkbox.checked = this.checked;
            });
            updateBulkActionsBar();
        });
    }
    
    
    formCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            updateBulkActionsBar();
            
            
            const allChecked = Array.from(formCheckboxes).every(cb => cb.checked);
            if (selectAllCheckbox) {
                selectAllCheckbox.checked = allChecked;
            }
        });
    });
    
   
    if (bulkExportBtn) {
        bulkExportBtn.addEventListener('click', function() {
            const selectedIds = Array.from(document.querySelectorAll('.form-select-checkbox:checked'))
                .map(cb => cb.dataset.formId);
            
            if (selectedIds.length === 0) {
                alert('Please select at least one form');
                return;
            }
            
            
            const params = new URLSearchParams();
            selectedIds.forEach(id => params.append('form_ids', id));
            
            window.location.href = `/bulk-export/?${params.toString()}`;
        });
    }
    
    
    if (bulkDeleteBtn) {
        bulkDeleteBtn.addEventListener('click', function() {
            const selectedIds = Array.from(document.querySelectorAll('.form-select-checkbox:checked'))
                .map(cb => cb.dataset.formId);
            
            if (selectedIds.length === 0) {
                alert('Please select at least one form');
                return;
            }
            
            const confirmed = confirm(`Are you sure you want to delete ${selectedIds.length} form(s)? This action cannot be undone.`);
            
            if (confirmed) {
                const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
                
                fetch('/bulk-delete/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken
                    },
                    body: JSON.stringify({ form_ids: selectedIds })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert(data.message);
                        window.location.reload();
                    } else {
                        alert('Error: ' + data.message);
                    }
                })
                .catch(error => {
                    alert('An error occurred: ' + error);
                });
            }
        });
    }
    
    if (cancelBulkBtn) {
        cancelBulkBtn.addEventListener('click', function() {
            formCheckboxes.forEach(checkbox => {
                checkbox.checked = false;
            });
            if (selectAllCheckbox) {
                selectAllCheckbox.checked = false;
            }
            updateBulkActionsBar();
        });
    }
});