// Enhanced Desktop Categories with Advanced Animations
class DesktopCategoriesEnhancer {
    constructor() {
        this.container = document.querySelector('.desktop-categories-section');
        this.cards = document.querySelectorAll('.desktop-category-card');
        this.currentSlide = 0;
        this.totalSlides = 0;
        this.isAutoPlaying = true;
        this.autoPlayInterval = null;
        
        this.init();
    }
    
    init() {
        if (!this.container) return;
        
        this.setupParallax();
        this.setupIntersectionObserver();
        this.setupCardAnimations();
        this.setupAutoPlay();
        this.setupKeyboardNavigation();
        this.addPerformanceOptimizations();
    }
    
    setupParallax() {
        if (window.innerWidth < 992) return;
        
        let ticking = false;
        
        const updateParallax = () => {
            const scrollTop = window.pageYOffset;
            const containerTop = this.container.offsetTop;
            const containerHeight = this.container.offsetHeight;
            const windowHeight = window.innerHeight;
            
            // Check if container is in viewport
            if (scrollTop + windowHeight > containerTop && scrollTop < containerTop + containerHeight) {
                const progress = (scrollTop + windowHeight - containerTop) / (windowHeight + containerHeight);
                const parallaxOffset = (progress - 0.5) * 20; // Subtle parallax effect
                
                this.cards.forEach((card, index) => {
                    const cardOffset = parallaxOffset * (1 + index * 0.1);
                    card.style.setProperty('--scroll-offset', `${cardOffset}px`);
                });
                
                this.container.classList.add('parallax');
            } else {
                this.container.classList.remove('parallax');
            }
            
            ticking = false;
        };
        
        const requestParallaxUpdate = () => {
            if (!ticking) {
                requestAnimationFrame(updateParallax);
                ticking = true;
            }
        };
        
        window.addEventListener('scroll', requestParallaxUpdate, { passive: true });
    }
    
    setupIntersectionObserver() {
        if (!('IntersectionObserver' in window)) return;
        
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '50px'
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                    this.startCardSequenceAnimation(entry.target);
                } else {
                    entry.target.classList.remove('animate-in');
                }
            });
        }, observerOptions);
        
        this.cards.forEach(card => observer.observe(card));
    }
    
    startCardSequenceAnimation(container) {
        const cards = container.querySelectorAll('.desktop-category-card');
        
        cards.forEach((card, index) => {
            setTimeout(() => {
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
                
                // Add bounce effect
                setTimeout(() => {
                    card.style.transform = 'translateY(-5px)';
                    setTimeout(() => {
                        card.style.transform = 'translateY(0)';
                    }, 150);
                }, 100);
            }, index * 100);
        });
    }
    
    setupCardAnimations() {
        this.cards.forEach(card => {
            // Enhanced hover effects
            card.addEventListener('mouseenter', (e) => this.handleCardHover(e, true));
            card.addEventListener('mouseleave', (e) => this.handleCardHover(e, false));
            
            // Click animation
            card.addEventListener('click', (e) => this.handleCardClick(e));
            
            // Focus effects for accessibility
            card.addEventListener('focus', (e) => this.handleCardFocus(e, true));
            card.addEventListener('blur', (e) => this.handleCardFocus(e, false));
        });
    }
    
    handleCardHover(e, isEntering) {
        const card = e.currentTarget;
        const image = card.querySelector('.desktop-category-image, .desktop-category-icon');
        const name = card.querySelector('.desktop-category-name');
        const count = card.querySelector('.desktop-category-count');
        
        if (isEntering) {
            // Add magnetic effect to nearby cards
            this.addMagneticEffect(card);
            
            // Enhance the hovered card
            card.style.zIndex = '10';
            
            // Add subtle rotation based on mouse position
            const rect = card.getBoundingClientRect();
            const centerX = rect.left + rect.width / 2;
            const centerY = rect.top + rect.height / 2;
            
            card.addEventListener('mousemove', (e) => {
                const mouseX = e.clientX;
                const mouseY = e.clientY;
                
                const rotateX = (mouseY - centerY) / 10;
                const rotateY = (centerX - mouseX) / 10;
                
                card.style.transform = `translateY(-12px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.02)`;
            });
            
        } else {
            // Reset effects
            this.removeMagneticEffect();
            card.style.zIndex = '';
            card.style.transform = '';
            card.removeEventListener('mousemove', () => {});
        }
    }
    
    addMagneticEffect(hoveredCard) {
        this.cards.forEach(card => {
            if (card !== hoveredCard) {
                const distance = this.getDistance(hoveredCard, card);
                if (distance < 300) { // Magnetic range
                    const force = Math.max(0, (300 - distance) / 300);
                    const angle = this.getAngle(hoveredCard, card);
                    
                    const offsetX = Math.cos(angle) * force * 10;
                    const offsetY = Math.sin(angle) * force * 10;
                    
                    card.style.transform = `translate(${offsetX}px, ${offsetY}px) scale(${1 - force * 0.05})`;
                    card.style.opacity = 1 - force * 0.2;
                }
            }
        });
    }
    
    removeMagneticEffect() {
        this.cards.forEach(card => {
            card.style.transform = '';
            card.style.opacity = '';
        });
    }
    
    getDistance(el1, el2) {
        const rect1 = el1.getBoundingClientRect();
        const rect2 = el2.getBoundingClientRect();
        
        const centerX1 = rect1.left + rect1.width / 2;
        const centerY1 = rect1.top + rect1.height / 2;
        const centerX2 = rect2.left + rect2.width / 2;
        const centerY2 = rect2.top + rect2.height / 2;
        
        return Math.sqrt(Math.pow(centerX2 - centerX1, 2) + Math.pow(centerY2 - centerY1, 2));
    }
    
    getAngle(el1, el2) {
        const rect1 = el1.getBoundingClientRect();
        const rect2 = el2.getBoundingClientRect();
        
        const centerX1 = rect1.left + rect1.width / 2;
        const centerY1 = rect1.top + rect1.height / 2;
        const centerX2 = rect2.left + rect2.width / 2;
        const centerY2 = rect2.top + rect2.height / 2;
        
        return Math.atan2(centerY2 - centerY1, centerX2 - centerX1);
    }
    
    handleCardClick(e) {
        const card = e.currentTarget;
        
        // Ripple effect
        const ripple = document.createElement('div');
        ripple.style.position = 'absolute';
        ripple.style.borderRadius = '50%';
        ripple.style.background = 'rgba(13, 110, 253, 0.3)';
        ripple.style.transform = 'scale(0)';
        ripple.style.animation = 'ripple 0.6s linear';
        ripple.style.pointerEvents = 'none';
        
        const rect = card.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;
        
        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        
        card.style.position = 'relative';
        card.appendChild(ripple);
        
        setTimeout(() => {
            ripple.remove();
        }, 600);
        
        // Add to CSS
        if (!document.getElementById('ripple-keyframes')) {
            const style = document.createElement('style');
            style.id = 'ripple-keyframes';
            style.textContent = `
                @keyframes ripple {
                    to {
                        transform: scale(2);
                        opacity: 0;
                    }
                }
            `;
            document.head.appendChild(style);
        }
    }
    
    handleCardFocus(e, isFocusing) {
        const card = e.currentTarget;
        
        if (isFocusing) {
            card.style.transform = 'translateY(-8px) scale(1.02)';
            card.style.boxShadow = '0 15px 30px rgba(13, 110, 253, 0.2)';
        } else {
            card.style.transform = '';
            card.style.boxShadow = '';
        }
    }
    
    setupAutoPlay() {
        // Auto-rotate category highlights
        let currentHighlight = 0;
        
        const highlightNext = () => {
            if (this.cards.length === 0) return;
            
            // Remove previous highlight
            this.cards.forEach(card => card.classList.remove('auto-highlight'));
            
            // Add highlight to current card
            this.cards[currentHighlight]?.classList.add('auto-highlight');
            
            currentHighlight = (currentHighlight + 1) % this.cards.length;
        };
        
        // Start auto-highlight
        if (this.isAutoPlaying && this.cards.length > 0) {
            this.autoPlayInterval = setInterval(highlightNext, 3000);
        }
        
        // Pause on hover
        this.container?.addEventListener('mouseenter', () => {
            if (this.autoPlayInterval) {
                clearInterval(this.autoPlayInterval);
            }
        });
        
        // Resume on leave
        this.container?.addEventListener('mouseleave', () => {
            if (this.isAutoPlaying) {
                this.autoPlayInterval = setInterval(highlightNext, 3000);
            }
        });
    }
    
    setupKeyboardNavigation() {
        document.addEventListener('keydown', (e) => {
            if (!this.container?.matches(':hover')) return;
            
            switch(e.key) {
                case 'ArrowLeft':
                    e.preventDefault();
                    this.navigateCarousel('prev');
                    break;
                case 'ArrowRight':
                    e.preventDefault();
                    this.navigateCarousel('next');
                    break;
                case 'Home':
                    e.preventDefault();
                    this.focusCard(0);
                    break;
                case 'End':
                    e.preventDefault();
                    this.focusCard(this.cards.length - 1);
                    break;
            }
        });
    }
    
    navigateCarousel(direction) {
        // Implementation for carousel navigation
        const carousel = document.querySelector('#categoriesCarousel');
        if (carousel) {
            const bsCarousel = bootstrap.Carousel.getInstance(carousel) || new bootstrap.Carousel(carousel);
            direction === 'next' ? bsCarousel.next() : bsCarousel.prev();
        }
    }
    
    focusCard(index) {
        if (this.cards[index]) {
            this.cards[index].focus();
        }
    }
    
    addPerformanceOptimizations() {
        // Reduce motion for users who prefer it
        if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
            this.cards.forEach(card => {
                card.style.transition = 'none';
            });
        }
        
        // Optimize for low-end devices
        if (navigator.hardwareConcurrency && navigator.hardwareConcurrency <= 2) {
            this.container?.classList.add('low-performance');
        }
        
        // Disable parallax on mobile
        if (window.innerWidth < 992) {
            this.container?.classList.add('no-parallax');
        }
    }
}

// Auto-highlight animation CSS
const autoHighlightCSS = `
.desktop-category-card.auto-highlight {
    animation: autoHighlight 1s ease-in-out;
}

@keyframes autoHighlight {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-8px) scale(1.02); }
}

.low-performance .desktop-category-card {
    transition: transform 0.2s ease, box-shadow 0.2s ease !important;
}

.no-parallax .desktop-category-card {
    transform: none !important;
}
`;

// Intersection Observer for performance
const observerCSS = `
.desktop-category-card {
    opacity: 0;
    transform: translateY(30px);
    transition: opacity 0.6s ease, transform 0.6s ease;
}

.desktop-category-card.animate-in {
    opacity: 1;
    transform: translateY(0);
}
`;

// Add CSS to document
document.addEventListener('DOMContentLoaded', function() {
    const style = document.createElement('style');
    style.textContent = autoHighlightCSS + observerCSS;
    document.head.appendChild(style);
    
    // Initialize desktop categories enhancer
    if (window.innerWidth >= 992) {
        new DesktopCategoriesEnhancer();
    }
    
    // Reinitialize on window resize
    let resizeTimeout;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(() => {
            if (window.innerWidth >= 992) {
                new DesktopCategoriesEnhancer();
            }
        }, 250);
    });
});

// Preload category images for better performance
function preloadDesktopCategoryImages() {
    const images = document.querySelectorAll('.desktop-category-image');
    images.forEach(img => {
        if (img.dataset.src) {
            const preloadImg = new Image();
            preloadImg.src = img.dataset.src;
        }
    });
}

// Lazy loading for better performance
function setupLazyLoading() {
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.classList.remove('lazy');
                        observer.unobserve(img);
                    }
                }
            });
        });
        
        document.querySelectorAll('.desktop-category-image.lazy').forEach(img => {
            imageObserver.observe(img);
        });
    }
}

document.addEventListener('DOMContentLoaded', function() {
    preloadDesktopCategoryImages();
    setupLazyLoading();
});
