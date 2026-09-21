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
    const lang = form.dataset.lang;
    const M = {
      tr: { req: 'Lütfen zorunlu alanları kontrol edin.', sending: 'Gönderiliyor…', ok: 'Teşekkürler! Talebiniz bize ulaştı, en kısa sürede dönüş yapacağız.',
            fail: 'Şu an gönderilemedi. Aşağıdaki düğmeyle e-posta olarak iletebilirsiniz.', mail: 'E-posta ile gönder', subj: 'Teklif Talebi',
            L: ['Ad Soyad', 'Firma', 'E-posta', 'Telefon', 'Ülke', 'Talep', 'Ürün', 'Miktar'] },
      en: { req: 'Please check the required fields.', sending: 'Sending…', ok: 'Thank you! We received your request and will reply shortly.',
            fail: 'Could not send right now. Use the button below to send it by email.', mail: 'Send by email', subj: 'Quote Request',
            L: ['Name', 'Company', 'Email', 'Phone', 'Country', 'Request', 'Product', 'Quantity'] },
      ar: { req: 'يرجى التحقق من الحقول الإلزامية.', sending: 'جارٍ الإرسال…', ok: 'شكرًا لكم! وصلنا طلبكم وسنرد عليكم في أقرب وقت.',
            fail: 'تعذّر الإرسال حاليًا. يمكنكم إرسال الطلب بالبريد الإلكتروني عبر الزر أدناه.', mail: 'إرسال بالبريد الإلكتروني', subj: 'طلب عرض سعر',
            L: ['الاسم', 'الشركة', 'البريد الإلكتروني', 'الهاتف', 'الدولة', 'نوع الطلب', 'المنتج', 'الكمية'] },
    }[lang] || {};
    const status = $('.qform__status', form), btn = $('button[type=submit]', form), btnHTML = btn.innerHTML;
    const p = new URLSearchParams(location.search).get('urun');
    if (p && form.product.querySelector(`option[value="${CSS.escape(p)}"]`)) form.product.value = p;
    const setStatus = (cls, html) => { status.className = 'qform__status ' + cls; status.innerHTML = html; };
    form.addEventListener('submit', async e => {
      e.preventDefault();
      let ok = true;
      $$('[required]', form).forEach(f => {
        const bad = f.type === 'checkbox' ? !f.checked : !f.value.trim() || (f.type === 'email' && !/^\S+@\S+\.\S+$/.test(f.value));
        f.classList.toggle('is-invalid', bad); if (bad) ok = false;
      });
      if (!ok) return setStatus('is-err', M.req);
      const d = Object.fromEntries(new FormData(form));
      const prod = d.product ? form.product.selectedOptions[0].text : '-';
      const vals = [d.name, d.company, d.email, d.phone, d.country, d.type, prod, d.qty];
      const body = M.L.map((l, i) => `${l}: ${vals[i] || '-'}`).join('\n') + '\n\n' + d.message;
      const subject = `${M.subj} — ${d.product ? prod : d.type} — ${d.company || d.name}`;
      const mailto = `mailto:${form.dataset.email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
      const ep = form.dataset.endpoint;
      if (!ep) { location.href = mailto; return; }
      btn.disabled = true; btn.innerHTML = `<span class="spinner" aria-hidden="true"></span> ${M.sending}`;
      setStatus('', '');
      const ctrl = new AbortController(), timer = setTimeout(() => ctrl.abort(), 15000);
      try {
        const payload = { ...d, product: prod, subject, _subject: subject, from_name: 'asyacerez.com', replyto: d.email, _replyto: d.email, _template: 'table', _captcha: 'false' };
        if (form.dataset.key) payload.access_key = form.dataset.key;
        const r = await fetch(ep, { method: 'POST', signal: ctrl.signal, headers: { 'Content-Type': 'application/json', Accept: 'application/json' }, body: JSON.stringify(payload) });
        const j = await r.json().catch(() => ({}));
        if (!r.ok || j.success === false || j.success === 'false') throw 0;
        form.reset(); setStatus('is-ok', M.ok);
      } catch {
        setStatus('is-err', `${M.fail}<br><a class="btn btn--outline btn--sm qform__mail" href="${mailto}">${M.mail}</a>`);
      } finally { clearTimeout(timer); btn.disabled = false; btn.innerHTML = btnHTML; }
    });
    form.addEventListener('input', e => e.target.classList.remove('is-invalid'));
  }
})();
