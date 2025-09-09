// Enhanced Categories Hamburger Menu Functionality

document.addEventListener('DOMContentLoaded', function() {
    const categoriesMenuToggle = document.getElementById('categoriesMenuToggle');
    const categoriesSidebar = document.getElementById('categoriesSidebar');
    const categoriesOverlay = document.getElementById('categoriesOverlay');
    const closeCategoriesMenu = document.getElementById('closeCategoriesMenu');

    if (categoriesMenuToggle && categoriesSidebar && categoriesOverlay) {
        // Open categories menu with enhanced animation
        categoriesMenuToggle.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            // Add loading animation to button
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 150);
            
            categoriesSidebar.classList.add('show');
            categoriesOverlay.classList.add('show');
            document.body.style.overflow = 'hidden';
            
            // Animate category items
            animateCategoryItems();
            
            // Focus management for accessibility
            const firstCategoryLink = categoriesSidebar.querySelector('.category-link');
            if (firstCategoryLink) {
                setTimeout(() => firstCategoryLink.focus(), 300);
            }
        });

        // Enhanced close function
        function closeCategoriesMenuFunction(immediate = false) {
            const delay = immediate ? 0 : 200;
            
            // Hide any open subcategories first
            const openSubcategories = document.querySelectorAll('.subcategory-container.show');
            openSubcategories.forEach(sub => sub.classList.remove('show'));
            
            setTimeout(() => {
                categoriesSidebar.classList.remove('show');
                categoriesOverlay.classList.remove('show');
                document.body.style.overflow = '';
                
                // Reset category animations
                const categoryItems = document.querySelectorAll('.category-item');
                categoryItems.forEach(item => {
                    item.style.animationDelay = '';
                    item.classList.remove('animate-in');
                });
            }, delay);
        }

        if (closeCategoriesMenu) {
            closeCategoriesMenu.addEventListener('click', closeCategoriesMenuFunction);
        }

        // Close menu when clicking overlay
        categoriesOverlay.addEventListener('click', closeCategoriesMenuFunction);

        // Close menu with Escape key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && categoriesSidebar.classList.contains('show')) {
                closeCategoriesMenuFunction();
            }
        });

        // Enhanced subcategory navigation
        initializeSubcategoryNavigation();
        
        // Initialize touch gestures for mobile
        initializeTouchGestures();
        
        // Initialize search functionality if search input exists
        initializeCategorySearch();
    }

    // Animate category items on menu open
    function animateCategoryItems() {
        const categoryItems = document.querySelectorAll('.categories-list .category-item');
        categoryItems.forEach((item, index) => {
            item.style.animationDelay = `${index * 0.1}s`;
            item.classList.add('animate-in');
        });
    }

    // Enhanced subcategory navigation
    function initializeSubcategoryNavigation() {
        // Handle category arrows for subcategory navigation
        document.addEventListener('click', function(e) {
            if (e.target.classList.contains('category-arrow') || 
                e.target.closest('.category-arrow-container')) {
                e.preventDefault();
                e.stopPropagation();
                
                const categoryLink = e.target.closest('.category-link');
                const categoryItem = categoryLink.closest('.category-item');
                const subcategoryContainer = categoryItem.querySelector('.subcategory-container');
                
                if (subcategoryContainer) {
                    // Add loading state
                    categoryItem.classList.add('loading');
                    
                    // Small delay for better UX
                    setTimeout(() => {
                        subcategoryContainer.classList.add('show');
                        categoryItem.classList.remove('loading');
                        
                        // Scroll to top of subcategory
                        subcategoryContainer.scrollTop = 0;
                        
                        // Focus management for accessibility
                        const backButton = subcategoryContainer.querySelector('.subcategory-back');
                        if (backButton) {
                            backButton.focus();
                        }
                    }, 150);
                }
            }
        });
        
        // Handle back button in subcategories
        document.addEventListener('click', function(e) {
            if (e.target.classList.contains('subcategory-back') || 
                e.target.closest('.subcategory-back')) {
                e.preventDefault();
                e.stopPropagation();
                
                const subcategoryContainer = e.target.closest('.subcategory-container');
                if (subcategoryContainer) {
                    subcategoryContainer.classList.remove('show');
                    
                    // Focus back to the parent category
                    const parentCategoryLink = subcategoryContainer.parentElement.querySelector('.category-link');
                    if (parentCategoryLink) {
                        setTimeout(() => parentCategoryLink.focus(), 300);
                    }
                }
            }
        });
    }

    // Touch gestures for mobile navigation
    function initializeTouchGestures() {
        let startX = 0;
        let currentX = 0;
        let isSwipping = false;
        
        document.addEventListener('touchstart', function(e) {
            const subcategoryContainer = e.target.closest('.subcategory-container.show');
            if (subcategoryContainer) {
                startX = e.touches[0].clientX;
                isSwipping = true;
            }
        }, { passive: true });
        
        document.addEventListener('touchmove', function(e) {
            if (!isSwipping) return;
            currentX = e.touches[0].clientX;
        }, { passive: true });
        
        document.addEventListener('touchend', function(e) {
            if (!isSwipping) return;
            isSwipping = false;
            
            const diffX = currentX - startX;
            const subcategoryContainer = e.target.closest('.subcategory-container.show');
            
            // Swipe right to go back (threshold: 50px)
            if (diffX > 50 && subcategoryContainer) {
                subcategoryContainer.classList.remove('show');
            }
        }, { passive: true });
    }

    // Category search functionality
    function initializeCategorySearch() {
        const searchInput = document.querySelector('.category-search');
        if (!searchInput) return;
        
        searchInput.addEventListener('input', function(e) {
            const searchTerm = e.target.value.toLowerCase().trim();
            const categoryItems = document.querySelectorAll('.categories-list .category-item');
            let hasVisibleItems = false;
            
            categoryItems.forEach(item => {
                const categoryName = item.querySelector('.category-name');
                if (!categoryName) return;
                
                const name = categoryName.textContent.toLowerCase();
                const shouldShow = name.includes(searchTerm) || searchTerm === '';
                
                item.style.display = shouldShow ? 'block' : 'none';
                
                if (shouldShow) {
                    hasVisibleItems = true;
                    // Add highlight to matching text
                    if (searchTerm) {
                        highlightText(categoryName, searchTerm);
                    } else {
                        removeHighlight(categoryName);
                    }
                }
            });
            
            // Show/hide no results message
            let noResultsMsg = document.querySelector('.no-search-results');
            if (!hasVisibleItems && searchTerm) {
                if (!noResultsMsg) {
                    noResultsMsg = document.createElement('div');
                    noResultsMsg.className = 'no-search-results text-center p-4 text-muted';
                    noResultsMsg.innerHTML = '<i class="fas fa-search mb-2 d-block" style="font-size: 2rem; opacity: 0.3;"></i>' +
                                           '<p>No categories found for "' + searchTerm + '"</p>';
                    document.querySelector('.categories-list').appendChild(noResultsMsg);
                }
                noResultsMsg.style.display = 'block';
            } else if (noResultsMsg) {
                noResultsMsg.style.display = 'none';
            }
        });
    }
    
    // Text highlighting helper
    function highlightText(element, term) {
        const originalText = element.textContent;
        const regex = new RegExp('(' + term + ')', 'gi');
        element.innerHTML = originalText.replace(regex, '<mark style="background-color: #fff3cd; padding: 1px 3px; border-radius: 2px;">$1</mark>');
    }
    
    // Remove highlight helper
    function removeHighlight(element) {
        const originalText = element.textContent;
        element.innerHTML = originalText;
    }
});

// Add enhanced CSS animations
const enhancedStyles = document.createElement('style');
enhancedStyles.textContent = `
    .category-item.animate-in {
        animation: slideInLeft 0.3s ease-out forwards;
        opacity: 0;
    }
    
    .category-item.loading .category-link {
        opacity: 0.6;
        pointer-events: none;
    }
    
    .category-item.loading::after {
        content: '';
        position: absolute;
        top: 50%;
        right: 20px;
        width: 16px;
        height: 16px;
        border: 2px solid #e9ecef;
        border-top: 2px solid #0d6efd;
        border-radius: 50%;
        animation: spinLoader 1s linear infinite;
        z-index: 10;
    }
    
    .categories-sidebar {
        transform: translateX(-100%);
        transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .categories-sidebar.show {
        transform: translateX(0);
    }
    
    .category-link:focus {
        outline: 2px solid #0d6efd;
        outline-offset: -2px;
        background-color: rgba(13, 110, 253, 0.1);
    }
    
    .subcategory-container {
        transition: transform 0.3s ease-in-out;
    }
    
    .subcategory-container.show {
        transform: translateX(0);
    }
    
    mark {
        animation: highlightPulse 2s infinite;
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes spinLoader {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    @keyframes highlightPulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
`;

document.head.appendChild(enhancedStyles);
