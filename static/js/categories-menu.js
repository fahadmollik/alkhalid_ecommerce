// Categories Menu JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle functionality
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const categoriesMenu = document.querySelector('.categories-mobile-menu');
    const menuOverlay = document.querySelector('.menu-overlay');
    
    if (mobileMenuToggle && categoriesMenu) {
        mobileMenuToggle.addEventListener('click', function() {
            categoriesMenu.classList.toggle('active');
            document.body.classList.toggle('menu-open');
            
            // Create overlay if it doesn't exist
            if (!menuOverlay) {
                const overlay = document.createElement('div');
                overlay.className = 'menu-overlay';
                overlay.style.cssText = `
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: rgba(0, 0, 0, 0.5);
                    z-index: 1010;
                    opacity: 0;
                    visibility: hidden;
                    transition: all 0.3s ease;
                `;
                document.body.appendChild(overlay);
                
                overlay.addEventListener('click', function() {
                    categoriesMenu.classList.remove('active');
                    document.body.classList.remove('menu-open');
                    this.style.opacity = '0';
                    this.style.visibility = 'hidden';
                });
            }
            
            const overlay = document.querySelector('.menu-overlay');
            if (categoriesMenu.classList.contains('active')) {
                overlay.style.opacity = '1';
                overlay.style.visibility = 'visible';
            } else {
                overlay.style.opacity = '0';
                overlay.style.visibility = 'hidden';
            }
        });
    }
    
    // Dropdown menu functionality
    const dropdownItems = document.querySelectorAll('.category-dropdown');
    
    dropdownItems.forEach(item => {
        const toggle = item.querySelector('.dropdown-toggle');
        const menu = item.querySelector('.dropdown-menu');
        
        if (toggle && menu) {
            toggle.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                // Close other dropdowns
                dropdownItems.forEach(otherItem => {
                    if (otherItem !== item) {
                        otherItem.classList.remove('active');
                    }
                });
                
                // Toggle current dropdown
                item.classList.toggle('active');
            });
        }
    });
    
    // Close dropdowns when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.category-dropdown')) {
            dropdownItems.forEach(item => {
                item.classList.remove('active');
            });
        }
    });
    
    // Mega menu functionality
    const megaMenuTriggers = document.querySelectorAll('.mega-menu-trigger');
    
    megaMenuTriggers.forEach(trigger => {
        const megaMenu = trigger.nextElementSibling;
        let timeoutId;
        
        if (megaMenu && megaMenu.classList.contains('mega-menu')) {
            // Show mega menu on hover
            trigger.addEventListener('mouseenter', function() {
                clearTimeout(timeoutId);
                megaMenu.classList.add('active');
                
                // Add backdrop
                const backdrop = document.createElement('div');
                backdrop.className = 'mega-menu-backdrop';
                backdrop.style.cssText = `
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: rgba(0, 0, 0, 0.1);
                    z-index: 999;
                `;
                document.body.appendChild(backdrop);
            });
            
            // Hide mega menu on leave
            [trigger, megaMenu].forEach(element => {
                element.addEventListener('mouseleave', function() {
                    timeoutId = setTimeout(() => {
                        megaMenu.classList.remove('active');
                        const backdrop = document.querySelector('.mega-menu-backdrop');
                        if (backdrop) {
                            backdrop.remove();
                        }
                    }, 300);
                });
                
                element.addEventListener('mouseenter', function() {
                    clearTimeout(timeoutId);
                });
            });
        }
    });
    
    // Search functionality in categories
    const categorySearch = document.querySelector('.category-search');
    if (categorySearch) {
        const searchInput = categorySearch.querySelector('input');
        const searchResults = document.createElement('div');
        searchResults.className = 'search-results';
        searchResults.style.cssText = `
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            background: white;
            border: 1px solid #dee2e6;
            border-top: none;
            border-radius: 0 0 0.375rem 0.375rem;
            max-height: 300px;
            overflow-y: auto;
            z-index: 1050;
            display: none;
        `;
        categorySearch.appendChild(searchResults);
        
        searchInput.addEventListener('input', function() {
            const query = this.value.toLowerCase().trim();
            
            if (query.length < 2) {
                searchResults.style.display = 'none';
                return;
            }
            
            // Mock search results - replace with actual search logic
            const mockResults = [
                'Electronics',
                'Clothing',
                'Books',
                'Home & Garden',
                'Sports & Outdoors'
            ].filter(item => item.toLowerCase().includes(query));
            
            searchResults.innerHTML = mockResults.map(result => `
                <div class="search-result-item" style="padding: 0.5rem 1rem; cursor: pointer; border-bottom: 1px solid #f8f9fa;">
                    ${result}
                </div>
            `).join('');
            
            searchResults.style.display = mockResults.length > 0 ? 'block' : 'none';
            
            // Add click handlers
            searchResults.querySelectorAll('.search-result-item').forEach(item => {
                item.addEventListener('click', function() {
                    searchInput.value = this.textContent;
                    searchResults.style.display = 'none';
                    // Handle search selection
                });
            });
        });
        
        // Hide search results when clicking outside
        document.addEventListener('click', function(e) {
            if (!categorySearch.contains(e.target)) {
                searchResults.style.display = 'none';
            }
        });
    }
    
    // Smooth scroll for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                e.preventDefault();
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Lazy loading for category images
    const categoryImages = document.querySelectorAll('.category-image[data-src]');
    
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        categoryImages.forEach(img => {
            imageObserver.observe(img);
        });
    } else {
        // Fallback for browsers without IntersectionObserver
        categoryImages.forEach(img => {
            img.src = img.dataset.src;
        });
    }
    
    // Multi-level Category Toggle Functionality
    // Wait for Bootstrap to be available before initializing
    if (typeof bootstrap !== 'undefined') {
        console.log('Bootstrap available, initializing multi-level categories...');
        initMultiLevelCategories();
    } else {
        console.log('Bootstrap not available, waiting...');
        // Wait a bit for Bootstrap to load
        setTimeout(function() {
            if (typeof bootstrap !== 'undefined') {
                console.log('Bootstrap loaded after delay, initializing...');
                initMultiLevelCategories();
            } else {
                console.warn('Bootstrap still not available, using fallback...');
                initMultiLevelCategoriesSimple();
            }
        }, 100);
    }
});

function initMultiLevelCategories() {
    console.log('Initializing multi-level categories with Bootstrap...');
    
    // Handle category toggle buttons
    const categoryToggleBtns = document.querySelectorAll('.category-toggle-btn');
    console.log('Found toggle buttons:', categoryToggleBtns.length);
    
    categoryToggleBtns.forEach((button, index) => {
        console.log(`Setting up button ${index + 1}...`);
        
        button.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            console.log('Toggle button clicked!');
            
            const targetId = this.getAttribute('data-bs-target');
            const targetElement = document.querySelector(targetId);
            const arrow = this.querySelector('.category-arrow');
            
            console.log('Target ID:', targetId);
            console.log('Target element:', targetElement);
            
            if (targetElement) {
                // Check current state more reliably
                const isCurrentlyShown = targetElement.classList.contains('show') || 
                                        targetElement.classList.contains('collapsing') ||
                                        this.getAttribute('aria-expanded') === 'true';
                
                console.log('Currently shown:', isCurrentlyShown);
                
                try {
                    // Use Bootstrap's Collapse API for proper functionality
                    let bsCollapse;
                    
                    // Get existing Bootstrap collapse instance or create new one
                    if (targetElement._bsCollapse) {
                        bsCollapse = targetElement._bsCollapse;
                    } else {
                        bsCollapse = new bootstrap.Collapse(targetElement, {
                            toggle: false
                        });
                        targetElement._bsCollapse = bsCollapse;
                    }
                    
                    if (isCurrentlyShown) {
                        // Collapse
                        console.log('Collapsing...');
                        bsCollapse.hide();
                        this.setAttribute('aria-expanded', 'false');
                        if (arrow) {
                            arrow.style.transform = 'rotate(0deg)';
                            arrow.style.transition = 'transform 0.3s ease';
                        }
                    } else {
                        // Expand
                        console.log('Expanding...');
                        bsCollapse.show();
                        this.setAttribute('aria-expanded', 'true');
                        if (arrow) {
                            arrow.style.transform = 'rotate(90deg)';
                            arrow.style.transition = 'transform 0.3s ease';
                        }
                    }
                } catch (error) {
                    console.error('Bootstrap collapse error:', error);
                    // Fallback to simple toggle
                    if (isCurrentlyShown) {
                        targetElement.classList.remove('show');
                        this.setAttribute('aria-expanded', 'false');
                        if (arrow) {
                            arrow.style.transform = 'rotate(0deg)';
                        }
                    } else {
                        targetElement.classList.add('show');
                        this.setAttribute('aria-expanded', 'true');
                        if (arrow) {
                            arrow.style.transform = 'rotate(90deg)';
                        }
                    }
                }
            } else {
                console.error('Target element not found for:', targetId);
            }
        });
        
        // Handle Bootstrap collapse events for proper arrow rotation
        const targetId = button.getAttribute('data-bs-target');
        const targetElement = document.querySelector(targetId);
        
        if (targetElement) {
            targetElement.addEventListener('shown.bs.collapse', function() {
                console.log('Bootstrap collapse shown event');
                const arrow = button.querySelector('.category-arrow');
                if (arrow) {
                    arrow.style.transform = 'rotate(90deg)';
                    arrow.style.transition = 'transform 0.3s ease';
                }
                button.setAttribute('aria-expanded', 'true');
            });
            
            targetElement.addEventListener('hidden.bs.collapse', function() {
                console.log('Bootstrap collapse hidden event');
                const arrow = button.querySelector('.category-arrow');
                if (arrow) {
                    arrow.style.transform = 'rotate(0deg)';
                    arrow.style.transition = 'transform 0.3s ease';
                }
                button.setAttribute('aria-expanded', 'false');
            });
        }
    });
    
    // Handle category link clicks for parents with children
    const categoryLinks = document.querySelectorAll('.category-parent-wrapper .category-link');
    
    categoryLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // Allow normal navigation but also handle toggle if user clicks on the link
            const toggleBtn = this.parentElement.querySelector('.category-toggle-btn');
            
            // Option 1: Navigate to category page immediately
            // (Default behavior - link works normally)
            
            // Option 2: Toggle subcategories on first click, navigate on second click
            // Uncomment below if you want this behavior:
            /*
            const isExpanded = toggleBtn.getAttribute('aria-expanded') === 'true';
            if (!isExpanded) {
                e.preventDefault();
                toggleBtn.click();
            }
            */
        });
    });
    
    // Add active class to current category
    highlightCurrentCategory();
    
    // Auto-expand parent categories if child is active
    autoExpandActiveCategories();
}

function highlightCurrentCategory() {
    const currentPath = window.location.pathname;
    const categoryLinks = document.querySelectorAll('.category-link');
    
    categoryLinks.forEach(link => {
        const linkPath = new URL(link.href).pathname;
        if (linkPath === currentPath) {
            const categoryItem = link.closest('.category-item');
            if (categoryItem) {
                categoryItem.classList.add('active');
            }
        }
    });
}

function autoExpandActiveCategories() {
    const activeCategoryItem = document.querySelector('.category-item.active');
    
    if (activeCategoryItem) {
        // Find all parent subcategory containers and expand them
        let currentElement = activeCategoryItem.parentElement;
        
        while (currentElement && currentElement !== document.body) {
            if (currentElement.classList.contains('subcategory-container')) {
                // Find the toggle button for this subcategory container
                const containerId = currentElement.id;
                const toggleBtn = document.querySelector(`[data-bs-target="#${containerId}"]`);
                
                if (toggleBtn) {
                    // Expand this level
                    currentElement.classList.add('show');
                    toggleBtn.setAttribute('aria-expanded', 'true');
                    const arrow = toggleBtn.querySelector('.category-arrow');
                    if (arrow) {
                        arrow.style.transform = 'rotate(90deg)';
                    }
                }
            }
            currentElement = currentElement.parentElement;
        }
    }
}

// Add smooth scrolling for better UX
function addSmoothScrolling() {
    const categoryLinks = document.querySelectorAll('.category-link[href^="#"]');
    
    categoryLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                e.preventDefault();
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Simple fallback initialization without Bootstrap API
function initMultiLevelCategoriesSimple() {
    console.log('Initializing categories with simple toggle...');
    const categoryToggleBtns = document.querySelectorAll('.category-toggle-btn');
    console.log('Found toggle buttons (simple):', categoryToggleBtns.length);
    
    categoryToggleBtns.forEach((button, index) => {
        console.log(`Setting up simple button ${index + 1}...`);
        
        button.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            console.log('Simple toggle button clicked!');
            
            const targetId = this.getAttribute('data-bs-target');
            const targetElement = document.querySelector(targetId);
            const arrow = this.querySelector('.category-arrow');
            
            console.log('Simple - Target ID:', targetId);
            console.log('Simple - Target element:', targetElement);
            
            if (targetElement) {
                // Check multiple indicators for current state
                const isCurrentlyShown = targetElement.classList.contains('show') || 
                                        this.getAttribute('aria-expanded') === 'true' ||
                                        targetElement.style.display === 'block';
                
                console.log('Simple - Currently shown:', isCurrentlyShown);
                
                if (isCurrentlyShown) {
                    // Collapse
                    console.log('Simple - Collapsing...');
                    targetElement.classList.remove('show');
                    targetElement.style.display = 'none';
                    this.setAttribute('aria-expanded', 'false');
                    if (arrow) {
                        arrow.style.transform = 'rotate(0deg)';
                        arrow.style.transition = 'transform 0.3s ease';
                    }
                } else {
                    // Expand
                    console.log('Simple - Expanding...');
                    targetElement.classList.add('show');
                    targetElement.style.display = 'block';
                    this.setAttribute('aria-expanded', 'true');
                    if (arrow) {
                        arrow.style.transform = 'rotate(90deg)';
                        arrow.style.transition = 'transform 0.3s ease';
                    }
                }
            } else {
                console.error('Simple - Target element not found for:', targetId);
            }
        });
    });
    
    // Add active class to current category
    highlightCurrentCategory();
    
    // Auto-expand parent categories if child is active
    autoExpandActiveCategories();
}
