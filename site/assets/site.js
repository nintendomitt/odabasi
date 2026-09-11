
(function(){
  var burger = document.getElementById('burger');
  var nav = document.getElementById('nav');
  if (burger && nav) {
    burger.addEventListener('click', function(){
      var open = nav.classList.toggle('open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      document.body.style.overflow = open ? 'hidden' : '';
    });
  }
  var groups = document.querySelectorAll('.has-menu');
  groups.forEach(function(g){
    var btn = g.querySelector('.nav-toggle');
    if(!btn) return;
    btn.addEventListener('click', function(ev){
      ev.stopPropagation();
      var wasOpen = g.classList.contains('open');
      groups.forEach(function(x){ x.classList.remove('open'); var b=x.querySelector('.nav-toggle'); if(b) b.setAttribute('aria-expanded','false'); });
      if(!wasOpen){ g.classList.add('open'); btn.setAttribute('aria-expanded','true'); }
    });
  });
  document.addEventListener('click', function(ev){
    if(ev.target.closest && ev.target.closest('.has-menu')) return;
    groups.forEach(function(x){ x.classList.remove('open'); var b=x.querySelector('.nav-toggle'); if(b) b.setAttribute('aria-expanded','false'); });
  });
  document.addEventListener('keydown', function(ev){
    if(ev.key === 'Escape'){
      groups.forEach(function(x){ x.classList.remove('open'); });
      if(nav){ nav.classList.remove('open'); }
      if(burger){ burger.setAttribute('aria-expanded','false'); }
      document.body.style.overflow = '';
    }
  });

  // Teklif formu -> WhatsApp
  var form = document.getElementById('leadForm');
  if (form) {
    form.addEventListener('submit', function(ev){
      ev.preventDefault();
      var d = new FormData(form);
      var ad = (d.get('ad')||'').toString().trim();
      var tel = (d.get('tel')||'').toString().trim();
      if(!ad || !tel){
        alertless(form, 'Lütfen ad soyad ve telefon alanlarını doldurun.');
        return;
      }
      var lines = [
        'Merhaba, web sitesi üzerinden teklif talebi:',
        'Ad Soyad: ' + ad,
        'Telefon: ' + tel
      ];
      if(d.get('urun')) lines.push('Ürün grubu: ' + d.get('urun'));
      if(d.get('bolge')) lines.push('Bölge: ' + d.get('bolge'));
      if(d.get('not')) lines.push('Not: ' + d.get('not'));
      if(form.dataset.source) lines.push('Kaynak: ' + form.dataset.source);
      var url = 'https://wa.me/905000000000?text=' + encodeURIComponent(lines.join('\n'));
      window.open(url, '_blank', 'noopener');
      alertless(form, 'Talebiniz WhatsApp üzerinden iletilmek üzere hazırlandı.');
    });
  }
  // --- hizmet haritasi: liste <-> nokta vurgulamasi ---
  var smap = document.querySelector('.smap');
  if (smap) {
    var link = function(el, on){
      var k = el.getAttribute('data-loc');
      smap.querySelectorAll('[data-loc="' + (window.CSS && CSS.escape ? CSS.escape(k) : k) + '"]')
        .forEach(function(n){ n.classList.toggle('is-hi', on); });
    };
    smap.querySelectorAll('[data-loc]').forEach(function(el){
      el.addEventListener('mouseenter', function(){ link(el, true); });
      el.addEventListener('mouseleave', function(){ link(el, false); });
      el.addEventListener('focus', function(){ link(el, true); });
      el.addEventListener('blur', function(){ link(el, false); });
    });
  }

  function alertless(scope, msg){
    var box = scope.querySelector('.form-msg');
    if(!box){
      box = document.createElement('p');
      box.className = 'form-msg lead-note';
      scope.appendChild(box);
    }
    box.textContent = msg;
  }
})();
