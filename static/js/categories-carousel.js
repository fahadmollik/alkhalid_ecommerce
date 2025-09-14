// Categories Carousel JavaScript
document.addEventListener('DOMContentLoaded', function() {
    const track = document.getElementById('categoriesTrack');
    const prevBtn = document.getElementById('categoryPrevBtn');
    const nextBtn = document.getElementById('categoryNextBtn');
    const indicators = document.getElementById('categoryIndicators');
    
    if (!track) return;
    
    let currentIndex = 0;
    const items = track.querySelectorAll('.category-item');
    
    if (items.length === 0) return;
    
    // Calculate responsive item width and visible count
    function getResponsiveSettings() {
        const containerWidth = track.parentElement.offsetWidth;
        const itemWidth = items[0].offsetWidth;
        const gap = 15; // Gap between items
        const visibleCount = Math.floor(containerWidth / (itemWidth + gap));
        
        return {
            itemWidth: itemWidth + gap,
            visibleCount: Math.max(1, visibleCount),
            maxIndex: Math.max(0, items.length - visibleCount)
        };
    }
    
    let settings = getResponsiveSettings();
    
    // Update carousel position
    function updateCarousel() {
        const translateX = -(currentIndex * settings.itemWidth);
        track.style.transform = `translateX(${translateX}px)`;
        
        // Update button states
        if (prevBtn) {
            prevBtn.style.opacity = currentIndex === 0 ? '0.5' : '1';
            prevBtn.disabled = currentIndex === 0;
        }
        
        if (nextBtn) {
            nextBtn.style.opacity = currentIndex >= settings.maxIndex ? '0.5' : '1';
            nextBtn.disabled = currentIndex >= settings.maxIndex;
        }
        
        // Update indicators
        updateIndicators();
    }
    
    // Update indicators (mobile only)
    function updateIndicators() {
        if (!indicators) return;
        
        indicators.innerHTML = '';
        const totalPages = Math.ceil(items.length / settings.visibleCount);
        
        for (let i = 0; i < totalPages; i++) {
            const indicator = document.createElement('button');
            indicator.className = `indicator ${i === Math.floor(currentIndex / settings.visibleCount) ? 'active' : ''}`;
            indicator.setAttribute('aria-label', `Go to page ${i + 1}`);
            indicator.addEventListener('click', () => {
                currentIndex = i * settings.visibleCount;
                if (currentIndex > settings.maxIndex) currentIndex = settings.maxIndex;
                updateCarousel();
            });
            indicators.appendChild(indicator);
        }
    }
    
    // Navigation event listeners
    if (prevBtn) {
        prevBtn.addEventListener('click', function(e) {
            e.preventDefault();
            if (currentIndex > 0) {
                currentIndex--;
                updateCarousel();
            }
        });
    }
    
    if (nextBtn) {
        nextBtn.addEventListener('click', function(e) {
            e.preventDefault();
            if (currentIndex < settings.maxIndex) {
                currentIndex++;
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
        const translateX = -(currentIndex * settings.itemWidth) - diff;
        track.style.transform = `translateX(${translateX}px)`;
    }, { passive: true });
    
    track.addEventListener('touchend', function(e) {
        if (!isDragging) return;
        isDragging = false;
        
        const diff = startX - currentX;
        const threshold = 50; // Minimum swipe distance
        
        if (Math.abs(diff) > threshold) {
            if (diff > 0 && currentIndex < settings.maxIndex) {
                // Swipe left - next
                currentIndex++;
            } else if (diff < 0 && currentIndex > 0) {
                // Swipe right - previous
                currentIndex--;
            }
        }
        
        updateCarousel();
    }, { passive: true });
    
    // Auto-advance carousel (optional)
    let autoAdvanceInterval;
    
    function startAutoAdvance() {
        autoAdvanceInterval = setInterval(() => {
            if (currentIndex >= settings.maxIndex) {
                currentIndex = 0;
            } else {
                currentIndex++;
            }
            updateCarousel();
        }, 5000); // 5 seconds
    }
    
    function stopAutoAdvance() {
        if (autoAdvanceInterval) {
            clearInterval(autoAdvanceInterval);
        }
    }
    
    // Start auto-advance if there are enough items
    if (items.length > settings.visibleCount) {
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
        if (currentIndex > settings.maxIndex) {
            currentIndex = settings.maxIndex;
        }
        updateCarousel();
    });
    
    // Initialize carousel
    updateCarousel();
    
    console.log('Categories carousel initialized:', {
        items: items.length,
        visibleCount: settings.visibleCount,
        maxIndex: settings.maxIndex
    });
});