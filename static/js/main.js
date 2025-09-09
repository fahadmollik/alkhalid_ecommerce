// Main JavaScript for E-Commerce Store

document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Sticky header scroll effect with throttling
    const header = document.querySelector('header');
    if (header) {
        let lastScrollTop = 0;
        let ticking = false;

        function updateHeader() {
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            
            if (Math.abs(scrollTop - lastScrollTop) > 5) { // Only update if scroll difference is significant
                if (scrollTop > 100) {
                    header.classList.add('scrolled');
                } else {
                    header.classList.remove('scrolled');
                }
                lastScrollTop = scrollTop;
            }
            ticking = false;
        }

        window.addEventListener('scroll', function() {
            if (!ticking) {
                requestAnimationFrame(updateHeader);
                ticking = true;
            }
        }, { passive: true });
    }

    // Add to cart functionality with AJAX
    const addToCartForms = document.querySelectorAll('.add-to-cart-form');
    addToCartForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const button = form.querySelector('button[type="submit"]');
            const originalHTML = button.innerHTML;
            
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
    // End of DOMContentLoaded
});
        });
                this.value = min;
            } else if (value > max) {
                this.value = max;
                showAlert(`Maximum quantity is ${max}`, 'warning');
            }
        });
    });

    // Search functionality
    const searchForm = document.querySelector('form[action*="products"]');
    if (searchForm) {
        const searchInput = searchForm.querySelector('input[name="search"]');
        if (searchInput) {
            searchInput.addEventListener('keyup', debounce(function() {
                if (this.value.length >= 3) {
                    // Auto-search functionality could be implemented here
                }
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
        
        alertContainer.insertBefore(alert, alertContainer.firstChild);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (alert.parentNode) {
                alert.classList.remove('show');
                setTimeout(() => {
                    alert.remove();
                }, 150);
            }
        }, 5000);
    }
}

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