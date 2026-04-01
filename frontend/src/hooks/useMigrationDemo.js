import { useEffect } from 'react';

export function useMigrationDemo() {
  useEffect(() => {

    // ── Custom cursor ──────────────────────────────────────────────────────────
    const cursor = document.getElementById('cursor');
    const ring = document.getElementById('cursor-ring');
    let mx = 0, my = 0, rx = 0, ry = 0;
    
    if (cursor && ring) {
      document.addEventListener('mousemove', e => {
        mx = e.clientX; my = e.clientY;
        cursor.style.transform = `translate(${mx}px,${my}px) translate(-50%,-50%)`;
      });
      function animRing() {
        rx += (mx - rx) * .12; ry += (my - ry) * .12;
        ring.style.transform = `translate(${rx}px,${ry}px) translate(-50%,-50%)`;
        requestAnimationFrame(animRing);
      }
      animRing();
      document.querySelectorAll('a,button,.nav-links a').forEach(el => {
        el.addEventListener('mouseenter', () => {
          ring.style.width = '56px'; ring.style.height = '56px';
          ring.style.borderColor = 'rgba(255,107,26,.7)';
        });
        el.addEventListener('mouseleave', () => {
          ring.style.width = '32px'; ring.style.height = '32px';
          ring.style.borderColor = 'rgba(255,107,26,.4)';
        });
      });
    }

    // ── Scroll reveal ──────────────────────────────────────────────────────────
    const obs = new IntersectionObserver(entries => {
      entries.forEach(e => {
        if (e.isIntersecting) e.target.classList.add('visible');
      });
    }, { threshold: .12 });
    document.querySelectorAll('.reveal').forEach(el => obs.observe(el));

    // ── Laser burn reveal ──────────────────────────────────────────────────────
    (function() {
      function buildChars(el) {
        if (!el) return [];
        const text = el.textContent.trim();
        if (!text) return [];
        el.textContent = '';
        [...text].forEach(ch => {
          const s = document.createElement('span');
          s.className = 'char';
          s.textContent = ch;
          el.appendChild(s);
        });
        return [...el.querySelectorAll('.char')];
      }

      const l1 = document.getElementById('brand-line1');
      const l2 = document.getElementById('brand-line2');
      if (!l1 || !l2) return;

      const line1chars = buildChars(l1);
      const line2chars = buildChars(l2);
      const allChars = [...line1chars, ...line2chars];

      const laserDuration = 1600;
      const laserDelay    = 200;

      window.addEventListener('load', () => {
        const wrap = document.querySelector('.hero-brand-wrap');
        if (!wrap) return;
        const wrapRect = wrap.getBoundingClientRect();
        const totalWidth = wrapRect.width;

        allChars.forEach(ch => {
          const rect = ch.getBoundingClientRect();
          const charCenter = rect.left - wrapRect.left + rect.width / 2;
          const progress = charCenter / totalWidth;
          const fireAt = laserDelay + progress * laserDuration * 0.88;
          setTimeout(() => ch.classList.add('burned'), fireAt);
        });
      });
    })();
    
  }, []);
}
