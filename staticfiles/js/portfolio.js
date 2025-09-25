// Portfolio JavaScript File - Complete Version
// Author: Portfolio Template
// Description: All interactive functionality for the portfolio website

console.log('Portfolio JavaScript loading...');

// DOM Elements - Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded, initializing portfolio...');

    // Get DOM elements
    const burger = document.getElementById('burger');
    const navLinks = document.getElementById('navLinks');
    const faders = document.querySelectorAll('.fade-in');
    const sections = document.querySelectorAll('section[id]');
    const navLinksList = document.querySelectorAll('.nav-links a[href^="#"]');

    console.log('Found elements:', {
        burger: !!burger,
        navLinks: !!navLinks,
        fadeElements: faders.length,
        sections: sections.length,
        navLinks: navLinksList.length
    });

    // ========================================
    // SCROLL ANIMATIONS
    // ========================================

    // Make all fade-in elements visible immediately for debugging
    faders.forEach(el => {
        el.classList.add('visible');
        el.style.opacity = '1';
        el.style.transform = 'translateY(0)';
    });

    // Intersection Observer for animations
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                console.log('Element animated:', entry.target.id);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    faders.forEach(el => observer.observe(el));

    // ========================================
    // MOBILE MENU FUNCTIONALITY
    // ========================================

    if (burger && navLinks) {
        burger.addEventListener('click', function() {
            console.log('Burger menu clicked');
            navLinks.classList.toggle('active');

            // Animate burger menu
            const spans = burger.querySelectorAll('span');
            if (navLinks.classList.contains('active')) {
                spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
                spans[1].style.opacity = '0';
                spans[2].style.transform = 'rotate(-45deg) translate(7px, -6px)';
                console.log('Mobile menu opened');
            } else {
                spans[0].style.transform = 'rotate(0)';
                spans[1].style.opacity = '1';
                spans[2].style.transform = 'rotate(0)';
                console.log('Mobile menu closed');
            }
        });

        // Close mobile menu when clicking on links
        navLinks.addEventListener('click', function(e) {
            if (e.target.tagName === 'A') {
                navLinks.classList.remove('active');
                const spans = burger.querySelectorAll('span');
                spans[0].style.transform = 'rotate(0)';
                spans[1].style.opacity = '1';
                spans[2].style.transform = 'rotate(0)';
                console.log('Mobile menu closed via link click');
            }
        });
    }

    // ========================================
    // SMOOTH SCROLLING
    // ========================================

    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const target = document.querySelector(targetId);

            if (target) {
                const nav = document.querySelector('nav');
                const navHeight = nav ? nav.offsetHeight : 80;
                const targetPosition = target.offsetTop - navHeight - 20; // 20px extra offset

                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });

                console.log('Smooth scrolled to:', targetId);

                // Close mobile menu if open
                if (navLinks && navLinks.classList.contains('active')) {
                    navLinks.classList.remove('active');
                    const spans = burger ? burger.querySelectorAll('span') : [];
                    spans.forEach((span, index) => {
                        if (index === 0) span.style.transform = 'rotate(0)';
                        if (index === 1) span.style.opacity = '1';
                        if (index === 2) span.style.transform = 'rotate(0)';
                    });
                }
            }
        });
    });

    // ========================================
    // NAVBAR SCROLL EFFECTS
    // ========================================

    let ticking = false;

    function updateNavbar() {
        let current = '';
        const scrollPos = window.scrollY + 100;

        // Find current section
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.offsetHeight;

            if (scrollPos >= sectionTop && scrollPos < sectionTop + sectionHeight) {
                current = section.getAttribute('id');
            }
        });

        // Update active nav link
        navLinksList.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active');
            }
        });

        // Update navbar background
        const nav = document.querySelector('nav');
        if (nav) {
            if (window.scrollY > 100) {
                nav.style.background = 'rgba(10, 10, 11, 0.95)';
            } else {
                nav.style.background = 'rgba(10, 10, 11, 0.9)';
            }
        }

        ticking = false;
    }

    window.addEventListener('scroll', function() {
        if (!ticking) {
            requestAnimationFrame(updateNavbar);
            ticking = true;
        }
    });

    // ========================================
    // TYPING EFFECT (Optional)
    // ========================================

    function typeWriter(element, text, speed = 80) {
        if (!element) return;

        let i = 0;
        element.innerHTML = '';
        element.style.borderRight = '2px solid var(--accent-primary)';

        function type() {
            if (i < text.length) {
                element.innerHTML += text.charAt(i);
                i++;
                setTimeout(type, speed);
            } else {
                setTimeout(() => {
                    element.style.borderRight = 'none';
                }, 500);
            }
        }
        type();
    }

    // Uncomment to enable typing effect
    /*
    const heroTitle = document.querySelector('.hero-title');
    if (heroTitle) {
        const originalText = heroTitle.textContent;
        setTimeout(() => {
            typeWriter(heroTitle, originalText, 80);
        }, 1000);
    }
    */

    // ========================================
    // PARTICLE EFFECTS
    // ========================================

    function createParticle() {
        const particle = document.createElement('div');
        particle.style.cssText = `
            position: fixed;
            width: 4px;
            height: 4px;
            background: var(--accent-primary);
            border-radius: 50%;
            pointer-events: none;
            opacity: 0.6;
            left: ${Math.random() * window.innerWidth}px;
            top: ${window.innerHeight}px;
            z-index: 1;
        `;

        document.body.appendChild(particle);

        const animation = particle.animate([
            { transform: 'translateY(0px)', opacity: 0.6 },
            { transform: `translateY(-${window.innerHeight + 100}px)`, opacity: 0 }
        ], {
            duration: Math.random() * 3000 + 2000,
            easing: 'linear'
        });

        animation.onfinish = () => {
            if (particle.parentNode) {
                particle.parentNode.removeChild(particle);
            }
        };
    }

    // Create particles periodically (reduced frequency for performance)
    setInterval(createParticle, 2000);

    // ========================================
    // PROJECT CARD HOVER EFFECTS
    // ========================================

    document.querySelectorAll('.project').forEach(project => {
        project.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px)';
        });

        project.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // ========================================
    // FORM HANDLING
    // ========================================

    const form = document.querySelector('form[method="POST"]');
    if (form) {
        form.addEventListener('submit', function(e) {
            // Don't prevent default - let Django handle the form submission
            const button = this.querySelector('button[type="submit"]');
            if (button) {
                const originalText = button.innerHTML;

                button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
                button.disabled = true;

                // Re-enable button after a delay (in case of errors)
                setTimeout(() => {
                    if (button.disabled) {
                        button.innerHTML = originalText;
                        button.disabled = false;
                    }
                }, 10000); // 10 seconds timeout
            }
        });
    }

    // ========================================
    // PARALLAX EFFECT (Subtle)
    // ========================================

    let parallaxTicking = false;

    function updateParallax() {
        const scrolled = window.pageYOffset;
        const heroContent = document.querySelector('.hero-content');

        if (heroContent && scrolled < window.innerHeight) {
            heroContent.style.transform = `translateY(${scrolled * 0.3}px)`;
        }

        parallaxTicking = false;
    }

    window.addEventListener('scroll', function() {
        if (!parallaxTicking) {
            requestAnimationFrame(updateParallax);
            parallaxTicking = true;
        }
    });

    // ========================================
    // SKILL BADGES ANIMATION
    // ========================================

    const skillBadges = document.querySelectorAll('.skill-badge');
    const skillObserver = new IntersectionObserver(entries => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                    entry.target.style.animation = 'fadeInUp 0.6s ease forwards';
                }, index * 100);
                skillObserver.unobserve(entry.target);
            }
        });
    });

    skillBadges.forEach(badge => {
        badge.style.opacity = '0';
        badge.style.transform = 'translateY(20px)';
        skillObserver.observe(badge);
    });

    // ========================================
    // IMAGE ERROR HANDLING
    // ========================================

    document.querySelectorAll('img').forEach(img => {
        img.addEventListener('error', function() {
            console.warn('Image failed to load:', this.src);
            if (!this.src.includes('placeholder') && !this.src.includes('via.placeholder')) {
                this.src = 'https://via.placeholder.com/400x220/667eea/ffffff?text=Image+Not+Found';
            }
        });

        img.addEventListener('load', function() {
            this.style.opacity = '1';
        });
    });

    // ========================================
    // PERFORMANCE UTILITIES
    // ========================================

    // Debounce function
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    // Throttle function
    function throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        }
    }

    // ========================================
    // LOADING ANIMATION REMOVAL
    // ========================================

    setTimeout(() => {
        const loader = document.querySelector('.loader');
        if (loader) {
            loader.style.opacity = '0';
            setTimeout(() => {
                loader.style.display = 'none';
            }, 300);
        }
    }, 500);

    // ========================================
    // CONSOLE SUCCESS MESSAGE
    // ========================================

    console.log('✅ Portfolio JavaScript initialized successfully!');
    console.log('📊 Performance metrics:', {
        fadeElements: faders.length,
        skillBadges: skillBadges.length,
        projects: document.querySelectorAll('.project').length,
        images: document.querySelectorAll('img').length
    });

}); // End of DOMContentLoaded

// ========================================
// GLOBAL ERROR HANDLING
// ========================================

window.addEventListener('error', function(e) {
    console.error('JavaScript error occurred:', e.error);
});

window.addEventListener('unhandledrejection', function(e) {
    console.error('Unhandled promise rejection:', e.reason);
});

// ========================================
// SERVICE WORKER (Optional - for PWA)
// ========================================

// Service Worker - Simple Cache Example

const CACHE_NAME = "portfolio-cache-v1";
const urlsToCache = [
  "/",               // asosiy sahifa
  "/static/css/portfolio.css",
  "/static/js/portfolio.js",
  "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css",
  "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Poppins:wght@300;400;500;600;700&display=swap"
];

// Install event
self.addEventListener("install", event => {
  console.log("✅ Service Worker installed");
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(urlsToCache);
    })
  );
});

// Activate event
self.addEventListener("activate", event => {
  console.log("⚡ Service Worker activated");
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.map(key => {
        if (key !== CACHE_NAME) {
          return caches.delete(key);
        }
      }))
    )
  );
});

// Fetch event
self.addEventListener("fetch", event => {
  event.respondWith(
    caches.match(event.request).then(response => {
      return response || fetch(event.request);
    })
  );
});
