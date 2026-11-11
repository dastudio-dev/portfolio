/* ==========================================================================
   DAStudio — Portfolio
   Panel de proyectos (sin modal), lightbox de capturas, scroll dinámico
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {

  const WHATSAPP = 'https://wa.me/5491125395150';
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // --- 1. Datos de los proyectos (capturas reales) ---
  const projects = {
    flota: {
      badge: 'SaaS B2B / Logística',
      title: 'Gestión de Flota, Depósito y Obras',
      result: 'Control total de combustible y partes diarios, sin papel.',
      tags: ['Firebase Firestore', 'Node.js', 'JavaScript Realtime', 'Panel B2B'],
      desafio: 'Una empresa constructora con más de 40 vehículos y equipos pesados en obra sufría ineficiencia y falta de trazabilidad en vales de combustible y partes diarios en papel.',
      solucion: 'Una plataforma web en tiempo real donde los operadores registran partes diarios y cargas con validación de kilometraje. El panel de administración alerta consumos anómalos y vencimientos de service.',
      screenshots: ['img/flota_1.png', 'img/flota_2.png', 'img/flota_3.png', 'img/flota_4.png', 'img/flota_5.png'],
      isPrivate: true,
      note: 'Sistema privado de uso interno. Por confidencialidad se muestran capturas de la aplicación; demo con datos de prueba bajo solicitud.'
    },
    herramientas: {
      badge: 'E-Commerce / Ventas Online',
      title: 'E-Commerce & Venta de Herramientas',
      result: 'Ventas online con cobro automático y envío calculado por código postal.',
      tags: ['Vite / React', 'Mercado Pago', 'Cálculo de envíos', 'Firebase'],
      desafio: 'Un comercio de herramientas e insumos industriales necesitaba pasar de un catálogo tradicional a una tienda online completa, con carrito, cobros automatizados y despacho de envíos.',
      solucion: 'Una tienda con arquitectura moderna: catálogo fluido, pasarelas de pago (Mercado Pago, tarjetas), costo de envío según código postal o retiro en local, y panel de administración de pedidos.',
      screenshots: ['img/herramientas_1.png', 'img/herramientas_2.png'],
      liveUrl: 'https://herramientaslibres.web.app'
    },
    neomonitor: {
      badge: 'Simulación / Multi-Dispositivo',
      title: 'NeoMonitor — Simulador Virtual de Monitor',
      result: 'Cualquier pantalla se convierte en monitor, controlado desde el celular.',
      tags: ['Node.js', 'WebSockets', 'Realtime API', 'Simulación clínica'],
      desafio: 'Los talleres de simulación médica y RCP neonatal (NRP) requieren monitores multiparamétricos costosos y difíciles de trasladar.',
      solucion: 'Un software que convierte cualquier pantalla, Smart TV o tablet en un monitor multiparamétrico interactivo, controlado en tiempo real desde el celular del instructor mediante WebSockets.',
      screenshots: ['img/neomonitor_1.png', 'img/neomonitor_2.png'],
      note: 'Plataforma de simulación interactiva sin instalación previa.'
    },
    constructora: {
      badge: 'Institucional',
      title: 'Landing Page — JL Constructora SRL',
      result: 'Una web liviana que transmite solvencia ante licitaciones.',
      tags: ['HTML5 semántico', 'CSS3', 'SEO B2B', 'Mobile first'],
      desafio: 'La constructora necesitaba presentar credenciales ante licitaciones y empresas de alto ticket. Su sitio anterior era lento y no transmitía solvencia corporativa.',
      solucion: 'Una web institucional limpia, sin librerías pesadas, que destaca obras ejecutadas y capacidad técnica, con acceso directo a pedidos de presupuesto.',
      screenshots: ['img/constructora_1.png', 'img/constructora_2.png', 'img/constructora_3.png'],
      liveUrl: 'https://www.jlsrl.com.ar'
    },
    neocalcu: {
      badge: 'App Móvil / Neonatal',
      title: 'NeoCalcu — Calculadora Neonatal & UCIN',
      result: 'Dosis exactas en el celular, sin depender de la conexión.',
      tags: ['TypeScript', 'PWA offline', 'Capacitor', 'UCIN'],
      desafio: 'En terapia intensiva neonatal, el cálculo de dosis para pesos extremadamente bajos exige precisión matemática absoluta.',
      solucion: 'Una PWA offline para uso junto a la incubadora, que calcula dosis de fármacos e infusiones neonatales con sliders interactivos y validación clínica.',
      screenshots: ['img/neocalcu_1.png', 'img/neocalcu_2.png', 'img/neocalcu_3.png'],
      note: 'Aplicación clínica instalable en dispositivos móviles.'
    },
    egpediatria: {
      badge: 'App Móvil / Emergencias',
      title: 'EGPediatria — Estoy de Guardia Pediatría',
      result: 'Diluciones y dosis a la vista en segundos, en plena guardia.',
      tags: ['JavaScript', 'PWA offline', 'SAP / PALS', 'Emergencias'],
      desafio: 'En la guardia de pediatría, calcular inotrópicos, antiepilépticos y diluciones bajo estrés requiere una guía gráfica de acceso inmediato.',
      solucion: 'Una aplicación interactiva con instrucciones exactas de dilución, volumen a extraer por ampolla y tablas de dosificación según estándares SAP y PALS.',
      screenshots: ['img/egpediatria_1.png', 'img/egpediatria_2.png', 'img/egpediatria_3.png'],
      note: 'Herramienta clínica interactiva de acceso público.'
    }
  };

  const escapeHtml = (str) => String(str).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

  // --- 2. Lightbox de capturas ---
  const lightboxOverlay = document.getElementById('imageLightbox');
  const lightboxImg = document.getElementById('lightboxImg');
  const lightboxCounter = document.getElementById('lightboxCounter');
  const lightboxPrevBtn = document.getElementById('lightboxPrevBtn');
  const lightboxNextBtn = document.getElementById('lightboxNextBtn');
  let lightboxImages = [];
  let lightboxIndex = 0;

  function renderLightbox() {
    lightboxImg.src = lightboxImages[lightboxIndex];
    lightboxCounter.textContent = `${lightboxIndex + 1} / ${lightboxImages.length}`;
    const multiple = lightboxImages.length > 1;
    lightboxPrevBtn.style.display = multiple ? 'flex' : 'none';
    lightboxNextBtn.style.display = multiple ? 'flex' : 'none';
  }

  function openLightbox(images, startIndex) {
    lightboxImages = images;
    lightboxIndex = startIndex;
    renderLightbox();
    lightboxOverlay.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  function closeLightbox() {
    lightboxOverlay.classList.remove('active');
    document.body.style.overflow = '';
  }

  lightboxPrevBtn.addEventListener('click', () => {
    lightboxIndex = (lightboxIndex - 1 + lightboxImages.length) % lightboxImages.length;
    renderLightbox();
  });
  lightboxNextBtn.addEventListener('click', () => {
    lightboxIndex = (lightboxIndex + 1) % lightboxImages.length;
    renderLightbox();
  });
  document.getElementById('lightboxCloseBtn').addEventListener('click', closeLightbox);
  lightboxOverlay.addEventListener('click', (e) => { if (e.target === lightboxOverlay) closeLightbox(); });
  document.addEventListener('keydown', (e) => {
    if (!lightboxOverlay.classList.contains('active')) return;
    if (e.key === 'Escape') closeLightbox();
    if (e.key === 'ArrowLeft') lightboxPrevBtn.click();
    if (e.key === 'ArrowRight') lightboxNextBtn.click();
  });

  // --- 3. Panel de proyectos (lista + detalle en la misma página) ---
  const workList = document.getElementById('workList');
  const workPanel = document.getElementById('workPanel');
  const workItems = workList ? workList.querySelectorAll('.work-item') : [];
  let currentProject = null;

  // Las capturas verticales se muestran completas; las horizontales, rellenando el marco
  function markPortrait(img) {
    const apply = () => img.classList.toggle('portrait', img.naturalHeight > img.naturalWidth);
    if (img.complete) apply(); else img.addEventListener('load', apply, { once: true });
  }

  function renderProject(id) {
    const p = projects[id];
    if (!p) return;
    currentProject = id;

    const accessBadge = p.isPrivate
      ? '<span class="private-badge">🔒 Acceso privado</span>'
      : '<span class="public-badge">🌐 Acceso libre</span>';

    const consult = `${WHATSAPP}?text=${encodeURIComponent('Hola, quiero consultar por el proyecto: ' + p.title)}`;
    const liveBtn = p.liveUrl
      ? `<a class="btn btn-primary btn-sm" href="${p.liveUrl}" target="_blank" rel="noopener"><span>Visitar el sitio</span><svg class="arrow-ico" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M7 17L17 7M8 7h9v9"/></svg></a>`
      : '';
    const consultBtn = `<a class="btn ${p.liveUrl ? 'btn-secondary' : 'btn-primary'} btn-sm" href="${consult}" target="_blank" rel="noopener"><span>Consultar por este proyecto</span><svg class="arrow-ico" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg></a>`;

    workPanel.innerHTML = `
      <button type="button" class="wp-main" aria-label="Ampliar captura">
        <img src="${p.screenshots[0]}" alt="Captura de ${escapeHtml(p.title)}">
        <span class="wp-zoom">Ampliar</span>
      </button>
      ${p.screenshots.length > 1 ? `<div class="wp-thumbs">${p.screenshots.map((src, i) => `
        <button type="button" class="wp-thumb${i === 0 ? ' active' : ''}" data-idx="${i}" aria-label="Captura ${i + 1}">
          <img src="${src}" alt="">
        </button>`).join('')}</div>` : ''}
      <div class="wp-body">
        <div>
          <div class="wp-badges"><span class="category-badge">${escapeHtml(p.badge)}</span>${accessBadge}</div>
          <h3 class="wp-title">${escapeHtml(p.title)}</h3>
          <p class="wp-result">${escapeHtml(p.result)}</p>
          <div class="tech-tags">${p.tags.map(t => `<span>${escapeHtml(t)}</span>`).join('')}</div>
          <div class="wp-actions">${liveBtn}${consultBtn}</div>
        </div>
        <div>
          <dl class="wp-story">
            <dt>El problema</dt><dd>${escapeHtml(p.desafio)}</dd>
            <dt>La solución</dt><dd>${escapeHtml(p.solucion)}</dd>
          </dl>
          ${p.note ? `<p class="wp-note">${escapeHtml(p.note)}</p>` : ''}
        </div>
      </div>`;

    const mainBtn = workPanel.querySelector('.wp-main');
    const mainImg = mainBtn.querySelector('img');
    const thumbs = workPanel.querySelectorAll('.wp-thumb');
    let shown = 0;

    markPortrait(mainImg);
    thumbs.forEach(t => markPortrait(t.querySelector('img')));

    mainBtn.addEventListener('click', () => openLightbox(p.screenshots, shown));
    thumbs.forEach(thumb => {
      thumb.addEventListener('click', () => {
        const idx = Number(thumb.dataset.idx);
        if (idx === shown) return;
        shown = idx;
        thumbs.forEach(t => t.classList.toggle('active', t === thumb));
        mainImg.classList.add('fading');
        setTimeout(() => {
          mainImg.src = p.screenshots[idx];
          markPortrait(mainImg);
          mainImg.classList.remove('fading');
        }, reduceMotion ? 0 : 200);
      });
    });
  }

  function selectProject(id) {
    if (!projects[id] || id === currentProject) return;
    workItems.forEach(item => {
      const on = item.dataset.project === id;
      item.classList.toggle('active', on);
      item.setAttribute('aria-selected', String(on));
    });
    if (reduceMotion || !currentProject) {
      renderProject(id);
      return;
    }
    workPanel.classList.add('is-swapping');
    setTimeout(() => {
      renderProject(id);
      workPanel.classList.remove('is-swapping');
    }, 200);
  }

  if (workPanel) {
    workItems.forEach(item => item.addEventListener('click', () => selectProject(item.dataset.project)));
    renderProject('flota');
  }

  // Enlaces "En la práctica" de cada paso: abren el proyecto correspondiente
  document.querySelectorAll('.step-link').forEach(link => {
    link.addEventListener('click', () => {
      selectProject(link.dataset.project);
      document.getElementById('proyectos').scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth' });
    });
  });

  // --- 4. Modal del contrato ---
  const contractModal = document.getElementById('contractModal');
  const openContractModalBtn = document.getElementById('openContractModalBtn');

  if (contractModal && openContractModalBtn) {
    const closeContract = () => {
      contractModal.classList.remove('active');
      document.body.style.overflow = '';
    };
    openContractModalBtn.addEventListener('click', () => {
      contractModal.classList.add('active');
      document.body.style.overflow = 'hidden';
    });
    document.getElementById('contractModalCloseBtn').addEventListener('click', closeContract);
    document.getElementById('contractModalCloseBottomBtn').addEventListener('click', closeContract);
    contractModal.addEventListener('click', (e) => { if (e.target === contractModal) closeContract(); });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && contractModal.classList.contains('active')) closeContract();
    });
  }

  // --- 5. Menú móvil ---
  const hamburgerBtn = document.getElementById('hamburgerBtn');
  const navMenu = document.getElementById('navMenu');
  if (hamburgerBtn) hamburgerBtn.addEventListener('click', () => navMenu.classList.toggle('active'));
  document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => navMenu.classList.remove('active'));
  });

  // --- 6. Dinamismo de scroll ---
  const progressBar = document.getElementById('scrollProgress');
  const navbar = document.getElementById('navbar');
  function onScroll() {
    const max = document.documentElement.scrollHeight - window.innerHeight;
    if (progressBar) progressBar.style.setProperty('--p', max > 0 ? (window.scrollY / max).toFixed(4) : 0);
    if (navbar) navbar.classList.toggle('scrolled', window.scrollY > 20);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  const revealEls = document.querySelectorAll('[data-reveal]');
  if ('IntersectionObserver' in window) {
    const revealObs = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('in');
          revealObs.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    revealEls.forEach(el => revealObs.observe(el));

    // Paso activo del proceso: el que cruza el centro de la pantalla
    const steps = document.querySelectorAll('.step');
    if (steps.length) {
      steps[0].classList.add('is-active');
      const stepObs = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            steps.forEach(s => s.classList.toggle('is-active', s === entry.target));
          }
        });
      }, { rootMargin: '-42% 0px -42% 0px' });
      steps.forEach(s => stepObs.observe(s));
    }

    // Link activo del menú según la sección visible
    const navLinks = document.querySelectorAll('.nav-link[href^="#"]');
    const sectionObs = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          navLinks.forEach(l => l.classList.toggle('active', l.getAttribute('href') === '#' + entry.target.id));
        }
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    ['enfoque', 'proyectos', 'contacto'].forEach(id => {
      const el = document.getElementById(id);
      if (el) sectionObs.observe(el);
    });
  } else {
    revealEls.forEach(el => el.classList.add('in'));
  }

});
