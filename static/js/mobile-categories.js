// Mobile Categories Additional JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Mobile categories grid functionality
    const mobileGrid = document.querySelector('.mobile-category-grid');
    
    if (mobileGrid) {
        // Add intersection observer for animation
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '50px'
        });
        
        // Observe all category cards
        const categoryCards = mobileGrid.querySelectorAll('.mobile-category-card');
        categoryCards.forEach((card, index) => {
            // Initial state for animation
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            card.style.transition = `opacity 0.6s ease ${index * 0.1}s, transform 0.6s ease ${index * 0.1}s`;
            
            observer.observe(card);
            
            // Add click ripple effect
            card.addEventListener('click', function(e) {
                const rect = this.getBoundingClientRect();
                const ripple = document.createElement('div');
                const size = Math.max(rect.width, rect.height);
                const x = e.clientX - rect.left - size / 2;
                const y = e.clientY - rect.top - size / 2;
                
                ripple.style.cssText = `
                    position: absolute;
                    width: ${size}px;
                    height: ${size}px;
                    left: ${x}px;
                    top: ${y}px;
                    background: rgba(0, 123, 255, 0.3);
                    border-radius: 50%;
                    transform: scale(0);
                    animation: ripple 0.6s ease-out;
                    pointer-events: none;
                    z-index: 1;
                `;
                
                this.style.position = 'relative';
                this.style.overflow = 'hidden';
                this.appendChild(ripple);
                
                setTimeout(() => {
                    ripple.remove();
                }, 600);
            });
        });
    }
    
    // Mobile category filter functionality
    const filterButtons = document.querySelectorAll('.mobile-category-filter');
    if (filterButtons.length > 0) {
        filterButtons.forEach(button => {
            button.addEventListener('click', function() {
                const filter = this.dataset.filter;
                const categories = document.querySelectorAll('.mobile-category-card');
                
                // Update active button
                filterButtons.forEach(btn => btn.classList.remove('active'));
                this.classList.add('active');
                
                // Filter categories
                categories.forEach(category => {
                    if (filter === 'all' || category.dataset.category === filter) {
                        category.style.display = 'block';
                        setTimeout(() => {
                            category.style.opacity = '1';
                            category.style.transform = 'scale(1)';
                        }, 100);
                    } else {
                        category.style.opacity = '0';
                        category.style.transform = 'scale(0.8)';
                        setTimeout(() => {
                            category.style.display = 'none';
                        }, 300);
                    }
                });
            });
        });
    }
    
    // Mobile category navigation functionality
    const mobilePrevBtn = document.querySelector('.mobile-category-nav.prev');
    const mobileNextBtn = document.querySelector('.mobile-category-nav.next');
    const mobileIndicators = document.querySelectorAll('.mobile-category-indicator');
    
    if (mobileGrid && mobilePrevBtn && mobileNextBtn) {
        console.log('Initializing mobile category navigation...');
        let currentIndex = 0;
        const categories = mobileGrid.querySelectorAll('.mobile-category-card');
        const categoriesPerPage = 4; // 4 categories per page on mobile
        const totalPages = Math.ceil(categories.length / categoriesPerPage);
        
        function updateMobileCarousel() {
            const offset = currentIndex * categoriesPerPage;
            categories.forEach((card, index) => {
                if (index >= offset && index < offset + categoriesPerPage) {
                    card.style.display = 'flex';
                } else {
                    card.style.display = 'none';
                }
            });
            
            // Update indicators
            mobileIndicators.forEach((indicator, index) => {
                indicator.classList.toggle('active', index === currentIndex);
            });
            
            // Update button states
            mobilePrevBtn.style.opacity = currentIndex === 0 ? '0.5' : '1';
            mobileNextBtn.style.opacity = currentIndex === totalPages - 1 ? '0.5' : '1';
            
            console.log(`Mobile carousel updated: page ${currentIndex + 1}/${totalPages}`);
        }
        
        mobilePrevBtn.addEventListener('click', function(e) {
            e.preventDefault();
            console.log('Mobile prev button clicked');
            if (currentIndex > 0) {
                currentIndex--;
                updateMobileCarousel();
            }
        });
        
        mobileNextBtn.addEventListener('click', function(e) {
            e.preventDefault();
            console.log('Mobile next button clicked');
            if (currentIndex < totalPages - 1) {
                currentIndex++;
                updateMobileCarousel();
            }
        });
        
        // Initialize
        updateMobileCarousel();
        console.log(`Mobile carousel initialized with ${totalPages} pages`);
    } else {
        console.log('Mobile category navigation elements not found');
    }
});

// Add CSS for ripple animation
const style = document.createElement('style');
style.textContent = `
    @keyframes ripple {
        to {
            transform: scale(2);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
