/* Stratos: justified body text on every screen size.
   Card / section body copy is always justified (last line left, or centred for centred blocks), on desktop and on phones.
   The old "measure the gaps and fall back to left-aligned" check now only applies to hero text, short centred lead-ins and
   pull-quote callouts, which keep their previous behaviour so they never show "word     word" gaps.
   Re-runs on resize, after fonts load, and when tabs / FAQ items open. Without JavaScript the normal styles apply. */
(function () {
    'use strict';
    var SELECTOR = 'main p, .stratos-footer__brand p';
    var CLASSES = ['sj-j', 'sj-jc', 'sj-l', 'sj-c', 'sj-m'];
    var MAX_EXTRA_EM = 0.45;      /* largest extra gap allowed on any one line, in em */
    var MAX_AVG_EM = 0.3;        /* average extra gap across the paragraph */

    function clear(el) { CLASSES.forEach(function (c) { el.classList.remove(c); }); }

    function process(el) {
        if (el.classList.contains('eyebrow') || el.classList.contains('eyebrow-light')) return;
        if (el.children.length || el.childNodes.length !== 1 || el.firstChild.nodeType !== 3) return;   /* plain text paragraphs only */
        var text = el.firstChild.data;
        if (text.trim().length < 70) return;

        clear(el);
        var cs = window.getComputedStyle(el);
        var orig = cs.textAlign;                                    /* what the stylesheet wanted: center / left / justify */
        var centred = orig === 'center';
        var fs = parseFloat(cs.fontSize) || 16;
        var width = el.getBoundingClientRect().width - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
        if (!(width > 0)) return;                                   /* hidden right now; handled when it is shown */

        el.classList.add('sj-m');                                   /* measure left-aligned */
        var lines = {}, order = [], re = /\S+/g, m, range = document.createRange(), node = el.firstChild;
        while ((m = re.exec(text))) {
            range.setStart(node, m.index); range.setEnd(node, m.index + m[0].length);
            var r = range.getBoundingClientRect();
            if (!r.width) continue;
            var key = Math.round(r.top);
            if (!lines[key]) { lines[key] = { l: r.left, r: r.right, n: 0 }; order.push(key); }
            var ln = lines[key]; ln.l = Math.min(ln.l, r.left); ln.r = Math.max(ln.r, r.right); ln.n++;
        }
        var worst = 0, total = 0, count = 0;
        for (var i = 0; i < order.length - 1; i++) {                /* every line except the last */
            var L = lines[order[i]];
            if (L.n < 2) { worst = Infinity; break; }               /* a lone word on a line cannot be justified */
            var extra = Math.max(0, width - (L.r - L.l)) / (L.n - 1) / fs;
            worst = Math.max(worst, extra); total += extra; count++;
        }
        var avg = count ? total / count : 0;
        clear(el);
        var forceJustify = !centred && !el.classList.contains('callout');   /* body copy: always justified */
        /* centred section intros that run to 3+ lines are justified too (last line stays centred); hero text, footer and callouts stay centred */
        if (centred && order.length >= 3 && !el.closest('.page-banner, .stratos-footer, .clarity-banner') && !el.classList.contains('callout')) forceJustify = true;
        if (order.length < 2) { el.classList.add(centred ? 'sj-c' : (forceJustify ? 'sj-j' : 'sj-l')); return; }
        var ok = forceJustify || (worst <= MAX_EXTRA_EM && avg <= MAX_AVG_EM);
        el.classList.add(ok ? (centred ? 'sj-jc' : 'sj-j') : (centred ? 'sj-c' : 'sj-l'));
    }

    function run() { Array.prototype.forEach.call(document.querySelectorAll(SELECTOR), process); }

    var timer;
    function later(ms) { clearTimeout(timer); timer = setTimeout(run, ms); }

    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { later(60); });
    else later(60);
    window.addEventListener('load', function () { later(120); });
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { later(60); });
    window.addEventListener('resize', function () { later(200); });
    window.addEventListener('orientationchange', function () { later(300); });
    document.addEventListener('click', function () { later(150); }, true);
    document.addEventListener('toggle', function () { later(60); }, true);
})();
