(function () {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const csrf = (document.cookie.match(/csrftoken=([^;]+)/) || [])[1];

  function toast(msg) {
    const t = document.createElement('div');
    t.className = 'toast'; t.textContent = msg;
    $('#toast-root').appendChild(t);
    setTimeout(() => t.remove(), 3500);
  }
  async function send(url, data = {}) {
    const r = await fetch(url, { method: 'POST', headers: { 'X-CSRFToken': csrf, 'Content-Type': 'application/x-www-form-urlencoded' }, body: new URLSearchParams(data) });
    if (!r.ok) throw new Error(r.status);
    return r.json();
  }
  $$('main > .toast').forEach(m => toast(m.textContent));

  $('#theme').addEventListener('click', () => {
    const next = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
    document.documentElement.dataset.theme = next;
    try { localStorage.setItem('theme', next); } catch (e) {}
  });

  // Home: instant search + filters
  const grid = $('#grid');
  if (grid) {
    const state = { kind: '', cat: '', q: '' }, cards = $$('.card', grid);
    const apply = () => {
      let shown = 0;
      cards.forEach(c => {
        const ok = (!state.kind || c.dataset.kind === state.kind) && (!state.cat || c.dataset.cat === state.cat) && (!state.q || c.dataset.text.includes(state.q));
        c.classList.toggle('hide', !ok); if (ok) shown++;
      });
      $('#empty').hidden = shown > 0;
      $('#result-count').textContent = cards.length ? `${shown} of ${cards.length} posts` : '';
    };
    $$('.chips').forEach(g => g.addEventListener('click', e => {
      const b = e.target.closest('.chip'); if (!b) return;
      $$('.chip', g).forEach(x => x.classList.toggle('on', x === b));
      state[g.dataset.group] = b.dataset.v; apply();
    }));
    $('#search').addEventListener('input', e => { state.q = e.target.value.trim().toLowerCase(); apply(); });
    apply();
  }

  // Write form counter
  const body = $('textarea[name=body]');
  if (body && $('#count')) { const u = () => $('#count').textContent = body.value.length; body.addEventListener('input', u); u(); }

  // Save + report on a post
  const bm = $('#bm');
  if (bm) bm.addEventListener('click', async () => {
    try { const d = await send(bm.dataset.url); bm.textContent = d.saved ? 'Saved' : 'Save'; toast(d.saved ? 'Saved to your list' : 'Removed from saved'); }
    catch (e) { toast('Could not update. Try again.'); }
  });
  const rp = $('#report');
  if (rp) rp.addEventListener('click', async () => {
    const reason = prompt('What is wrong with this post?'); if (reason === null) return;
    try { const d = await send(rp.dataset.url, { reason }); toast(d.created ? 'Report sent to the admins' : 'You already reported this post'); }
    catch (e) { toast('Could not send the report.'); }
  });

  // Moderation: approve / decline / dismiss without reloading
  const fade = el => { el.classList.add('gone'); setTimeout(() => el.remove(), 300); };
  document.addEventListener('click', async e => {
    const btn = e.target.closest('.review button[data-action], button[data-dismiss]'); if (!btn) return;
    const row = btn.closest('.review, [data-report]');
    let note = '';
    if (btn.dataset.action === 'decline') { note = prompt('Tell the author why this was declined (optional):'); if (note === null) return; }
    btn.disabled = true;
    try {
      const d = await send(btn.dataset.url, { note });
      fade(row);
      if (btn.dataset.action) {
        $('#queue-count').textContent = d.pending;
        const nav = $('#nav-count'); if (nav) nav.textContent = d.pending;
        if (!d.pending) $('#queue-empty').hidden = false;
        toast(btn.dataset.action === 'approve' ? 'Approved and published' : 'Declined');
      } else toast('Report dismissed');
    } catch (err) { btn.disabled = false; toast('Something went wrong. Try again.'); }
  });
})();
