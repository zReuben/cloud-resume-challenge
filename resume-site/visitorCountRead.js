const countEl = document.getElementById('resumeCount');
const spinnerEl = document.getElementById('spinner');

spinnerEl.style.display = 'inline-block';

fetch('/visitor-count', { method: 'GET' })
  .then(r => r.json())
  .then(data => {
    if (data && data.body) { try { data = JSON.parse(data.body); } catch(_) {} }
    countEl.textContent = (data && typeof data.count === 'number') ? data.count : '—';
  })
  .catch(() => { countEl.textContent = '—'; })
  .finally(() => { spinnerEl.style.display = 'none'; });
