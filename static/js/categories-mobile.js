// Categories Menu for Mobile Devices
document.addEventListener('DOMContentLoaded', function() {
    const categoriesToggle = document.getElementById('categoriesMenuToggle');
    const categoriesSidebar = document.getElementById('categoriesSidebar');
    const categoriesOverlay = document.getElementById('categoriesOverlay');
    const closeCategoriesMenu = document.getElementById('closeCategoriesMenu');
    
    // Toggle categories menu
    if (categoriesToggle) {
        categoriesToggle.addEventListener('click', function() {
            categoriesSidebar.classList.add('show');
            categoriesOverlay.classList.add('show');
            document.body.style.overflow = 'hidden'; // Prevent body scrolling
        });
    }
    
    // Close menu on overlay click
    if (categoriesOverlay) {
        categoriesOverlay.addEventListener('click', function() {
            categoriesSidebar.classList.remove('show');
            categoriesOverlay.classList.remove('show');
            document.body.style.overflow = ''; // Restore body scrolling
        });
    }
    
    // Close menu on close button click
    if (closeCategoriesMenu) {
        closeCategoriesMenu.addEventListener('click', function() {
            categoriesSidebar.classList.remove('show');
            categoriesOverlay.classList.remove('show');
            document.body.style.overflow = ''; // Restore body scrolling
        });
    }
    
    // Close menu on escape key press
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && categoriesSidebar.classList.contains('show')) {
            categoriesSidebar.classList.remove('show');
            categoriesOverlay.classList.remove('show');
            document.body.style.overflow = ''; // Restore body scrolling
        }
    });
    
    // Close menu on window resize (to desktop)
    window.addEventListener('resize', function() {
        if (window.innerWidth > 991 && categoriesSidebar.classList.contains('show')) {
            categoriesSidebar.classList.remove('show');
            categoriesOverlay.classList.remove('show');
            document.body.style.overflow = ''; // Restore body scrolling
        }
    });
});
