// Quotation Webhook Handler - Frontend JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips if Bootstrap tooltips are available
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    // Auto-refresh functionality (optional)
    const autoRefreshCheckbox = document.getElementById('auto-refresh');
    let refreshInterval;

    if (autoRefreshCheckbox) {
        autoRefreshCheckbox.addEventListener('change', function() {
            if (this.checked) {
                refreshInterval = setInterval(function() {
                    window.location.reload();
                }, 30000); // Refresh every 30 seconds
            } else {
                clearInterval(refreshInterval);
            }
        });
    }

    // Search functionality enhancements
    const searchInput = document.getElementById('search');
    const customerInput = document.getElementById('customer');

    if (searchInput) {
        // Add search on Enter key press
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                document.querySelector('form').submit();
            }
        });
    }

    if (customerInput) {
        // Add customer filter on Enter key press
        customerInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                document.querySelector('form').submit();
            }
        });
    }

    // Copy to clipboard functionality for code blocks
    const codeBlocks = document.querySelectorAll('pre code');
    codeBlocks.forEach(function(codeBlock) {
        const pre = codeBlock.parentElement;
        const copyButton = document.createElement('button');
        copyButton.className = 'btn btn-sm btn-outline-secondary position-absolute top-0 end-0 m-2';
        copyButton.innerHTML = '<i class="fas fa-copy"></i>';
        copyButton.title = 'Copy to clipboard';
        
        // Make the pre element relative positioned
        pre.style.position = 'relative';
        pre.appendChild(copyButton);

        copyButton.addEventListener('click', function() {
            navigator.clipboard.writeText(codeBlock.textContent).then(function() {
                copyButton.innerHTML = '<i class="fas fa-check"></i>';
                copyButton.classList.replace('btn-outline-secondary', 'btn-success');
                
                setTimeout(function() {
                    copyButton.innerHTML = '<i class="fas fa-copy"></i>';
                    copyButton.classList.replace('btn-success', 'btn-outline-secondary');
                }, 2000);
            }).catch(function(err) {
                console.error('Failed to copy text: ', err);
                copyButton.innerHTML = '<i class="fas fa-times"></i>';
                copyButton.classList.replace('btn-outline-secondary', 'btn-danger');
                
                setTimeout(function() {
                    copyButton.innerHTML = '<i class="fas fa-copy"></i>';
                    copyButton.classList.replace('btn-danger', 'btn-outline-secondary');
                }, 2000);
            });
        });
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Form validation feedback
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // Add loading state to submit buttons
            const submitButton = form.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.disabled = true;
                const originalText = submitButton.innerHTML;
                submitButton.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Loading...';
                
                // Re-enable after a delay (in case of client-side form processing)
                setTimeout(function() {
                    submitButton.disabled = false;
                    submitButton.innerHTML = originalText;
                }, 3000);
            }
        });
    });

    // Table sorting functionality (if needed)
    const sortableHeaders = document.querySelectorAll('th[data-sort]');
    sortableHeaders.forEach(header => {
        header.style.cursor = 'pointer';
        header.addEventListener('click', function() {
            const table = this.closest('table');
            const tbody = table.querySelector('tbody');
            const rows = Array.from(tbody.querySelectorAll('tr'));
            const column = this.getAttribute('data-sort');
            const isAscending = this.getAttribute('data-order') !== 'asc';
            
            // Sort rows
            rows.sort((a, b) => {
                const aValue = a.querySelector(`td[data-${column}]`).textContent;
                const bValue = b.querySelector(`td[data-${column}]`).textContent;
                
                if (isAscending) {
                    return aValue.localeCompare(bValue);
                } else {
                    return bValue.localeCompare(aValue);
                }
            });
            
            // Update DOM
            rows.forEach(row => tbody.appendChild(row));
            
            // Update sort indicator
            this.setAttribute('data-order', isAscending ? 'asc' : 'desc');
            
            // Update visual indicator
            sortableHeaders.forEach(h => h.classList.remove('sort-asc', 'sort-desc'));
            this.classList.add(isAscending ? 'sort-asc' : 'sort-desc');
        });
    });

    // Real-time status updates (optional enhancement)
    function updateStatus() {
        fetch('/health')
            .then(response => response.json())
            .then(data => {
                const statusElements = document.querySelectorAll('.status-indicator');
                statusElements.forEach(element => {
                    if (data.status === 'healthy') {
                        element.className = 'status-indicator status-healthy';
                        element.innerHTML = '<i class="fas fa-check-circle"></i> Healthy';
                    } else {
                        element.className = 'status-indicator status-error';
                        element.innerHTML = '<i class="fas fa-exclamation-circle"></i> Error';
                    }
                });
            })
            .catch(error => {
                console.error('Status check failed:', error);
            });
    }

    // Update status every 30 seconds (optional)
    // setInterval(updateStatus, 30000);
    // updateStatus(); // Initial status check
});

// Utility functions
function formatDateTime(isoString) {
    const date = new Date(isoString);
    return date.toLocaleString();
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

// Export functions for potential use in other scripts
window.QuotationHandler = {
    formatDateTime,
    formatCurrency
};
