// Categories Carousel JavaScript
document.addEventListener('DOMContentLoaded', function() {
    const track = document.getElementById('categoriesTrack');
    const prevBtn = document.getElementById('categoryPrevBtn');
    const nextBtn = document.getElementById('categoryNextBtn');
    const indicators = document.getElementById('categoryIndicators');
    
    if (!track) return;
    
    let currentSlide = 0;
    const items = track.querySelectorAll('.category-item');
    
    if (items.length === 0) return;
    
    // Get responsive settings for slides
    function getResponsiveSettings() {
        const containerWidth = track.parentElement.offsetWidth;
        const itemWidth = items[0].offsetWidth;
        const gap = 15;
        
        // Determine items per slide based on screen width
        let itemsPerSlide;
        if (containerWidth < 768) {
            itemsPerSlide = 4; // Mobile: 4 items per slide
        } else {
            itemsPerSlide = 6; // Desktop: 6 items per slide
        }
        
        const totalSlides = Math.ceil(items.length / itemsPerSlide);
        
        return {
            itemWidth: itemWidth + gap,
            itemsPerSlide: itemsPerSlide,
            totalSlides: totalSlides,
            maxSlide: totalSlides - 1
        };
    }
    
    let settings = getResponsiveSettings();
    
    // Update carousel position
    function updateCarousel() {
        const slideOffset = currentSlide * settings.itemsPerSlide;
        const translateX = -(slideOffset * settings.itemWidth);
        track.style.transform = `translateX(${translateX}px)`;
        
        // Update button states
        if (prevBtn) {
            prevBtn.style.opacity = currentSlide === 0 ? '0.5' : '1';
            prevBtn.disabled = currentSlide === 0;
        }
        
        if (nextBtn) {
            nextBtn.style.opacity = currentSlide >= settings.maxSlide ? '0.5' : '1';
            nextBtn.disabled = currentSlide >= settings.maxSlide;
        }
        
        // Update indicators
        updateIndicators();
    }
    
    // Update indicators
    function updateIndicators() {
        if (!indicators) return;
        
        indicators.innerHTML = '';
        
        for (let i = 0; i < settings.totalSlides; i++) {
            const indicator = document.createElement('button');
            indicator.className = `indicator ${i === currentSlide ? 'active' : ''}`;
            indicator.setAttribute('aria-label', `Go to slide ${i + 1}`);
            indicator.addEventListener('click', () => {
                currentSlide = i;
                updateCarousel();
            });
            indicators.appendChild(indicator);
        }
    }
    
    // Navigation event listeners
    if (prevBtn) {
        prevBtn.addEventListener('click', function(e) {
            e.preventDefault();
            if (currentSlide > 0) {
                currentSlide--;
                updateCarousel();
            }
        });
    }
    
    if (nextBtn) {
        nextBtn.addEventListener('click', function(e) {
            e.preventDefault();
            if (currentSlide < settings.maxSlide) {
                currentSlide++;
                updateCarousel();
            }
        });
    }
    
    // Touch/swipe support for mobile
    let startX = 0;
    let currentX = 0;
    let isDragging = false;
    
    track.addEventListener('touchstart', function(e) {
        startX = e.touches[0].clientX;
        isDragging = true;
    }, { passive: true });
    
    track.addEventListener('touchmove', function(e) {
        if (!isDragging) return;
        currentX = e.touches[0].clientX;
        const diff = startX - currentX;
        
        // Add visual feedback during swipe
        const slideOffset = currentSlide * settings.itemsPerSlide;
        const translateX = -(slideOffset * settings.itemWidth) - diff;
        track.style.transform = `translateX(${translateX}px)`;
    }, { passive: true });
    
    track.addEventListener('touchend', function(e) {
        if (!isDragging) return;
        isDragging = false;
        
        const diff = startX - currentX;
        const threshold = 50; // Minimum swipe distance
        
        if (Math.abs(diff) > threshold) {
            if (diff > 0 && currentSlide < settings.maxSlide) {
                // Swipe left - next slide
                currentSlide++;
            } else if (diff < 0 && currentSlide > 0) {
                // Swipe right - previous slide
                currentSlide--;
            }
        }
        
        updateCarousel();
    }, { passive: true });
    
    // Auto-advance carousel (optional)
    let autoAdvanceInterval;
    
    function startAutoAdvance() {
        autoAdvanceInterval = setInterval(() => {
            if (currentSlide >= settings.maxSlide) {
                currentSlide = 0;
            } else {
                currentSlide++;
            }
            updateCarousel();
        }, 5000); // 5 seconds
    }
    
    function stopAutoAdvance() {
        if (autoAdvanceInterval) {
            clearInterval(autoAdvanceInterval);
        }
    }
    
    // Start auto-advance if there are enough slides
    if (settings.totalSlides > 1) {
        startAutoAdvance();
        
        // Pause on hover
        track.addEventListener('mouseenter', stopAutoAdvance);
        track.addEventListener('mouseleave', startAutoAdvance);
        
        // Pause on focus
        track.addEventListener('focusin', stopAutoAdvance);
        track.addEventListener('focusout', startAutoAdvance);
    }
    
    // Handle window resize
    window.addEventListener('resize', function() {
        settings = getResponsiveSettings();
        if (currentSlide > settings.maxSlide) {
            currentSlide = settings.maxSlide;
        }
        updateCarousel();
    });
    
    // Initialize carousel
    updateCarousel();
    
    console.log('Categories carousel initialized:', {
        items: items.length,
        itemsPerSlide: settings.itemsPerSlide,
        totalSlides: settings.totalSlides,
        maxSlide: settings.maxSlide
    });
});