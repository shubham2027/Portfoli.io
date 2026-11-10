/**
 * portfoli.io - Client-side Interactive Enhancements
 * Vanilla JavaScript (No React, No external frontend frameworks)
 */

document.addEventListener('DOMContentLoaded', () => {
    const navbar = document.querySelector('.custom-navbar');

    // 1. Navbar scroll effect (add elevation shadow on page scroll)
    if (navbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 20) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }

    // 2. Smooth anchor scrolling with offset for sticky navbar
    const anchorLinks = document.querySelectorAll('a[href*="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            const href = link.getAttribute('href');
            if (!href || href === '#' || href === '') return;

            const hashIndex = href.indexOf('#');
            if (hashIndex === -1) return;

            const pathPart = href.substring(0, hashIndex);
            const hashPart = href.substring(hashIndex);

            // Check if link points to an anchor on the current page
            const currentPath = window.location.pathname;
            const isSamePage = (pathPart === '' || pathPart === currentPath || (pathPart === '/' && (currentPath === '/' || currentPath === '')));

            if (isSamePage) {
                const targetElement = document.querySelector(hashPart);
                if (targetElement) {
                    e.preventDefault();
                    const navHeight = navbar ? navbar.offsetHeight : 0;
                    const elementPosition = targetElement.getBoundingClientRect().top;
                    const offsetPosition = elementPosition + window.pageYOffset - navHeight - 20;

                    window.scrollTo({
                        top: offsetPosition,
                        behavior: 'smooth'
                    });

                    // Update URL hash cleanly
                    history.pushState(null, null, hashPart);
                }
            }
        });
    });

    // 3. Auto offset scroll if page loaded with a hash in URL (e.g. from dashboard to /#features)
    if (window.location.hash) {
        setTimeout(() => {
            const targetElement = document.querySelector(window.location.hash);
            if (targetElement) {
                const navHeight = navbar ? navbar.offsetHeight : 0;
                const elementPosition = targetElement.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - navHeight - 20;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        }, 120);
    }

    // 4. Auto-dismiss alerts after 5 seconds if any exist
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(alert => {
        setTimeout(() => {
            try {
                const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
                bsAlert.close();
            } catch (err) {
                alert.style.transition = 'opacity 0.5s ease';
                alert.style.opacity = '0';
                setTimeout(() => alert.remove(), 500);
            }
        }, 5000);
    });
});
