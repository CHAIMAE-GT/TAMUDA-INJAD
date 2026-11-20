/* TAMUDA INJAD – JavaScript léger : navigation, sous-menus, validation de formulaires.
   Aucun traceur, aucun stockage local de données personnelles. */
(function () {
  'use strict';

  /* ---------- Navigation mobile ---------- */
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('primary-nav');
  function setNav(open) {
    if (!toggle || !nav) return;
    nav.classList.toggle('open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.querySelector('span').textContent = open ? 'Fermer' : 'Menu';
  }
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      setNav(toggle.getAttribute('aria-expanded') !== 'true');
    });
  }

  /* ---------- Sous-menu Services ---------- */
  var subs = document.querySelectorAll('.has-sub');
  function setSub(li, open) {
    var btn = li.querySelector('.sub-toggle');
    li.classList.toggle('open', open);
    if (btn) btn.setAttribute('aria-expanded', String(open));
  }
  subs.forEach(function (li) {
    var btn = li.querySelector('.sub-toggle');
    if (!btn) return;
    btn.addEventListener('click', function () {
      setSub(li, btn.getAttribute('aria-expanded') !== 'true');
    });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    var closedSub = false;
    subs.forEach(function (li) {
      if (li.classList.contains('open')) {
        setSub(li, false);
        closedSub = true;
        var b = li.querySelector('.sub-toggle');
        if (b) b.focus();
      }
    });
    if (!closedSub && nav && nav.classList.contains('open')) {
      setNav(false);
      toggle.focus();
    }
  });
  document.addEventListener('click', function (e) {
    subs.forEach(function (li) { if (!li.contains(e.target)) setSub(li, false); });
  });
  /* Ferme le sous-menu quand le focus clavier le quitte */
  subs.forEach(function (li) {
    li.addEventListener('focusout', function (e) {
      if (!li.contains(e.relatedTarget)) setSub(li, false);
    });
  });

  /* ---------- Carte externe : chargée uniquement après clic ---------- */
  document.querySelectorAll('[data-map-src]').forEach(function (box) {
    var btn = box.querySelector('[data-map-load]');
    if (!btn) return;
    btn.addEventListener('click', function () {
      var f = document.createElement('iframe');
      f.src = box.getAttribute('data-map-src');
      f.title = 'Carte interactive de la zone d’intervention';
      f.loading = 'lazy';
      f.referrerPolicy = 'no-referrer-when-downgrade';
      box.textContent = '';
      box.appendChild(f);
    });
  });

  /* ---------- Validation accessible des formulaires ---------- */
  var MSG = {
    valueMissing: 'Ce champ est obligatoire.',
    typeMismatch: 'Le format saisi n’est pas valide.',
    patternMismatch: 'Le format saisi n’est pas valide.',
    tooShort: 'La saisie est trop courte.'
  };
  function messageFor(el) {
    if (el.validity.valueMissing && el.type === 'checkbox') return 'Veuillez cocher cette case pour continuer.';
    if (el.type === 'tel' && !el.validity.valueMissing) return 'Saisissez un numéro de téléphone valide (chiffres, espaces, +).';
    if (el.type === 'email') return 'Saisissez une adresse e-mail valide (ex. nom@domaine.fr).';
    for (var k in MSG) { if (el.validity[k]) return MSG[k]; }
    return 'Valeur non valide.';
  }
  function clearError(el) {
    var wrap = el.closest('.field');
    if (!wrap) return;
    wrap.classList.remove('invalid');
    el.removeAttribute('aria-invalid');
    var err = wrap.querySelector('.error');
    if (err) err.remove();
    var d = (el.getAttribute('aria-describedby') || '').split(' ').filter(function (id) { return id && id !== el.id + '-err'; });
    if (d.length) el.setAttribute('aria-describedby', d.join(' ')); else el.removeAttribute('aria-describedby');
  }
  function showError(el) {
    clearError(el);
    var wrap = el.closest('.field');
    if (!wrap) return;
    wrap.classList.add('invalid');
    el.setAttribute('aria-invalid', 'true');
    var p = document.createElement('p');
    p.className = 'error';
    p.id = el.id + '-err';
    p.textContent = messageFor(el);
    wrap.appendChild(p);
    var d = (el.getAttribute('aria-describedby') || '').split(' ').filter(Boolean);
    d.push(p.id);
    el.setAttribute('aria-describedby', d.join(' '));
  }

  document.querySelectorAll('form[data-form]').forEach(function (form) {
    var status = form.querySelector('.form-status');
    var endpoint = form.getAttribute('data-endpoint') || '';
    form.setAttribute('novalidate', '');

    form.addEventListener('input', function (e) { if (e.target.closest('.field.invalid')) { if (e.target.checkValidity()) clearError(e.target); } });
    form.addEventListener('change', function (e) { if (e.target.closest('.field.invalid')) { if (e.target.checkValidity()) clearError(e.target); } });

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      status.hidden = true;
      var first = null;
      form.querySelectorAll('input, select, textarea').forEach(function (el) {
        if (el.type === 'hidden' || el.name === 'website') return;
        if (!el.checkValidity()) { showError(el); if (!first) first = el; } else { clearError(el); }
      });
      if (first) {
        status.hidden = false;
        status.className = 'form-status ko';
        status.textContent = 'Le formulaire contient des erreurs. Merci de corriger les champs signalés.';
        first.focus();
        return;
      }
      /* Aucun backend configuré : on ne simule PAS l’envoi. */
      if (!endpoint) {
        status.hidden = false;
        status.className = 'form-status demo';
        status.textContent = 'Mode démonstration : ce formulaire n’est relié à aucun service d’envoi. Aucune donnée n’a été transmise ni enregistrée. Merci d’utiliser les coordonnées de la page Contact.';
        return;
      }
      /* Endpoint sécurisé (HTTPS) configuré dans le HTML via data-endpoint */
      if (form.querySelector('[name="website"]') && form.querySelector('[name="website"]').value) return; /* leurre anti-spam */
      var data = {};
      new FormData(form).forEach(function (v, k) { if (k !== 'website') data[k] = v; });
      var btn = form.querySelector('[type="submit"]');
      btn.disabled = true;
      fetch(endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }, body: JSON.stringify(data) })
        .then(function (r) {
          if (!r.ok) throw new Error('HTTP ' + r.status);
          status.hidden = false; status.className = 'form-status ok';
          status.textContent = 'Votre demande a bien été transmise.';
          form.reset();
        })
        .catch(function () {
          status.hidden = false; status.className = 'form-status ko';
          status.textContent = 'L’envoi a échoué. Aucune confirmation n’a été reçue : merci de réessayer ou d’utiliser un autre moyen de contact.';
        })
        .then(function () { btn.disabled = false; });
    });
  });
})();
