/* Administrator-authorized scan scope editor. */
(() => {
  const renderScanner = window.PAGES.scanner;
  window.PAGES.scanner = async function(el, seg) {
    await renderScanner(el, seg);
    if (seg[1]) return;
  const loadScope = async () => {
    const box = document.getElementById("scope-box");
    try {
      const [scope, config] = await Promise.all([getJSON("/scanner/scope"), getJSON("/settings")]);
      const extra = config.settings.extra_authorized_cidrs.value || [];
      box.innerHTML = `<p>Effective networks:</p><p class="mono">${esc(scope.networks.join(", "))}</p>
        <p class="faint small">Server-configured networks remain managed by the server administrator. Add, edit or remove additional networks below. Only add networks you own or are authorized to scan.</p>
        ${config.can_write ? `<label for="scope-networks">Additional authorized networks (one IP or CIDR per line)</label>
        <textarea id="scope-networks" rows="5" placeholder="10.53.216.0/24">${esc(extra.join("\n"))}</textarea>
        <button id="save-scope" class="primary">Save networks</button>
        <p id="scope-save-status" role="status" aria-live="polite"></p>` : '<p>Only administrators can edit authorized networks.</p>'}
        <div class="sep"></div><p>Nmap: ${scope.nmap_available ? 'AVAILABLE' : 'NOT FOUND'}</p>`;
      const save = box.querySelector("#save-scope");
      if (save) save.onclick = async () => {
        save.disabled = true;
        const status = box.querySelector("#scope-save-status");
        try {
          const networks = box.querySelector("#scope-networks").value.split(/[\n,]+/).map(x => x.trim()).filter(Boolean);
          await putJSON("/settings/extra_authorized_cidrs", {value: networks});
          await loadScope();
          toast("Authorized networks saved", "ok");
        } catch (e) { status.textContent = e.message; save.disabled = false; }
      };
    } catch (e) { box.textContent = e.message; }
  };
  await loadScope();

  };
})();
