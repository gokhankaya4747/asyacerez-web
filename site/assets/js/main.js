(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];

  // Header: şeffaf → dolu
  const header = $('.site-header');
  if (header && header.classList.contains('is-transparent')) {
    const onScroll = () => header.classList.toggle('is-scrolled', scrollY > 40);
    addEventListener('scroll', onScroll, { passive: true }); onScroll();
  }

  // Mobil menü
  const burger = $('.burger'), drawer = $('#drawer');
  if (burger && drawer) {
    const set = open => {
      burger.setAttribute('aria-expanded', open); drawer.hidden = !open;
      document.body.classList.toggle('menu-open', open);
      if (header) header.classList.toggle('is-scrolled', open || scrollY > 40);
    };
    burger.addEventListener('click', () => set(burger.getAttribute('aria-expanded') !== 'true'));
    addEventListener('keydown', e => { if (e.key === 'Escape') set(false); });
    matchMedia('(min-width:1021px)').addEventListener('change', e => e.matches && set(false));
  }

  // Scroll ile belirme (grup içinde kademeli)
  const rv = $$('.reveal');
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(entries => {
      entries.forEach(en => {
        if (!en.isIntersecting) return;
        const sibs = [...en.target.parentElement.children].filter(c => c.classList.contains('reveal'));
        en.target.style.setProperty('--rd', `${Math.min(sibs.indexOf(en.target), 6) * 0.08}s`);
        en.target.classList.add('is-in'); io.unobserve(en.target);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    rv.forEach(el => io.observe(el));
  } else rv.forEach(el => el.classList.add('is-in'));

  // Ürün filtre + arama
  const grid = $('#product-grid');
  if (grid) {
    const chips = $$('.fchip'), input = $('.search input'), empty = $('.empty');
    let cat = 'all';
    const norm = s => s.toLocaleLowerCase('tr').normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/ı/g, 'i');
    const apply = () => {
      const q = norm(input.value.trim()); let n = 0;
      $$('.pcard', grid).forEach(c => {
        const ok = (cat === 'all' || c.dataset.cat === cat) && (!q || norm(c.dataset.name).includes(q));
        c.classList.toggle('is-hidden', !ok); if (ok) { n++; c.classList.add('is-in'); }
      });
      empty.hidden = n > 0;
    };
    const pick = c => { cat = c; chips.forEach(b => b.classList.toggle('is-on', b.dataset.filter === c)); apply(); };
    chips.forEach(b => b.addEventListener('click', () => {
      pick(b.dataset.filter);
      history.replaceState(null, '', b.dataset.filter === 'all' ? location.pathname : '#' + b.dataset.filter);
    }));
    input.addEventListener('input', apply);
    const h = location.hash.slice(1);
    if (chips.some(b => b.dataset.filter === h)) pick(h);
  }

  // Ürün galerisi
  const main = $('#gal-main');
  $$('.gal__thumb').forEach(t => t.addEventListener('click', () => {
    if (t.classList.contains('is-on')) return;
    $$('.gal__thumb').forEach(x => x.classList.remove('is-on')); t.classList.add('is-on');
    main.classList.add('is-fading');
    const img = new Image(); img.src = t.dataset.src;
    img.onload = () => { main.src = t.dataset.src; main.classList.remove('is-fading'); };
  }));

  // Sekmeler
  const tabs = $$('.tab');
  tabs.forEach(tab => tab.addEventListener('click', () => {
    tabs.forEach(t => { const on = t === tab; t.classList.toggle('is-on', on); t.setAttribute('aria-selected', on);
      $('#' + t.getAttribute('aria-controls')).hidden = !on; });
  }));

  // Teklif formu
  const form = $('#quote-form');
  if (form) {
    const tr = form.dataset.lang === 'tr';
    const status = $('.qform__status', form);
    const p = new URLSearchParams(location.search).get('urun');
    if (p && form.product.querySelector(`option[value="${CSS.escape(p)}"]`)) form.product.value = p;
    form.addEventListener('submit', async e => {
      e.preventDefault();
      let ok = true;
      $$('[required]', form).forEach(f => {
        const bad = f.type === 'checkbox' ? !f.checked : !f.value.trim() || (f.type === 'email' && !/^\S+@\S+\.\S+$/.test(f.value));
        f.classList.toggle('is-invalid', bad); if (bad) ok = false;
      });
      if (!ok) { status.className = 'qform__status is-err'; status.textContent = tr ? 'Lütfen zorunlu alanları kontrol edin.' : 'Please check the required fields.'; return; }
      const d = Object.fromEntries(new FormData(form));
      const prod = form.product.selectedOptions[0]?.text || '';
      const lines = [
        `${tr ? 'Ad Soyad' : 'Name'}: ${d.name}`, `${tr ? 'Firma' : 'Company'}: ${d.company || '-'}`, `E-mail: ${d.email}`,
        `${tr ? 'Telefon' : 'Phone'}: ${d.phone || '-'}`, `${tr ? 'Ülke' : 'Country'}: ${d.country || '-'}`,
        `${tr ? 'Talep' : 'Request'}: ${d.type}`, `${tr ? 'Ürün' : 'Product'}: ${d.product ? prod : '-'}`,
        `${tr ? 'Miktar' : 'Quantity'}: ${d.qty || '-'}`, '', d.message];
      const subject = `${tr ? 'Teklif Talebi' : 'Quote Request'} — ${d.product ? prod : d.type} — ${d.company || d.name}`;
      const ep = form.dataset.endpoint;
      if (ep) {
        const btn = $('button[type=submit]', form); btn.disabled = true;
        try {
          const r = await fetch(ep, { method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
            body: JSON.stringify({ ...d, product: prod, _subject: subject, _replyto: d.email, _template: 'table' }) });
          if (!r.ok) throw 0;
          form.reset(); status.className = 'qform__status is-ok';
          status.textContent = tr ? 'Teşekkürler! Talebiniz bize ulaştı, en kısa sürede dönüş yapacağız.' : 'Thank you! We received your request and will reply shortly.';
        } catch { status.className = 'qform__status is-err'; status.textContent = tr ? `Gönderilemedi. Lütfen ${form.dataset.email} adresine yazın.` : `Could not send. Please email ${form.dataset.email}.`; }
        btn.disabled = false;
      } else {
        location.href = `mailto:${form.dataset.email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(lines.join('\n'))}`;
        status.className = 'qform__status is-ok';
        status.textContent = tr ? 'E-posta uygulamanız açılıyor; mesajı göndererek talebinizi iletebilirsiniz.' : 'Your email app is opening — send the message to submit your request.';
      }
    });
    form.addEventListener('input', e => e.target.classList.remove('is-invalid'));
  }
})();
