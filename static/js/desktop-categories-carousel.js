// Minimal Desktop Categories Auto-Sliding Carousel
class DesktopCategoriesCarousel {
    constructor() {
        this.container = document.querySelector('.desktop-categories-section');
        this.carousel = document.querySelector('.desktop-categories-carousel');
        this.track = document.querySelector('.desktop-categories-track');
        this.items = document.querySelectorAll('.desktop-category-item');
        this.prevBtn = document.getElementById('prevCategories');
        this.nextBtn = document.getElementById('nextCategories');
        
        this.currentIndex = 0;
        this.totalItems = this.items.length;
        this.itemsPerView = this.calculateItemsPerView();
        this.isAutoPlaying = true;
        this.autoPlayInterval = null;
        this.autoPlayDelay = 4000; // 4 seconds
        this.isTransitioning = false;
        
        this.init();
    }
    
    init() {
        if (!this.container || this.totalItems === 0) return;
        
        this.setupEventListeners();
        this.startAutoPlay();
        this.setupIntersectionObserver();
        this.setupTouchGestures();
        this.handleResize();
    }
    
    calculateItemsPerView() {
        const containerWidth = this.carousel?.offsetWidth || 1200;
        const itemWidth = 200; // 180px + 20px gap
        return Math.floor(containerWidth / itemWidth);
    }
    
    setupEventListeners() {
        // Navigation buttons
        this.prevBtn?.addEventListener('click', () => this.goToPrevious());
        this.nextBtn?.addEventListener('click', () => this.goToNext());
        
        // Pause on hover
        this.container?.addEventListener('mouseenter', () => this.pauseAutoPlay());
        this.container?.addEventListener('mouseleave', () => this.resumeAutoPlay());
        
        // Window resize
        window.addEventListener('resize', () => this.handleResize());
    }
    
    setupIntersectionObserver() {
        const options = {
            root: null,
            rootMargin: '0px',
            threshold: 0.1
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    this.startAutoPlay();
                } else {
                    this.pauseAutoPlay();
                }
            });
        }, options);
        
        if (this.container) {
            observer.observe(this.container);
        }
    }
    
    setupTouchGestures() {
        let startX = 0;
        let isDragging = false;
        
        this.carousel?.addEventListener('touchstart', (e) => {
            startX = e.touches[0].clientX;
            isDragging = true;
            this.pauseAutoPlay();
        });
        
        this.carousel?.addEventListener('touchend', (e) => {
            if (!isDragging) return;
            
            const endX = e.changedTouches[0].clientX;
            const deltaX = startX - endX;
            
            if (Math.abs(deltaX) > 50) {
                if (deltaX > 0) {
                    this.goToNext();
                } else {
                    this.goToPrevious();
                }
            }
            
            isDragging = false;
            this.resumeAutoPlay();
        });
    }
    
    goToNext() {
        if (this.isTransitioning) return;
        
        this.currentIndex = (this.currentIndex + 1) % this.totalItems;
        this.updateCarousel();
        this.resetAutoPlayTimer();
    }
    
    goToPrevious() {
        if (this.isTransitioning) return;
        
        this.currentIndex = (this.currentIndex - 1 + this.totalItems) % this.totalItems;
        this.updateCarousel();
        this.resetAutoPlayTimer();
    }
    
    goToSlide(index) {
        if (this.isTransitioning || index === this.currentIndex) return;
        
        this.currentIndex = index;
        this.updateCarousel();
        this.resetAutoPlayTimer();
    }
    
    updateCarousel() {
        if (!this.track) return;
        
        this.isTransitioning = true;
        
        // Calculate transform based on current index
        const itemWidth = 200; // 180px + 20px gap
        const translateX = -this.currentIndex * itemWidth;
        
        this.track.style.transform = `translateX(${translateX}px)`;
        
        // Reset transition flag after animation
        setTimeout(() => {
            this.isTransitioning = false;
        }, 600);
    }
    
    startAutoPlay() {
        if (!this.isAutoPlaying || this.autoPlayInterval) return;
        
        this.autoPlayInterval = setInterval(() => {
            this.goToNext();
        }, this.autoPlayDelay);
    }
    
    pauseAutoPlay() {
        if (this.autoPlayInterval) {
            clearInterval(this.autoPlayInterval);
            this.autoPlayInterval = null;
        }
    }
    
    resumeAutoPlay() {
        if (this.isAutoPlaying) {
            this.startAutoPlay();
        }
    }
    
    resetAutoPlayTimer() {
        this.pauseAutoPlay();
        if (this.isAutoPlaying) {
            this.startAutoPlay();
        }
    }
    
    handleResize() {
        const newItemsPerView = this.calculateItemsPerView();
        if (newItemsPerView !== this.itemsPerView) {
            this.itemsPerView = newItemsPerView;
            this.updateCarousel();
        }
    }
    
    // Public methods for external control
    next() {
        this.goToNext();
    }
    
    previous() {
        this.goToPrevious();
    }
    
    destroy() {
        this.pauseAutoPlay();
        window.removeEventListener('resize', this.handleResize);
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Only initialize on desktop screens
    if (window.innerWidth >= 992) {
        window.desktopCategoriesCarousel = new DesktopCategoriesCarousel();
    }
});

// Reinitialize on window resize if switching from mobile to desktop
window.addEventListener('resize', () => {
    if (window.innerWidth >= 992 && !window.desktopCategoriesCarousel) {
        window.desktopCategoriesCarousel = new DesktopCategoriesCarousel();
    } else if (window.innerWidth < 992 && window.desktopCategoriesCarousel) {
        window.desktopCategoriesCarousel.destroy();
        window.desktopCategoriesCarousel = null;
    }
});
