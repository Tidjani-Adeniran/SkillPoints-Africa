document.addEventListener('DOMContentLoaded', function() {
    // 1. MOBILE HAMBURGER MENU TOGGLE SYSTEM
    const menuToggle = document.getElementById('menu-toggle');
    const navContainer = document.getElementById('nav-container');

    if (menuToggle && navContainer) {
        menuToggle.addEventListener('click', function() {
            navContainer.classList.toggle('active');
            
            const icon = menuToggle.querySelector('i');
            if (navContainer.classList.contains('active')) {
                icon.classList.remove('fa-bars');
                icon.classList.add('fa-xmark');
            } else {
                icon.classList.remove('fa-xmark');
                icon.classList.add('fa-bars');
            }
        });
    }

    // 2. LOGOUT CONFIRMATION DIALOG INTERCEPTOR
    // This targets the secure form in your navbar to prevent accidental logouts
    const logoutForm = document.querySelector('form[action*="logout"]');
    
    if (logoutForm) {
        logoutForm.addEventListener('submit', function(event) {
            // Trigger browser native confirmation modal
            const confirmLogout = confirm("ARE YOU SURE you want to logout?");
            
            // If the user clicks 'Cancel' (false), halt the form submit action completely
            if (!confirmLogout) {
                event.preventDefault();
            }
        });
    }
});