const { chromium } = require('playwright');
const path = require('path');
const icons = {
  '1-proyectos': '<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/>',
  '2-como-trabajamos': '<path d="M10 6h10M10 12h10M10 18h10"/><path d="M3.5 6l1.5 1.5L7.5 4.5M3.5 12l1.5 1.5L7.5 10.5M3.5 18l1.5 1.5L7.5 16.5"/>',
  '3-planillas-a-sistema': '<rect x="1.5" y="6" width="8" height="12" rx="1"/><path d="M1.5 10h8M1.5 14h8M5.5 6v12"/><path d="M11.5 12h3M13 10.5l1.5 1.5-1.5 1.5"/><rect x="16" y="6" width="6.5" height="12" rx="1"/><path d="M16 9h6.5"/>',
  '4-salud-apps-clinicas': '<path d="M2.5 12h4l2.5-6 4 12 2.5-6h6"/>',
  '5-contacto': '<path d="M21 12a8 8 0 0 1-11.7 7L4 20l1.1-4.4A8 8 0 1 1 21 12z"/><path d="M8.5 12h.01M12 12h.01M15.5 12h.01"/>'
};
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  for (const [name, svg] of Object.entries(icons)) {
    await p.setContent(`<style>html,body{margin:0;width:1080px;height:1920px;background:#0d1117;display:flex;align-items:center;justify-content:center}
    .c{width:640px;height:640px;border-radius:50%;background:#161b22;border:6px solid #30363d;display:flex;align-items:center;justify-content:center}
    svg{width:320px;height:320px;fill:none;stroke:#38bdf8;stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round}</style>
    <div class="c"><svg viewBox="0 0 24 24">${svg}</svg></div>`);
    await p.screenshot({ path: path.join(__dirname, 'portadas', name + '.png') });
  }
  await b.close();
})();
