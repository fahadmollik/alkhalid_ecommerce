// Enhanced Mobile Categories with Touch Gestures
class MobileCategoriesSlider {
    constructor(container) {
        this.container = container;
        this.wrapper = container.querySelector('.mobile-categories-wrapper');
        this.items = container.querySelectorAll('.mobile-category-item');
        this.prevBtn = container.querySelector('.mobile-category-nav.prev');
        this.nextBtn = container.querySelector('.mobile-category-nav.next');
        this.indicators = container.querySelectorAll('.mobile-category-indicator');
        
        this.currentIndex = 0;
        this.itemsPerView = this.getItemsPerView();
        this.maxIndex = Math.max(0, this.items.length - this.itemsPerView);
        
        // Touch/swipe properties
        this.startX = 0;
        this.startY = 0;
        this.currentX = 0;
        this.currentY = 0;
        this.isDragging = false;
        this.isScrolling = false;
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.updateNavigationState();
        this.setupIntersectionObserver();
        
        // Auto-hide navigation hint after 3 seconds
        setTimeout(() => {
            const hint = this.container.querySelector('.mobile-swipe-hint');
            if (hint) {
                hint.style.opacity = '0';
                hint.style.transition = 'opacity 0.5s ease';
            }
        }, 3000);
    }
    
    getItemsPerView() {
        const containerWidth = this.container.offsetWidth;
        const itemWidth = 160; // Approximate item width
        return Math.floor(containerWidth / itemWidth) || 2;
    }
    
    setupEventListeners() {
        // Navigation buttons
        if (this.prevBtn) {
            this.prevBtn.addEventListener('click', () => this.prev());
        }
        if (this.nextBtn) {
            this.nextBtn.addEventListener('click', () => this.next());
        }
        
        // Touch events
        this.wrapper.addEventListener('touchstart', (e) => this.handleTouchStart(e), { passive: false });
        this.wrapper.addEventListener('touchmove', (e) => this.handleTouchMove(e), { passive: false });
        this.wrapper.addEventListener('touchend', (e) => this.handleTouchEnd(e), { passive: true });
        
        // Mouse events for desktop testing
        this.wrapper.addEventListener('mousedown', (e) => this.handleMouseDown(e));
        this.wrapper.addEventListener('mousemove', (e) => this.handleMouseMove(e));
        this.wrapper.addEventListener('mouseup', (e) => this.handleMouseUp(e));
        this.wrapper.addEventListener('mouseleave', (e) => this.handleMouseUp(e));
        
        // Indicators
        this.indicators.forEach((indicator, index) => {
            indicator.addEventListener('click', () => this.goToSlide(index));
        });
        
        // Resize handler
        window.addEventListener('resize', () => this.handleResize());
        
        // Keyboard navigation
        this.container.addEventListener('keydown', (e) => this.handleKeydown(e));
    }
    
    setupIntersectionObserver() {
        if (!('IntersectionObserver' in window)) return;
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('in-view');
                } else {
                    entry.target.classList.remove('in-view');
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '20px'
        });
        
        this.items.forEach(item => observer.observe(item));
    }
    
    handleTouchStart(e) {
        this.startX = e.touches[0].clientX;
        this.startY = e.touches[0].clientY;
        this.isDragging = true;
        this.isScrolling = false;
        this.wrapper.classList.add('dragging');
    }
    
    handleTouchMove(e) {
        if (!this.isDragging) return;
        
        this.currentX = e.touches[0].clientX;
        this.currentY = e.touches[0].clientY;
        
        const deltaX = Math.abs(this.currentX - this.startX);
        const deltaY = Math.abs(this.currentY - this.startY);
        
        // Determine if user is scrolling vertically or swiping horizontally
        if (!this.isScrolling) {
            if (deltaY > deltaX) {
                this.isScrolling = true;
                this.isDragging = false;
                this.wrapper.classList.remove('dragging');
                return;
            }
        }
        
        if (deltaX > deltaY && deltaX > 10) {
            e.preventDefault(); // Prevent vertical scrolling
        }
    }
    
    handleTouchEnd(e) {
        if (!this.isDragging) return;
        
        const deltaX = this.currentX - this.startX;
        const threshold = 50;
        
        if (Math.abs(deltaX) > threshold) {
            if (deltaX > 0) {
                this.prev();
            } else {
                this.next();
            }
        }
        
        this.isDragging = false;
        this.wrapper.classList.remove('dragging');
    }
    
    handleMouseDown(e) {
        if (window.innerWidth > 768) return; // Only for mobile testing
        
        this.startX = e.clientX;
        this.isDragging = true;
        this.wrapper.classList.add('dragging');
        e.preventDefault();
    }
    
    handleMouseMove(e) {
        if (!this.isDragging || window.innerWidth > 768) return;
        
        this.currentX = e.clientX;
        e.preventDefault();
    }
    
    handleMouseUp(e) {
        if (!this.isDragging || window.innerWidth > 768) return;
        
        const deltaX = this.currentX - this.startX;
        const threshold = 50;
        
        if (Math.abs(deltaX) > threshold) {
            if (deltaX > 0) {
                this.prev();
            } else {
                this.next();
            }
        }
        
        this.isDragging = false;
        this.wrapper.classList.remove('dragging');
    }
    
    handleKeydown(e) {
        switch(e.key) {
            case 'ArrowLeft':
                e.preventDefault();
                this.prev();
                break;
            case 'ArrowRight':
                e.preventDefault();
                this.next();
                break;
        }
    }
    
    handleResize() {
        this.itemsPerView = this.getItemsPerView();
        this.maxIndex = Math.max(0, this.items.length - this.itemsPerView);
        this.currentIndex = Math.min(this.currentIndex, this.maxIndex);
        this.updateSlider();
    }
    
    prev() {
        if (this.currentIndex > 0) {
            this.currentIndex--;
            this.updateSlider();
        }
    }
    
    next() {
        if (this.currentIndex < this.maxIndex) {
            this.currentIndex++;
            this.updateSlider();
        }
    }
    
    goToSlide(index) {
        this.currentIndex = Math.max(0, Math.min(index, this.maxIndex));
        this.updateSlider();
    }
    
    updateSlider() {
        const itemWidth = this.items[0]?.offsetWidth || 160;
        const gap = 12; // 0.75rem
        const translateX = -(this.currentIndex * (itemWidth + gap));
        
        this.wrapper.style.transform = `translateX(${translateX}px)`;
        this.updateNavigationState();
        this.updateIndicators();
        
        // Add haptic feedback on mobile
        if ('vibrate' in navigator && window.innerWidth <= 768) {
            navigator.vibrate(10);
        }
    }
    
    updateNavigationState() {
        if (this.prevBtn) {
            this.prevBtn.style.opacity = this.currentIndex === 0 ? '0.3' : '0.8';
            this.prevBtn.style.pointerEvents = this.currentIndex === 0 ? 'none' : 'auto';
        }
        
        if (this.nextBtn) {
            this.nextBtn.style.opacity = this.currentIndex >= this.maxIndex ? '0.3' : '0.8';
            this.nextBtn.style.pointerEvents = this.currentIndex >= this.maxIndex ? 'none' : 'auto';
        }
    }
    
    updateIndicators() {
        this.indicators.forEach((indicator, index) => {
            indicator.classList.toggle('active', index === this.currentIndex);
        });
    }
}

// Initialize mobile categories slider
document.addEventListener('DOMContentLoaded', function() {
    const mobileContainer = document.querySelector('.mobile-categories-section');
    if (mobileContainer && window.innerWidth <= 991) {
        new MobileCategoriesSlider(mobileContainer);
    }
    
    // Reinitialize on window resize
    let resizeTimeout;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(() => {
            const container = document.querySelector('.mobile-categories-section');
            if (container && window.innerWidth <= 991) {
                new MobileCategoriesSlider(container);
            }
        }, 250);
    });
});

// Preload images for better performance
function preloadCategoryImages() {
    const images = document.querySelectorAll('.mobile-category-image');
    images.forEach(img => {
        if (img.dataset.src) {
            img.src = img.dataset.src;
        }
    });
}

// Call preload after DOM is ready
document.addEventListener('DOMContentLoaded', preloadCategoryImages);
