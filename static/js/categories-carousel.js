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
        if (containerWidth < 576) {
            itemsPerSlide = 2; // Small mobile: 2 items per slide
        } else if (containerWidth < 768) {
            itemsPerSlide = 3; // Large mobile/small tablet: 3 items per slide
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
        // Ensure currentSlide doesn't exceed bounds
        currentSlide = Math.max(0, Math.min(currentSlide, settings.maxSlide));
        
        const slideOffset = currentSlide * settings.itemsPerSlide;
        
        // Calculate translateX with proper bounds checking
        let translateX = -(slideOffset * settings.itemWidth);
        
        // Ensure we don't scroll past the last item
        const maxTranslateX = -((items.length - settings.itemsPerSlide) * settings.itemWidth);
        if (translateX < maxTranslateX) {
            translateX = maxTranslateX;
        }
        
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
    
    // Update active indicator
    function updateIndicators() {
        if (!indicators) return;
        
        const indicatorDots = indicators.querySelectorAll('.indicator-dot');
        if (!indicatorDots.length) return;
        
        // Calculate which categories are currently visible
        const slideOffset = currentSlide * settings.itemsPerSlide;
        const startIndex = slideOffset;
        const endIndex = Math.min(startIndex + settings.itemsPerSlide, items.length);
        
        indicatorDots.forEach((indicator, index) => {
            // Check if this category is currently visible
            const isVisible = index >= startIndex && index < endIndex;
            
            if (isVisible) {
                indicator.classList.add('active');
            } else {
                indicator.classList.remove('active');
            }
        });
    }    // Navigation event listeners
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
    let startTime = 0;
    let startTranslateX = 0;
    
    track.addEventListener('touchstart', function(e) {
        startX = e.touches[0].clientX;
        startTime = Date.now();
        isDragging = true;
        
        // Get current translateX value
        const transform = window.getComputedStyle(track).transform;
        if (transform !== 'none') {
            const matrix = new DOMMatrix(transform);
            startTranslateX = matrix.e;
        } else {
            startTranslateX = 0;
        }
        
        track.style.transition = 'none'; // Disable transition during drag
    }, { passive: true });
    
    track.addEventListener('touchmove', function(e) {
        if (!isDragging) return;
        
        e.preventDefault();
        const currentX = e.touches[0].clientX;
        const deltaX = currentX - startX;
        
        // Calculate the maximum allowed translation
        const maxTranslateX = -((items.length - settings.itemsPerSlide) * settings.itemWidth);
        
        // Apply resistance when trying to go beyond boundaries
        let translateX = startTranslateX + deltaX;
        
        // Resist going beyond the left boundary (first item)
        if (translateX > 0) {
            translateX = deltaX * 0.3; // Apply resistance
        }
        // Resist going beyond the right boundary (last visible items)
        else if (translateX < maxTranslateX) {
            const overflow = maxTranslateX - translateX;
            translateX = maxTranslateX + overflow * 0.3; // Apply resistance
        }
        
        track.style.transform = `translateX(${translateX}px)`;
    }, { passive: false });
    
    track.addEventListener('touchend', function(e) {
        if (!isDragging) return;
        isDragging = false;
        
        track.style.transition = 'transform 0.3s ease'; // Re-enable transition
        
        const currentX = e.changedTouches[0].clientX;
        const diff = startX - currentX;
        const duration = Date.now() - startTime;
        const velocity = Math.abs(diff) / duration;
        
        // Lower threshold for fast swipes, higher for slow swipes
        const threshold = velocity > 0.5 ? 30 : 80;
        
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
        maxSlide: settings.maxSlide,
        containerWidth: track.parentElement.offsetWidth,
        isMobile: track.parentElement.offsetWidth < 768,
        paginationType: 'category-based'
    });
});