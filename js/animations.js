(function () {
  'use strict';

  var pref = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ── mark JS loaded so CSS reveal rules activate ── */
  document.body.classList.add('js-loaded');

  /* ─────────────────────────────────────────────────
     ANIMATION 1 — SCROLL FADE-IN
  ───────────────────────────────────────────────── */
  if (!pref) {
    /* Apply stagger delays to siblings in the same parent */
    var parents = [];
    document.querySelectorAll('.reveal').forEach(function (el) {
      if (parents.indexOf(el.parentElement) === -1) parents.push(el.parentElement);
    });
    parents.forEach(function (parent) {
      var siblings = parent.querySelectorAll('.reveal');
      if (siblings.length > 1) {
        siblings.forEach(function (el, i) {
          el.style.transitionDelay = (i * 0.1) + 's';
        });
      }
    });

    var revealObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          revealObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

    document.querySelectorAll('.reveal').forEach(function (el) {
      revealObserver.observe(el);
    });
  } else {
    document.querySelectorAll('.reveal').forEach(function (el) {
      el.classList.add('visible');
    });
  }

  /* ─────────────────────────────────────────────────
     ANIMATION 2 — FLOATING PARTICLES (hero canvas)
  ───────────────────────────────────────────────── */
  if (!pref) {
    var canvas = document.getElementById('particle-canvas');
    if (canvas) {
      var ctx = canvas.getContext('2d');
      var COUNT = 60;
      var MAX_DIST = 120;
      var particles = [];
      var rafId;

      function initParticles() {
        canvas.width  = canvas.offsetWidth  || canvas.parentElement.offsetWidth;
        canvas.height = canvas.offsetHeight || canvas.parentElement.offsetHeight;
        particles = [];
        for (var i = 0; i < COUNT; i++) {
          particles.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            r: 1.5 + Math.random() * 1,
            vx: (Math.random() - 0.5) * 0.4,
            vy: (Math.random() - 0.5) * 0.4,
            opacity: 0.15 + Math.random() * 0.1
          });
        }
      }

      function drawParticles() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        /* Connect nearby particles */
        for (var i = 0; i < particles.length; i++) {
          for (var j = i + 1; j < particles.length; j++) {
            var dx   = particles[i].x - particles[j].x;
            var dy   = particles[i].y - particles[j].y;
            var dist = Math.sqrt(dx * dx + dy * dy);
            if (dist < MAX_DIST) {
              ctx.strokeStyle = 'rgba(15,23,42,' + (0.07 * (1 - dist / MAX_DIST)) + ')';
              ctx.lineWidth = 0.6;
              ctx.beginPath();
              ctx.moveTo(particles[i].x, particles[i].y);
              ctx.lineTo(particles[j].x, particles[j].y);
              ctx.stroke();
            }
          }
        }

        /* Draw + move dots */
        particles.forEach(function (p) {
          ctx.fillStyle = 'rgba(15,23,42,' + p.opacity + ')';
          ctx.beginPath();
          ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
          ctx.fill();
          p.x += p.vx;
          p.y += p.vy;
          if (p.x < 0 || p.x > canvas.width)  p.vx *= -1;
          if (p.y < 0 || p.y > canvas.height) p.vy *= -1;
        });

        rafId = requestAnimationFrame(drawParticles);
      }

      var resizeTimer;
      window.addEventListener('resize', function () {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(function () {
          cancelAnimationFrame(rafId);
          initParticles();
          drawParticles();
        }, 150);
      });

      initParticles();
      drawParticles();
    }
  }

  /* ─────────────────────────────────────────────────
     ANIMATION 3 — SMOOTH PAGE TRANSITIONS
  ───────────────────────────────────────────────── */
  if (!pref) {
    document.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function (e) {
        var href = link.getAttribute('href');
        if (!href || href.charAt(0) === '#' || href.indexOf('mailto') === 0 ||
            link.target === '_blank') return;
        /* Only intercept same-origin .html links */
        if (href.indexOf('http') === 0 || href.indexOf('//') === 0) return;
        e.preventDefault();
        document.body.classList.add('page-exit');
        setTimeout(function () { window.location.href = href; }, 300);
      });
    });
  }

})();
