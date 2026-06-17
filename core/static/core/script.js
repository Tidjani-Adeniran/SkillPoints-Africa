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



// core/static/script.js
document.addEventListener("DOMContentLoaded", function() {
  
  // 1. Identify if the user is actively waiting for an admin review
  const hasPendingTasks = document.body.innerHTML.includes("Assignment Under Review") || 
                          document.body.innerHTML.includes("UNDER REVIEW");

  if (hasPendingTasks) {
    console.log("Active review pending detected. Live status polling initialized...");
    
    // 2. Poll the server in the background every 4 seconds
    const statusInterval = setInterval(function() {
      
      fetch(window.location.href, {
        method: 'GET',
        headers: {
          'X-Requested-With': 'XMLHttpRequest'
        }
      })
      .then(response => {
        if (!response.ok) throw new Error('Network response failure.');
        return response.text();
      })
      .then(htmlString => {
        const parser = new DOMParser();
        const freshDoc = parser.parseFromString(htmlString, 'text/html');
        
        const stillPending = freshDoc.body.innerHTML.includes("Assignment Under Review") || 
                             freshDoc.body.innerHTML.includes("UNDER REVIEW");

        // 3. If it's no longer pending, auto-reload the workspace UI!
        if (!stillPending) {
          console.log("Status modification detected! Syncing workspace view...");
          clearInterval(statusInterval);
          window.location.reload();
        }
      })
      .catch(err => console.warn('Background sync status polling paused:', err));
      
    }, 4000);
  }
});