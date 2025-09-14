// Desktop Categories Carousel JavaScript
document.addEventListener('DOMContentLoaded', function() {
    const carousel = document.querySelector('.desktop-categories-carousel');
    const track = document.querySelector('.desktop-categories-track');
    const prevBtn = document.querySelector('#prevCategories');
    const nextBtn = document.querySelector('#nextCategories');
    
    if (!carousel || !track) return;
    
    let currentIndex = 0;
    const cards = track.querySelectorAll('.desktop-category-item');
    const cardWidth = cards[0] ? cards[0].offsetWidth : 200;
    const gap = 24; // 1.5rem in pixels
    const visibleCards = Math.floor(carousel.offsetWidth / (cardWidth + gap));
    const maxIndex = Math.max(0, cards.length - visibleCards);
    
    console.log('Desktop carousel initialized:', { cards: cards.length, visibleCards, maxIndex });
    
    // Update carousel position
    function updateCarousel() {
        const translateX = -(currentIndex * (cardWidth + gap));
        track.style.transform = `translateX(${translateX}px)`;
        
        // Update button states
        if (prevBtn) {
            prevBtn.style.opacity = currentIndex === 0 ? '0.5' : '1';
            prevBtn.style.pointerEvents = currentIndex === 0 ? 'none' : 'auto';
        }
        
        if (nextBtn) {
            nextBtn.style.opacity = currentIndex >= maxIndex ? '0.5' : '1';
            nextBtn.style.pointerEvents = currentIndex >= maxIndex ? 'none' : 'auto';
        }
        
        console.log('Desktop carousel updated:', { currentIndex, maxIndex });
    }
    
    // Navigation event listeners
    if (prevBtn) {
        prevBtn.addEventListener('click', function(e) {
            e.preventDefault();
            console.log('Desktop prev clicked');
            if (currentIndex > 0) {
                currentIndex--;
                updateCarousel();
            }
        });
    }
    
    if (nextBtn) {
        nextBtn.addEventListener('click', function(e) {
            e.preventDefault();
            console.log('Desktop next clicked');
            if (currentIndex < maxIndex) {
                currentIndex++;
                updateCarousel();
            }
        });
    }
    
    // Touch/swipe support
    let startX = 0;
    let endX = 0;
    let isDragging = false;
    
    track.addEventListener('touchstart', function(e) {
        startX = e.touches[0].clientX;
        isDragging = true;
        track.style.transition = 'none';
    });
    
    track.addEventListener('touchmove', function(e) {
        if (!isDragging) return;
        endX = e.touches[0].clientX;
        const diff = startX - endX;
        const currentTranslate = -(currentIndex * (cardWidth + gap));
        track.style.transform = `translateX(${currentTranslate - diff}px)`;
    });
    
    track.addEventListener('touchend', function() {
        if (!isDragging) return;
        isDragging = false;
        track.style.transition = 'transform 0.3s ease';
        
        const diff = startX - endX;
        const threshold = cardWidth / 3;
        
        if (Math.abs(diff) > threshold) {
            if (diff > 0 && currentIndex < maxIndex) {
                currentIndex++;
            } else if (diff < 0 && currentIndex > 0) {
                currentIndex--;
            }
        }
        
        updateCarousel();
    });
    
    // Mouse drag support for desktop
    let mouseDown = false;
    let mouseStartX = 0;
    
    track.addEventListener('mousedown', function(e) {
        mouseDown = true;
        mouseStartX = e.clientX;
        track.style.cursor = 'grabbing';
        track.style.transition = 'none';
        e.preventDefault();
    });
    
    document.addEventListener('mousemove', function(e) {
        if (!mouseDown) return;
        const diff = mouseStartX - e.clientX;
        const currentTranslate = -(currentIndex * (cardWidth + gap));
        track.style.transform = `translateX(${currentTranslate - diff}px)`;
    });
    
    document.addEventListener('mouseup', function(e) {
        if (!mouseDown) return;
        mouseDown = false;
        track.style.cursor = 'grab';
        track.style.transition = 'transform 0.3s ease';
        
        const diff = mouseStartX - e.clientX;
        const threshold = cardWidth / 3;
        
        if (Math.abs(diff) > threshold) {
            if (diff > 0 && currentIndex < maxIndex) {
                currentIndex++;
            } else if (diff < 0 && currentIndex > 0) {
                currentIndex--;
            }
        }
        
        updateCarousel();
    });
    
    // Keyboard navigation
    document.addEventListener('keydown', function(e) {
        if (e.key === 'ArrowLeft' && currentIndex > 0) {
            currentIndex--;
            updateCarousel();
        } else if (e.key === 'ArrowRight' && currentIndex < maxIndex) {
            currentIndex++;
            updateCarousel();
        }
    });
    
    // Auto-play functionality (optional)
    let autoPlayInterval;
    
    function startAutoPlay() {
        autoPlayInterval = setInterval(() => {
            if (currentIndex < maxIndex) {
                currentIndex++;
            } else {
                currentIndex = 0;
            }
            updateCarousel();
        }, 5000);
    }
    
    function stopAutoPlay() {
        clearInterval(autoPlayInterval);
    }
    
    // Start auto-play and pause on hover
    if (cards.length > visibleCards) {
        startAutoPlay();
        
        carousel.addEventListener('mouseenter', stopAutoPlay);
        carousel.addEventListener('mouseleave', startAutoPlay);
    }
    
    // Window resize handler
    window.addEventListener('resize', function() {
        const newVisibleCards = Math.floor(carousel.offsetWidth / (cardWidth + gap));
        const newMaxIndex = Math.max(0, cards.length - newVisibleCards);
        
        if (currentIndex > newMaxIndex) {
            currentIndex = newMaxIndex;
        }
        
        updateCarousel();
    });
    
    // Initialize
    updateCarousel();
    
    // Add smooth scroll indicators
    if (cards.length > visibleCards) {
        const indicators = document.createElement('div');
        indicators.className = 'carousel-indicators';
        indicators.style.cssText = `
            display: flex;
            justify-content: center;
            gap: 8px;
            margin-top: 1rem;
        `;
        
        for (let i = 0; i <= maxIndex; i++) {
            const dot = document.createElement('button');
            dot.style.cssText = `
                width: 8px;
                height: 8px;
                border-radius: 50%;
                border: none;
                background: ${i === 0 ? '#007bff' : '#dee2e6'};
                cursor: pointer;
                transition: background 0.3s ease;
            `;
            
            dot.addEventListener('click', function() {
                currentIndex = i;
                updateCarousel();
                
                // Update dot states
                indicators.querySelectorAll('button').forEach((btn, index) => {
                    btn.style.background = index === i ? '#007bff' : '#dee2e6';
                });
            });
            
            indicators.appendChild(dot);
        }
        
        carousel.appendChild(indicators);
    }
});
