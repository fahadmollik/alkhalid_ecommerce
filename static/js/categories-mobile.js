// Categories Mobile JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Mobile categories scroll functionality
    const categoryScrollContainer = document.querySelector('.category-scroll-container');
    
    if (categoryScrollContainer) {
        // Add smooth scrolling behavior
        categoryScrollContainer.style.scrollBehavior = 'smooth';
        
        // Touch scroll optimization for mobile
        let isScrolling = false;
        let touchStart = 0;
        
        categoryScrollContainer.addEventListener('touchstart', function(e) {
            touchStart = e.touches[0].clientX;
            isScrolling = false;
        });
        
        categoryScrollContainer.addEventListener('touchmove', function(e) {
            if (!touchStart) return;
            
            const touchCurrent = e.touches[0].clientX;
            const touchDiff = touchStart - touchCurrent;
            
            if (Math.abs(touchDiff) > 10) {
                isScrolling = true;
            }
        });
        
        categoryScrollContainer.addEventListener('touchend', function() {
            touchStart = 0;
            setTimeout(() => {
                isScrolling = false;
            }, 100);
        });
        
        // Category item click handler
        const categoryItems = document.querySelectorAll('.category-mobile-item');
        categoryItems.forEach(item => {
            item.addEventListener('click', function(e) {
                if (isScrolling) {
                    e.preventDefault();
                    return false;
                }
                
                // Add click animation
                this.style.transform = 'scale(0.95)';
                setTimeout(() => {
                    this.style.transform = '';
                }, 150);
            });
        });
    }
    
    // Mobile category search functionality
    const categorySearch = document.querySelector('#mobile-category-search');
    if (categorySearch) {
        categorySearch.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const categories = document.querySelectorAll('.category-mobile-item');
            
            categories.forEach(category => {
                const categoryName = category.querySelector('h6').textContent.toLowerCase();
                if (categoryName.includes(searchTerm)) {
                    category.style.display = 'block';
                } else {
                    category.style.display = 'none';
                }
            });
        });
    }
});
