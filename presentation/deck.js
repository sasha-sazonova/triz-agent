(function(){
  const slides = Array.from(document.querySelectorAll('.slide'));
  const total = slides.length;
  const progress = document.getElementById('progressFill');
  const slideNo = document.getElementById('slideNo');
  const index = document.getElementById('index');
  const indexGrid = document.getElementById('indexGrid');
  let current = 0;
  let wheelLock = false;

  function pad(n){ return String(n).padStart(2,'0'); }

  function renderIndex(){
    indexGrid.innerHTML = '';
    slides.forEach((slide, i) => {
      const btn = document.createElement('button');
      btn.className = 'index-item';
      btn.type = 'button';
      const n = document.createElement('span');
      n.className = 'n';
      n.textContent = pad(i+1);
      const t = document.createElement('span');
      t.className = 't';
      t.textContent = slide.dataset.title || ('Слайд ' + (i+1));
      btn.appendChild(n); btn.appendChild(t);
      btn.addEventListener('click', () => { go(i); closeIndex(); });
      indexGrid.appendChild(btn);
    });
  }

  function go(n){
    if(n < 0) n = 0;
    if(n > total - 1) n = total - 1;
    slides[current].classList.remove('active');
    current = n;
    slides[current].classList.add('active');
    document.body.classList.toggle('on-dark', slides[current].classList.contains('dark'));
    progress.style.width = ((current + 1) / total * 100) + '%';
    slideNo.textContent = pad(current + 1);
    try { history.replaceState(null, '', '#s' + (current + 1)); } catch(e) {}
  }

  function closeIndex(){ index.classList.remove('open'); }
  function toggleIndex(){ index.classList.toggle('open'); }

  function fromHash(){
    const m = location.hash.match(/^#s(\d+)$/);
    if(m){
      const n = parseInt(m[1],10) - 1;
      if(n >= 0 && n < total) return n;
    }
    return 0;
  }

  document.addEventListener('keydown', (e) => {
    if(e.key === 'Escape'){ toggleIndex(); return; }
    if(index.classList.contains('open')) return;
    if(e.key === 'ArrowRight' || e.key === 'ArrowDown' || e.key === ' ' || e.key === 'PageDown'){ e.preventDefault(); go(current + 1); }
    else if(e.key === 'ArrowLeft' || e.key === 'ArrowUp' || e.key === 'PageUp'){ e.preventDefault(); go(current - 1); }
    else if(e.key === 'Home'){ e.preventDefault(); go(0); }
    else if(e.key === 'End'){ e.preventDefault(); go(total - 1); }
    else if(e.key === 'b' || e.key === 'B'){ document.body.classList.toggle('static'); }
  });

  window.addEventListener('wheel', (e) => {
    if(index.classList.contains('open')) return;
    if(Math.abs(e.deltaY) < 24) return;
    if(wheelLock) return;
    wheelLock = true;
    if(e.deltaY > 0) go(current + 1); else go(current - 1);
    setTimeout(() => { wheelLock = false; }, 900);
  }, {passive:true});

  let touchStartX = null;
  let touchStartY = null;
  window.addEventListener('touchstart', (e) => {
    if(e.touches.length === 1){ touchStartX = e.touches[0].clientX; touchStartY = e.touches[0].clientY; }
  }, {passive:true});
  window.addEventListener('touchend', (e) => {
    if(touchStartX === null) return;
    const dx = e.changedTouches[0].clientX - touchStartX;
    const dy = e.changedTouches[0].clientY - touchStartY;
    if(Math.abs(dx) > 48 && Math.abs(dx) > Math.abs(dy)){ if(dx < 0) go(current + 1); else go(current - 1); }
    touchStartX = null; touchStartY = null;
  }, {passive:true});

  renderIndex();
  current = fromHash();
  slides.forEach((s,i) => s.classList.toggle('active', i === current));
  document.body.classList.toggle('on-dark', slides[current].classList.contains('dark'));
  progress.style.width = ((current + 1) / total * 100) + '%';
  slideNo.textContent = pad(current + 1);
  requestAnimationFrame(() => document.body.classList.add('ready'));
})();