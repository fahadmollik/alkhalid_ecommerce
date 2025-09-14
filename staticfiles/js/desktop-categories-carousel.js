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
        
        // Determine items per slide based on screen width
        let itemsPerSlide;
        if (containerWidth < 576) {
            itemsPerSlide = 2; // Small mobile: 2 items per slide
        } else if (containerWidth < 768) {
            itemsPerSlide = 3; // Large mobile/small tablet: 3 items per slide
        } else {
            itemsPerSlide = 6; // Desktop: 6 items per slide
        }
        
        // Calculate slide width based on container
        const slideWidth = containerWidth;
        
        // Calculate ACTUAL total slides based on content
        const totalSlides = Math.ceil(items.length / itemsPerSlide);
        const maxSlide = Math.max(0, totalSlides - 1);
        
        return {
            slideWidth: slideWidth,
            itemsPerSlide: itemsPerSlide,
            totalSlides: totalSlides,
            maxSlide: maxSlide
        };
    }
    
    let settings = getResponsiveSettings();
    
    // Update carousel position
    function updateCarousel() {
        // Recalculate settings in case of window resize
        settings = getResponsiveSettings();
        
        // Ensure currentSlide doesn't exceed valid bounds
        currentSlide = Math.max(0, Math.min(currentSlide, settings.maxSlide));
        
        // Validate that current slide has content
        const slideStartItem = currentSlide * settings.itemsPerSlide;
        if (slideStartItem >= items.length && currentSlide > 0) {
            // Current slide has no content, go to last valid slide
            currentSlide = Math.floor((items.length - 1) / settings.itemsPerSlide);
        }
        
        // Calculate how many slides to skip
        const slidesToSkip = currentSlide;
        
        // Move by full container width per slide
        const translateX = -(slidesToSkip * settings.slideWidth);
        
        track.style.transform = `translateX(${translateX}px)`;
        
        // Update button states - check if next slide has content
        const hasNextSlide = (currentSlide + 1) * settings.itemsPerSlide < items.length;
        const hasPrevSlide = currentSlide > 0;
        
        if (prevBtn) {
            prevBtn.style.opacity = hasPrevSlide ? '1' : '0.5';
            prevBtn.disabled = !hasPrevSlide;
        }
        
        if (nextBtn) {
            nextBtn.style.opacity = hasNextSlide ? '1' : '0.5';
            nextBtn.disabled = !hasNextSlide;
        }
        
        // Hide navigation if all items fit in one view
        if (settings.totalSlides <= 1) {
            if (prevBtn) prevBtn.style.display = 'none';
            if (nextBtn) nextBtn.style.display = 'none';
        } else {
            if (prevBtn) prevBtn.style.display = 'flex';
            if (nextBtn) nextBtn.style.display = 'flex';
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
    }
    
    // Navigation event listeners
    if (prevBtn) {
        prevBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            if (currentSlide > 0) {
                currentSlide--;
                updateCarousel();
            }
        });
    }
    
    if (nextBtn) {
        nextBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            // Check if next slide would have content
            const nextSlideStartItem = (currentSlide + 1) * settings.itemsPerSlide;
            
            if (nextSlideStartItem < items.length) {
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
        
        // Calculate the maximum allowed translation (last slide position)
        const maxTranslateX = -(settings.maxSlide * settings.slideWidth);
        
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
            if (diff > 0) {
                // Swipe left - next slide (only if it has content)
                const nextSlideStartItem = (currentSlide + 1) * settings.itemsPerSlide;
                if (nextSlideStartItem < items.length) {
                    currentSlide++;
                }
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
            // Check if next slide would have content
            const nextSlideStartItem = (currentSlide + 1) * settings.itemsPerSlide;
            if (nextSlideStartItem >= items.length) {
                currentSlide = 0; // Go to first slide if next would be empty
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
});