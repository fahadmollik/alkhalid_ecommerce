// Enhanced Header JavaScript Functionality

document.addEventListener('DOMContentLoaded', function() {
    
    // Header scroll effect
    const header = document.querySelector('.modern-header');
    let lastScrollTop = 0;
    
    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        // Add scrolled class for enhanced shadow
        if (scrollTop > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
        
        lastScrollTop = scrollTop;
    });
    
    // Enhanced search functionality
    const searchInput = document.querySelector('.search-input');
    const searchBtn = document.querySelector('.search-btn');
    const searchContainer = document.querySelector('.search-container');
    const searchSuggestions = document.querySelector('.search-suggestions');
    
    if (searchInput && searchBtn && searchContainer) {
        let searchTimeout;
        
        // Enhanced search input focus/blur effects
        searchInput.addEventListener('focus', function() {
            this.placeholder = 'Type to search...';
            searchContainer.style.transform = 'translateY(-2px) scale(1.01)';
            searchContainer.style.boxShadow = '0 8px 35px rgba(13, 110, 253, 0.25)';
            
            // Add typing animation to search button
            searchBtn.style.background = 'linear-gradient(135deg, #0056b3 0%, var(--primary-color) 100%)';
        });
        
        searchInput.addEventListener('blur', function() {
            this.placeholder = 'Search products, brands, categories...';
            searchContainer.style.transform = 'translateY(0) scale(1)';
            searchContainer.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.08)';
            
            // Reset search button
            searchBtn.style.background = 'linear-gradient(135deg, var(--primary-color) 0%, #0056b3 100%)';
            
            // Hide suggestions after a delay
            setTimeout(() => {
                if (searchSuggestions) {
                    searchSuggestions.classList.add('d-none');
                }
            }, 200);
        });
        
        // Enhanced typing effects
        searchInput.addEventListener('input', function() {
            const query = this.value.trim();
            
            // Add ripple effect to search button on typing
            if (query.length > 0) {
                searchBtn.style.transform = 'scale(1.05)';
                setTimeout(() => {
                    searchBtn.style.transform = 'scale(1)';
                }, 150);
            }
            
            clearTimeout(searchTimeout);
            
            if (query.length > 2) {
                searchTimeout = setTimeout(() => {
                    showSearchSuggestions(query);
                }, 300);
            } else if (searchSuggestions) {
                searchSuggestions.classList.add('d-none');
            }
        });
        
        // Enhanced search button hover effects
        searchBtn.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.05)';
            this.style.background = 'linear-gradient(135deg, #0056b3 0%, var(--primary-color) 100%)';
            
            // Add icon animation
            const icon = this.querySelector('i');
            if (icon) {
                icon.style.transform = 'scale(1.1) rotate(5deg)';
            }
        });
        
        searchBtn.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
            this.style.background = 'linear-gradient(135deg, var(--primary-color) 0%, #0056b3 100%)';
            
            // Reset icon animation
            const icon = this.querySelector('i');
            if (icon) {
                icon.style.transform = 'scale(1) rotate(0deg)';
            }
        });
        
        // Enhanced search button click effect
        searchBtn.addEventListener('mousedown', function() {
            this.style.transform = 'scale(0.98)';
        });
        
        searchBtn.addEventListener('mouseup', function() {
            this.style.transform = 'scale(1.05)';
        });
        
        // Search form submission enhancement
        const searchForm = document.querySelector('.search-form');
        if (searchForm) {
            searchForm.addEventListener('submit', function(e) {
                const query = searchInput.value.trim();
                if (query.length === 0) {
                    e.preventDefault();
                    
                    // Shake animation for empty search
                    searchContainer.style.animation = 'shake 0.5s ease-in-out';
                    setTimeout(() => {
                        searchContainer.style.animation = '';
                    }, 500);
                    
                    searchInput.focus();
                    return false;
                }
                
                // Success animation
                searchBtn.style.background = 'linear-gradient(135deg, #198754, #20c997)';
                searchBtn.innerHTML = '<i class="fas fa-check"></i>';
                
                setTimeout(() => {
                    searchBtn.innerHTML = '<i class="fas fa-search"></i>';
                    searchBtn.style.background = 'linear-gradient(135deg, var(--primary-color) 0%, #0056b3 100%)';
                }, 1000);
            });
        }
        
        // Mock search suggestions function
        function showSearchSuggestions(query) {
            const mockSuggestions = [
                'Electronics',
                'Fashion',
                'Home & Garden',
                'Sports & Outdoors',
                'Books',
                'Toys & Games'
            ].filter(item => item.toLowerCase().includes(query.toLowerCase()));
            
            if (mockSuggestions.length > 0) {
                const suggestionsHTML = mockSuggestions.map(suggestion => 
                    `<div class="p-2 border-bottom hover-bg-light cursor-pointer">${suggestion}</div>`
                ).join('');
                
                searchSuggestions.innerHTML = suggestionsHTML;
                searchSuggestions.classList.remove('d-none');
                
                // Add click handlers to suggestions
                searchSuggestions.querySelectorAll('div').forEach(item => {
                    item.addEventListener('click', function() {
                        searchInput.value = this.textContent;
                        searchSuggestions.classList.add('d-none');
                        searchInput.form.submit();
                    });
                });
            }
        }
    }
    
    // Animate cart badge when items are added
    const cartBadge = document.querySelector('.cart-badge');
    if (cartBadge) {
        // Add a more pronounced animation when cart updates
        function animateCartBadge() {
            cartBadge.style.animation = 'none';
            setTimeout(() => {
                cartBadge.style.animation = 'cartBounce 0.6s ease-in-out';
            }, 10);
        }
        
        // You can call this function when items are added to cart
        window.animateCartUpdate = animateCartBadge;
    }
    
    // Header buttons hover effects
    const headerButtons = document.querySelectorAll('.btn-header');
    headerButtons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px) scale(1.05)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
    
    // Logo animation on click
    const logo = document.querySelector('.navbar-brand');
    if (logo) {
        logo.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Add a fun spin animation
            this.style.transform = 'rotate(360deg) scale(1.1)';
            setTimeout(() => {
                this.style.transform = 'rotate(0deg) scale(1)';
                window.location.href = this.href;
            }, 500);
        });
    }
    
    // Mobile search toggle (if needed)
    if (window.innerWidth <= 768 && searchContainer) {
        // Add smooth slide animation for mobile search
        searchContainer.style.transition = 'all 0.3s ease';
    }
    
    // Keyboard navigation for search suggestions
    if (searchInput && searchSuggestions) {
        let selectedSuggestion = -1;
        
        searchInput.addEventListener('keydown', function(e) {
            const suggestions = searchSuggestions.querySelectorAll('div');
            
            if (e.key === 'ArrowDown') {
                e.preventDefault();
                selectedSuggestion = Math.min(selectedSuggestion + 1, suggestions.length - 1);
                updateSelectedSuggestion(suggestions);
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                selectedSuggestion = Math.max(selectedSuggestion - 1, -1);
                updateSelectedSuggestion(suggestions);
            } else if (e.key === 'Enter' && selectedSuggestion >= 0) {
                e.preventDefault();
                suggestions[selectedSuggestion].click();
            } else if (e.key === 'Escape') {
                searchSuggestions.classList.add('d-none');
                selectedSuggestion = -1;
            }
        });
        
        function updateSelectedSuggestion(suggestions) {
            suggestions.forEach((suggestion, index) => {
                suggestion.classList.toggle('bg-light', index === selectedSuggestion);
            });
        }
    }
});

// Add CSS for additional animations
const style = document.createElement('style');
style.textContent = `
    @keyframes cartBounce {
        0%, 20%, 60%, 100% { transform: scale(1); }
        40% { transform: scale(1.25); }
        80% { transform: scale(1.1); }
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
        20%, 40%, 60%, 80% { transform: translateX(5px); }
    }
    
    .hover-bg-light:hover {
        background-color: #f8f9fa !important;
    }
    
    .cursor-pointer {
        cursor: pointer;
    }
    
    .search-suggestions div {
        transition: background-color 0.2s ease;
    }
    
    .search-container {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    .search-btn i {
        transition: transform 0.3s ease !important;
    }
`;
document.head.appendChild(style);
