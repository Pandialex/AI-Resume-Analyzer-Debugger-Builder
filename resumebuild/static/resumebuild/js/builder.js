// resumebuild/js/builder.js
// Generic builder helper used by all step templates
const Builder = (function(){
  let cfg = {
    draftId: null,
    step: 1,
    getData: null,
    onNext: null
  };
  let _debounceTimer = null;
  const DEBOUNCE_MS = 900;
  const CSRF = (function(){ // get csrftoken
    function cookie(name){ let v=null; if(document.cookie && document.cookie!==''){document.cookie.split(';').forEach(c=>{const t=c.trim(); if(t.startsWith(name+'=')){v=decodeURIComponent(t.substring(name.length+1));}});} return v;}
    return cookie('csrftoken');
  })();

  async function saveNow(){
    const url = `/resumebuild/api/draft/${cfg.draftId}/save/`;
    const payload = { data: cfg.getData ? cfg.getData() : (window.__RESUME_DATA__ || {}), current_step: cfg.step };
    const res = await fetch(url, {
      method: 'POST',
      headers: {'Content-Type':'application/json','X-CSRFToken': CSRF},
      body: JSON.stringify(payload)
    });
    return res.json();
  }

  function debouncedSave(){
    clearTimeout(_debounceTimer);
    _debounceTimer = setTimeout(()=>{ saveNow().then(r=>console.log('autosave', r)); }, DEBOUNCE_MS);
  }

  function bindInputs(root){
    // attach input listeners inside root (element or document)
    const scope = root || document;
    Array.from(scope.querySelectorAll('input, textarea, select')).forEach(el=>{
      el.addEventListener('input', debouncedSave);
    });
  }

  function currentData(){
    // used to get previously-initialized data in templates via window.__RESUME_DATA__
    return window.__RESUME_DATA__ || {};
  }

  function init(options){
    cfg = Object.assign(cfg, options);
    // attach to window for debugging
    window.Builder = window.Builder || {};
    window.Builder.config = cfg;
    window.Builder.saveNow = saveNow;
    window.Builder.debouncedSave = debouncedSave;
    window.Builder.bindInputs = bindInputs;
    window.Builder.currentData = currentData;

    // bind existing inputs on page for autosave
    bindInputs(document);

    // update progress bar width based on step
    const prog = document.getElementById('prog');
    if(prog){ const percent = Math.min(100, Math.round((cfg.step / 7)*100)); prog.style.width = percent + '%'; prog.style.transition = 'width .25s ease'; }

    // load draft data into window.__RESUME_DATA__ if server provided data variable
    try{
      if(window.__RESUME_DATA__ === undefined){
        // if template included 'data' context, it's available as "data" var in template; guard set
        window.__RESUME_DATA__ = (typeof __TEMPLATE_DATA__ !== 'undefined') ? __TEMPLATE_DATA__ : window.__RESUME_DATA__ || {};
      }
    } catch(e){ console.warn('builder init data load', e); }

    // keyboard shortcut: Ctrl+S to save
    document.addEventListener('keydown', (e)=>{
      if((e.ctrlKey || e.metaKey) && e.key === 's'){ e.preventDefault(); saveNow().then(r=>{ console.log('saved via shortcut', r); alert('Saved'); }); }
    });
  }

  return {
    init: init,
    saveNow: saveNow,
    debouncedSave: debouncedSave,
    bindInputs: bindInputs,
    currentData: currentData,
    config: cfg
  };
})();
