// Main JavaScript functionality for the e-commerce site
document.addEventListener('DOMContentLoaded', function() {
    console.log('Main.js loaded');

    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Add to cart functionality
    const addToCartForms = document.querySelectorAll('.add-to-cart-form');
    addToCartForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const button = this.querySelector('button[type="submit"]');
            const originalHTML = button.innerHTML;
            
            // Disable button and show loading
            button.disabled = true;
            button.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
            
            // Get form data
            const formData = new FormData(this);
            
            // Send AJAX request
            fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showAlert(data.message, 'success');
                    updateCartCount();
                    button.innerHTML = '<i class="fas fa-check"></i>';
                    button.classList.add('added-to-cart');
                    button.disabled = true;
                    console.log('Cart add success, button updated, reloading...');
                    setTimeout(() => {
                        window.location.reload();
                    }, 700);
                } else {
                    showAlert(data.message || 'Error adding to cart', 'danger');
                    button.innerHTML = originalHTML;
                    button.disabled = false;
                    console.log('Cart add failed:', data);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showAlert('Error adding to cart', 'danger');
                button.innerHTML = originalHTML;
                button.disabled = false;
            });
        });
    });

    // Quantity input validation
    const quantityInputs = document.querySelectorAll('input[type="number"][min][max]');
    quantityInputs.forEach(input => {
        input.addEventListener('change', function() {
            const min = parseInt(this.min);
            const max = parseInt(this.max);
            const value = parseInt(this.value);
            
            if (value < min) {
                this.value = min;
            } else if (value > max) {
                this.value = max;
                showAlert(`Maximum quantity is ${max}`, 'warning');
            }
        });
    });

    // Update cart count
    function updateCartCount() {
        fetch('/cart/count/')
            .then(response => response.json())
            .then(data => {
                const cartCount = document.querySelector('.cart-count');
                if (cartCount) {
                    cartCount.textContent = data.count;
                }
            })
            .catch(error => console.error('Error updating cart count:', error));
    }

    // Show alert function
    function showAlert(message, type = 'info') {
        // Remove existing alerts
        const existingAlerts = document.querySelectorAll('.custom-alert');
        existingAlerts.forEach(alert => alert.remove());
        
        // Create alert element
        const alert = document.createElement('div');
        alert.className = `alert alert-${type} alert-dismissible fade show custom-alert`;
        alert.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
            min-width: 300px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        `;
        alert.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        // Add to page
        document.body.appendChild(alert);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (alert.parentNode) {
                alert.remove();
            }
        }, 5000);
    }

    // Debounce function
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    // Search functionality
    const searchForm = document.querySelector('form[action*="products"]');
    if (searchForm) {
        const searchInput = searchForm.querySelector('input[name="search"]');
        if (searchInput) {
            searchInput.addEventListener('keyup', debounce(function() {
                if (this.value.length >= 3) {
                    // Auto-search functionality could be implemented here
                }
            }, 300));
        }
    }

    // Sticky header scroll effect
    let lastScrollTop = 0;
    let ticking = false;
    
    function updateHeader() {
        const header = document.querySelector('header');
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (header) {
            if (scrollTop > 100) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
        }
        
        lastScrollTop = scrollTop;
        ticking = false;
    }
    
    function requestTick() {
        if (!ticking) {
            requestAnimationFrame(updateHeader);
            ticking = true;
        }
    }
    
    window.addEventListener('scroll', requestTick);

    console.log('Main.js initialization complete');
});

function updateCartCount() {
    // This function would make an AJAX request to get updated cart count
    // For now, we'll just increment the visible count
    const cartBadge = document.querySelector('.badge');
    if (cartBadge) {
        const currentCount = parseInt(cartBadge.textContent) || 0;
        cartBadge.textContent = currentCount + 1;
        
        // Show the badge if it was hidden
        cartBadge.style.display = 'inline-block';
    }
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function openImageModal(src, alt) {
    // Create modal for image zoom
    const modal = document.createElement('div');
    modal.className = 'modal fade';
    modal.innerHTML = `
        <div class="modal-dialog modal-lg modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">${alt}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body text-center">
                    <img src="${src}" alt="${alt}" class="img-fluid">
            // Add to cart functionality with AJAX
            document.body.addEventListener('submit', function(e) {
                const form = e.target.closest('.add-to-cart-form');
                if (!form) return;
                e.preventDefault();
                let button = form.querySelector('button[type="submit"]');
                if (!button) {
                    console.error('Add to cart button not found in form:', form);
                    return;
                }
                const originalHTML = button.innerHTML;
                button.innerHTML = '<span class="loading"></span>';
                button.disabled = true;
                const formData = new FormData(form);
                fetch(form.action, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        showAlert(data.message, 'success');
                        updateCartCount();
                        button.innerHTML = '<i class="fas fa-check"></i>';
                        button.classList.add('added-to-cart');
                        button.disabled = true;
                        console.log('Cart add success, button updated, reloading...');
                        setTimeout(() => {
                            window.location.reload();
                        }, 700);
                    } else {
                        showAlert(data.message || 'Error adding to cart', 'danger');
                        button.innerHTML = originalHTML;
                        button.disabled = false;
                        console.log('Cart add failed:', data);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    showAlert('Error adding to cart', 'danger');
                    button.innerHTML = originalHTML;
                    button.disabled = false;
                });
            });