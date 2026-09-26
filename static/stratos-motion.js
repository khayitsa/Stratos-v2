/* Stratos - light motion layer.
   1. Sections fade/slide in as they scroll into view (staggered across cards).
   2. Proof-strip numbers count up once.
   Skipped entirely for visitors who ask their device for reduced motion, or if IntersectionObserver is missing. */
(function () {
    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reduce || !('IntersectionObserver' in window)) return;
    document.documentElement.classList.add('js-motion');

    var sel = '.band__head, .split__photo, .split__text, .svc-card, .info-card, .persona-card, .timeline__step, ' +
              '.faq-list details, .fit-panel, .fit-layout__text, .luxury-card, .editorial-card, .proof-item, ' +
              '.reach__map, .cta-band__content, .statement-strip p';
    var els = [].slice.call(document.querySelectorAll(sel));

    els.forEach(function (el) {
        var sibs = el.parentElement ? [].filter.call(el.parentElement.children, function (c) { return c.matches(sel); }) : [];
        var i = Math.max(0, sibs.indexOf(el));
        el.style.setProperty('--d', (Math.min(i, 5) * 0.08).toFixed(2) + 's');
        el.classList.add('reveal');
    });

    function countUp(el) {
        var m = /^(\d+)(.*)$/.exec(el.textContent.trim());
        if (!m) return;
        var target = parseInt(m[1], 10), rest = m[2], start = null, dur = 1100;
        function step(ts) {
            if (start === null) start = ts;
            var p = Math.min((ts - start) / dur, 1), eased = 1 - Math.pow(1 - p, 3);
            el.textContent = Math.round(target * eased) + rest;
            if (p < 1) requestAnimationFrame(step);
        }
        el.textContent = '0' + rest;
        requestAnimationFrame(step);
    }

    var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
            if (!e.isIntersecting) return;
            var el = e.target;
            el.classList.add('is-in');
            io.unobserve(el);
            var num = el.matches('.proof-item') ? el.querySelector('strong') : null;
            if (num) countUp(num);
            // drop the reveal classes afterwards so normal hover effects (lift, shadow) work again
            setTimeout(function () { el.classList.remove('reveal', 'is-in'); el.style.removeProperty('--d'); }, 1200);
        });
    }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });

    els.forEach(function (el) { io.observe(el); });

    /* ---- Cursor spotlight on cards: sets --mx / --my so the CSS glow follows the mouse ---- */
    document.addEventListener('pointermove', function (e) {
        var card = e.target.closest && e.target.closest('.svc-card, .info-card, .persona-card');
        if (!card) return;
        var r = card.getBoundingClientRect();
        card.style.setProperty('--mx', (e.clientX - r.left) + 'px');
        card.style.setProperty('--my', (e.clientY - r.top) + 'px');
    }, { passive: true });

    /* ---- Timeline rail draws itself when it scrolls into view ---- */
    var tio = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('tl-in'); tio.unobserve(en.target); } });
    }, { threshold: 0.25 });
    [].slice.call(document.querySelectorAll('.timeline')).forEach(function (t) { tio.observe(t); });
})();

/* Scroll cue on the home hero: disappears the moment the visitor scrolls (and stays gone). Runs even with reduced motion. */
(function () {
    var cue = document.querySelector('.scroll-cue');
    if (!cue) return;
    function hide() { cue.classList.add('is-gone'); window.removeEventListener('scroll', onScroll); }
    function onScroll() { if (window.scrollY > 40) hide(); }
    window.addEventListener('scroll', onScroll, { passive: true });
    cue.addEventListener('click', function (e) {
        var banner = cue.closest('section'), next = banner && banner.nextElementSibling;
        if (next) { e.preventDefault(); next.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
        setTimeout(hide, 50);
    });
    if (window.scrollY > 40) hide();
})();

/* Services showcase (home): click / arrow-key a service to open its panel. Without JS every panel simply stays listed. */
(function () {
    var box = document.querySelector('.svc-showcase');
    if (!box) return;
    var tabs = [].slice.call(box.querySelectorAll('.svc-tab'));
    var panels = [].slice.call(box.querySelectorAll('.svc-panel'));
    if (!tabs.length || tabs.length !== panels.length) return;
    box.classList.remove('no-js');
    function show(i, focus) {
        tabs.forEach(function (t, k) {
            var on = k === i;
            t.classList.toggle('is-active', on);
            t.setAttribute('aria-selected', on ? 'true' : 'false');
            t.tabIndex = on ? 0 : -1;
            panels[k].classList.toggle('is-active', on);
        });
        if (focus) tabs[i].focus();
    }
    tabs.forEach(function (t, i) {
        t.addEventListener('click', function () { show(i); });
        t.addEventListener('mouseenter', function () { if (window.matchMedia('(hover:hover)').matches && window.innerWidth > 960) show(i); });
        t.addEventListener('keydown', function (e) {
            var k = e.key;
            if (k === 'ArrowDown' || k === 'ArrowRight') { e.preventDefault(); show((i + 1) % tabs.length, true); }
            if (k === 'ArrowUp' || k === 'ArrowLeft') { e.preventDefault(); show((i - 1 + tabs.length) % tabs.length, true); }
        });
    });
    show(0);
})();
