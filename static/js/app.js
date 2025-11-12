let started = false;

// Normaliza un nombre de jugador a un filename tipo: "aaron_wan_bissaka"
function normalizePlayerName(name){
  if(!name) return '';
  // trim, lowercase, remove diacritics
  let s = name.trim().toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  // replace any non-alphanumeric (letters/numbers) with underscore
  s = s.replace(/[^a-z0-9]+/g, '_');
  // collapse multiple underscores
  s = s.replace(/_+/g, '_');
  // remove leading/trailing underscores
  s = s.replace(/^_|_$/g, '');
  return s;
}

// Genera varias URLs candidatas donde puede estar la imagen en el repo
function getPlayerImageCandidates(playerName){
  const silhouette = 'https://raw.githubusercontent.com/ManriquePeralta/SubastaFutbolera/master/static/images/silueta.webp';
  if(!playerName) return [silhouette];
  const base = normalizePlayerName(playerName);
  if(!base) return [silhouette];

  // posibles ubicaciones en el repo (user provided example includes refs/heads/master)
  const candidates = [
    `https://raw.githubusercontent.com/ManriquePeralta/SubastaFutbolera/refs/heads/master/jugadores/${base}.jpg`,
    `https://raw.githubusercontent.com/ManriquePeralta/SubastaFutbolera/master/jugadores/${base}.jpg`,
    `https://raw.githubusercontent.com/ManriquePeralta/SubastaFutbolera/master/static/images/jugadores/${base}.jpg`,
    `https://raw.githubusercontent.com/ManriquePeralta/SubastaFutbolera/master/static/images/jugadores/${base}.webp`,
  ];
  // always end with silhouette fallback
  candidates.push(silhouette);
  return candidates;
}

// Asigna de forma resiliente la imagen al elemento <img>. Prueba varias URLs y
// si ninguna carga correctamente deja la silueta.
function setPlayerImage(imgEl, playerName){
  const urls = getPlayerImageCandidates(playerName);
  let idx = 0;
  function tryNext(){
    if(idx >= urls.length){
      // nothing worked, ensure silhouette
      imgEl.src = urls[urls.length-1];
      return;
    }
    const url = urls[idx++];
    // create a temporary Image to test loading
    const t = new Image();
    t.onload = function(){ imgEl.src = url; };
    t.onerror = function(){ tryNext(); };
    t.src = url;
  }
  tryNext();
}

function showNotification(text, kind = 'info'){
    // kind: info | success | error
    const container = document.getElementById('notifications');
    const el = document.createElement('div');
    el.className = 'notification ' + kind;
    el.textContent = text;
    container.prepend(el);
    setTimeout(()=>{ el.style.opacity = '0'; setTimeout(()=>el.remove(),600); }, 5000);
}

async function loadFormations(){
  try{
    const r = await fetch('/formations');
    const j = await r.json();
    if(!j.ok) return;
    const sel = document.getElementById('formationSelect');
    // keep RANDOM
    sel.innerHTML = '<option value="RANDOM">RANDOM</option>';
    j.formations.forEach(f=>{ const opt=document.createElement('option'); opt.value=f; opt.textContent=f; sel.appendChild(opt); });
  }catch(e){ /* ignore */ }
}
document.addEventListener('DOMContentLoaded', loadFormations);

document.getElementById("startBtn").addEventListener("click", async ()=>{
  const parts = document.getElementById("participants").value.split(",").map(s=>s.trim()).filter(Boolean);
  const formation = document.getElementById("formationSelect").value;
  if(parts.length < 1){ showNotification("Ingresa al menos un participante", 'error'); return; }
  const res = await fetch("/start", {
    method:"POST", headers:{"Content-Type":"application/json"},
    body: JSON.stringify({participants:parts, formation})
  });
  const j = await res.json();
  if(!j.ok){ showNotification("Error: "+ (j.error||''), 'error'); return; }
  started = true;
  showNotification("Subasta iniciada — " + j.total_items + " candidatos (Formación: " + j.formation + ")", 'success');
  const cf = document.getElementById('chosenFormation'); if(cf) cf.textContent = 'Formación: ' + j.formation;
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
  if(j.Jugador){ 
    showNotification(`Se pasó a: ${j.Jugador}`, 'info');
    // Mostrar la imagen del jugador brevemente
  const img = document.querySelector('.silhouette');
  setPlayerImage(img, j.Jugador);
    setTimeout(() => {
  setPlayerImage(img); // Volver a la silueta
      loadCandidate();
      loadStatus();
    }, 3000); // Mostrar por 3 segundos
  } else {
    loadCandidate();
    loadStatus();
  }
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
  
  // Mostrar la imagen del jugador comprado
  const playerName = j.msg.split(" compró ")[1].split(" por ")[0];
  const img = document.querySelector('.silhouette');
  setPlayerImage(img, playerName);
  
  // Esperar un momento antes de cargar el siguiente
  setTimeout(() => {
  setPlayerImage(img); // Volver a la silueta
    loadCandidate();
    loadStatus();
  }, 2000); // Mostrar por 2 segundos
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

    // create formation visual
    const formation = document.createElement('div'); formation.className = 'formation';

  // Forwards left-to-right (EI, DC, ED)
  const fwdLine = document.createElement('div'); fwdLine.className='line forwards';
  ['EI','DC','ED'].forEach(k=>{
      const players = map[k] || [];
      if(players.length === 0){
        // placeholder empty card
        const pc = document.createElement('div'); pc.className='player-card'; pc.innerHTML = '<div class="player-avatar"></div><div class="player-name">-</div>'; fwdLine.appendChild(pc);
      } else {
        players.forEach(name=>{
          const pc = document.createElement('div'); pc.className='player-card';
          const img = document.createElement('img'); img.className='player-avatar'; img.alt = name;
          setPlayerImage(img, name);
          const nm = document.createElement('div'); nm.className='player-name'; nm.textContent = name;
          pc.appendChild(img); pc.appendChild(nm);
          fwdLine.appendChild(pc);
        })
      }
    });
    formation.appendChild(fwdLine);

    // Midfield (MCD, MC, MCO)
    const midLine = document.createElement('div'); midLine.className='line midfield';
    ['MCD','MC','MCO'].forEach(k=>{
      const players = map[k] || [];
      if(players.length === 0){ const pc = document.createElement('div'); pc.className='player-card'; pc.innerHTML = '<div class="player-avatar"></div><div class="player-name">-</div>'; midLine.appendChild(pc); }
      else { players.forEach(name=>{ const pc = document.createElement('div'); pc.className='player-card'; const img = document.createElement('img'); img.className='player-avatar'; img.alt = name; setPlayerImage(img, name); const nm = document.createElement('div'); nm.className='player-name'; nm.textContent = name; pc.appendChild(img); pc.appendChild(nm); midLine.appendChild(pc); }) }
    });
    formation.appendChild(midLine);

  // Defense left-to-right (DFI, DFC, DFD)
  const defLine = document.createElement('div'); defLine.className='line defense';
  ['DFI','DFC','DFD'].forEach(k=>{
      const players = map[k] || [];
      if(players.length === 0){ const pc = document.createElement('div'); pc.className='player-card'; pc.innerHTML = '<div class="player-avatar"></div><div class="player-name">-</div>'; defLine.appendChild(pc); }
      else { players.forEach(name=>{ const pc = document.createElement('div'); pc.className='player-card'; const img = document.createElement('img'); img.className='player-avatar'; img.alt = name; setPlayerImage(img, name); const nm = document.createElement('div'); nm.className='player-name'; nm.textContent = name; pc.appendChild(img); pc.appendChild(nm); defLine.appendChild(pc); }) }
    });
    formation.appendChild(defLine);

    // Goalkeeper
    const gkLine = document.createElement('div'); gkLine.className='line gkline';
    const gks = map['PO'] || [];
    if(gks.length === 0){ const pc = document.createElement('div'); pc.className='player-card'; pc.innerHTML = '<div class="player-avatar"></div><div class="player-name">-</div>'; gkLine.appendChild(pc); }
    else { gks.forEach(name=>{ const pc = document.createElement('div'); pc.className='player-card'; const img = document.createElement('img'); img.className='player-avatar'; img.alt = name; setPlayerImage(img, name); const nm = document.createElement('div'); nm.className='player-name'; nm.textContent = name; pc.appendChild(img); pc.appendChild(nm); gkLine.appendChild(pc); }) }
    formation.appendChild(gkLine);

    wrap.appendChild(formation);
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
