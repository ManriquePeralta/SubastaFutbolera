let started = false;

function showNotification(text, kind = 'info'){
  // kind: info | success | error
  const container = document.getElementById('notifications');
  const el = document.createElement('div');
  el.className = 'notification ' + kind;
  el.textContent = text;
  container.prepend(el);
  setTimeout(()=>{ el.style.opacity = '0'; setTimeout(()=>el.remove(),600); }, 5000);
}

document.getElementById("startBtn").addEventListener("click", async ()=>{
  const parts = document.getElementById("participants").value.split(",").map(s=>s.trim()).filter(Boolean);
  const formation = document.getElementById("formation").value;
  if(parts.length < 1){ showNotification("Ingresa al menos un participante", 'error'); return; }
  const res = await fetch("/start", {
    method:"POST", headers:{"Content-Type":"application/json"},
    body: JSON.stringify({participants:parts, formation})
  });
  const j = await res.json();
  if(!j.ok){ showNotification("Error: "+ (j.error||''), 'error'); return; }
  started = true;
  showNotification("Subasta iniciada — " + j.total_items + " candidatos", 'success');
  // populate participant selector
  const sel = document.getElementById('participantName');
  sel.value = parts[0] || '';
  loadCandidate();
  loadStatus();
});

async function loadCandidate(){
  const r = await fetch("/candidate");
  const j = await r.json();
  if(j.finished || !j.ok){
    document.querySelector(".mistery-tag").textContent = "SUBASTA FINALIZADA";
    document.getElementById("pos").textContent="";
    document.getElementById("nac").textContent="";
    document.getElementById("price").textContent="";
    document.getElementById("plaza_desc").textContent="";
    showNotification('Subasta finalizada', 'info');
    renderPlanteles();
    return;
  }
  document.querySelector(".mistery-tag").textContent = "JUGADOR MISTERIOSO";
  document.getElementById("pos").textContent = "Posición: " + j.Posicion;
  document.getElementById("nac").textContent = "Nacionalidad: " + j.Nacionalidad;
  document.getElementById("price").textContent = "Precio base: " + j.Precio + " M";
  document.getElementById("plaza_desc").textContent = "Plaza: " + j.plaza_desc;
  document.getElementById("amount").value = j.Precio;
  document.getElementById("remaining").textContent = "Candidatos restantes: " + j.remaining;

  // show planteles at mid-auction: when global_slot == 6 (i.e., before starting 6)
  if(j.global_slot === 6){
    showNotification('Pausa: mitad de la subasta — mostrando planteles', 'info');
    renderPlanteles();
  }
}

document.getElementById("passBtn").addEventListener("click", async ()=>{
  if(!started){ showNotification("Inicia la subasta primero", 'error'); return; }
  const r = await fetch("/action", {method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify({action:"paso"})});
  const j = await r.json();
  if(!j.ok){ showNotification("Error: " + (j.error||''), 'error'); return; }
  // show who was the passed player
  if(j.Jugador){ showNotification(`Se pasó a: ${j.Jugador}`, 'info'); }
  loadCandidate(); loadStatus();
});

document.getElementById("payBtn").addEventListener("click", async ()=>{
  if(!started){ showNotification("Inicia la subasta primero", 'error'); return; }
  const participant = document.getElementById("participantName").value.trim();
  const amount = parseInt(document.getElementById("amount").value);
  if(!participant || isNaN(amount)){ showNotification("Rellena participante y monto", 'error'); return; }
  const r = await fetch("/action", {method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify({action:"pagar", participant, monto: amount})});
  const j = await r.json();
  if(!j.ok){ showNotification("Error: " + (j.error||''), 'error'); return; }
  showNotification(j.msg, 'success');
  document.getElementById("amount").value = "";
  loadCandidate(); loadStatus();
});

async function renderPlanteles(){
  const r = await fetch('/status'); const j = await r.json();
  if(!j.ok) return;
  const plantelesDiv = document.getElementById('planteles');
  plantelesDiv.innerHTML = '';
  // build a neat layout for each participant
  for(const [p, data] of Object.entries(j.participants)){
    const wrap = document.createElement('div'); wrap.className = 'roster';
    const title = document.createElement('h4'); title.textContent = p; wrap.appendChild(title);
    // map positions -> names
    const map = {};
    for(const pl of data.plantel){ map[pl.Posicion] = map[pl.Posicion] || []; map[pl.Posicion].push(pl.Jugador); }

    const rowDef = document.createElement('div'); rowDef.className='row defenders';
    // defenders: DFD, DFC, DFI
    ['DFD','DFC','DFI'].forEach(k=>{ const cell = document.createElement('div'); cell.className='cell'; cell.textContent = (map[k]||[]).join(' | '); rowDef.appendChild(cell); });
    wrap.appendChild(rowDef);

    const rowMid = document.createElement('div'); rowMid.className='row midfield';
    ['MCD','MC','MCO'].forEach(k=>{ const cell = document.createElement('div'); cell.className='cell'; cell.textContent = (map[k]||[]).join(' | '); rowMid.appendChild(cell); });
    wrap.appendChild(rowMid);

    const rowFwd = document.createElement('div'); rowFwd.className='row forwards';
    ['ED','EI','DC'].forEach(k=>{ const cell = document.createElement('div'); cell.className='cell'; cell.textContent = (map[k]||[]).join(' | '); rowFwd.appendChild(cell); });
    wrap.appendChild(rowFwd);

    const gk = document.createElement('div'); gk.className='gk'; gk.textContent = (map['PO']||[]).join(' | ');
    wrap.appendChild(gk);

    plantelesDiv.appendChild(wrap);
  }
  // make planteles visible
}

async function loadStatus(){
  const r = await fetch("/status"); const j=await r.json();
  if(!j.ok) return;
  const balancesDiv = document.getElementById("balances");
  const plantelesDiv = document.getElementById("planteles");
  balancesDiv.innerHTML = ""; // planteles only shown via renderPlanteles at mid/end
  for(const [p, data] of Object.entries(j.participants)){
    const b = document.createElement("div"); b.textContent = `${p}: ${data.presupuesto} M`; balancesDiv.appendChild(b);
  }
  document.getElementById("remaining").textContent = "Candidatos restantes: " + j.remaining;
}

// refrescar balances periódicamente (cada 2s)
setInterval(()=>{ if(started) loadStatus(); }, 2000);
