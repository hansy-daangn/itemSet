import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ─── 1. CSS ───────────────────────────────────────────────────────────────
new_css = """/* ── EDIT BUTTON ── */
.hd-edit{padding:7px 14px;border:1.5px solid var(--b);border-radius:20px;font-size:12px;font-weight:600;cursor:pointer;background:var(--w);color:var(--s);transition:.15s}
.hd-edit.on{border-color:#6C5CE7;color:#6C5CE7;background:#F0EEFF}
/* ── FAB ── */
.fab{position:fixed;bottom:24px;right:24px;z-index:500;display:none;align-items:center;gap:8px;background:var(--o);color:#fff;border:none;border-radius:28px;padding:14px 22px;font-size:13px;font-weight:800;cursor:pointer;box-shadow:0 4px 20px rgba(255,111,15,.35);transition:.2s}
.fab:hover{background:var(--od);transform:translateY(-2px)}
/* ── MODAL ── */
.mo{position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:600;display:none;align-items:flex-end;justify-content:center}
.mo.on{display:flex}
@media(min-width:600px){.mo{align-items:center}}
.mo-box{background:var(--w);border-radius:24px 24px 0 0;padding:24px 20px 32px;width:100%;max-width:520px;max-height:90vh;overflow-y:auto}
@media(min-width:600px){.mo-box{border-radius:20px}}
.mo-head{display:flex;align-items:center;justify-content:space-between;margin-bottom:20px}
.mo-title{font-size:17px;font-weight:900}
.mo-close{font-size:24px;cursor:pointer;color:var(--s);background:none;border:none;line-height:1;padding:0}
.mo-field{margin-bottom:13px}
.mo-lbl{font-size:11px;font-weight:700;color:var(--s);margin-bottom:5px}
.mo-inp{width:100%;padding:10px 12px;border:1.5px solid var(--b);border-radius:10px;font-size:13px;font-family:inherit;outline:none;transition:.15s;background:var(--w)}
.mo-inp:focus{border-color:var(--o)}
.mo-row{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.mo-btn{width:100%;padding:13px;background:var(--o);color:#fff;border:none;border-radius:12px;font-size:14px;font-weight:800;cursor:pointer;margin-top:8px;transition:.15s}
.mo-btn:hover{background:var(--od)}
/* ── AUTOCOMPLETE ── */
.ac-wrap{position:relative}
.ac-drop{position:absolute;top:calc(100% + 4px);left:0;right:0;background:var(--w);border:1.5px solid var(--b);border-radius:12px;box-shadow:0 8px 28px rgba(0,0,0,.13);z-index:700;max-height:260px;overflow-y:auto;display:none}
.ac-drop.on{display:block}
.ac-item{padding:9px 14px;cursor:pointer;display:flex;align-items:center;gap:10px;border-bottom:1px solid var(--b)}
.ac-item:last-child{border-bottom:none}
.ac-item:hover{background:var(--ol)}
.ac-nm{font-size:13px;font-weight:700;flex:1}
.ac-cat{font-size:10px;color:var(--s)}
.ac-vol{font-size:10px;color:var(--o);font-weight:700;white-space:nowrap}
/* ── EDIT CONTROLS ── */
.del-btn{position:absolute;top:5px;right:5px;width:22px;height:22px;background:#E8291A;color:#fff;border:none;border-radius:50%;font-size:16px;line-height:22px;text-align:center;cursor:pointer;display:none;z-index:20;padding:0;font-weight:900}
.edit-on .del-btn{display:block}
.ic-del{position:absolute;top:6px;right:6px;width:22px;height:22px;background:#E8291A;color:#fff;border:none;border-radius:50%;font-size:16px;line-height:22px;text-align:center;cursor:pointer;z-index:20;padding:0;font-weight:900}
.add-item-card{background:var(--w);border:2px dashed var(--b);border-radius:14px;min-height:110px;display:flex;align-items:center;justify-content:center;cursor:pointer;flex-direction:column;gap:6px;color:var(--s);font-size:12px;font-weight:700;transition:.15s}
.add-item-card:hover{border-color:var(--o);color:var(--o);background:var(--ol)}
.ic.dragging{opacity:.35;transform:scale(.97)}
.ic.drag-over{outline:2.5px dashed var(--o);outline-offset:2px}
"""
content = content.replace('</style>', new_css + '\n</style>', 1)

# ─── 2. Header: edit button ───────────────────────────────────────────────
content = content.replace(
    "    <button class=\"hd-btn\" id=\"btn-data\" onclick=\"setView('data')\">📊 데이터</button>",
    "    <button class=\"hd-btn\" id=\"btn-data\" onclick=\"setView('data')\">📊 데이터</button>\n    <button class=\"hd-btn hd-edit\" id=\"btn-edit\" onclick=\"toggleEditMode()\">✏️ 편집</button>",
    1
)

# ─── 3. FAB + Modal HTML before </body> ──────────────────────────────────
fab_html = """
<!-- FAB SAVE -->
<button class="fab" id="fabSave" onclick="saveAll()">💾 저장하기</button>

<!-- MODAL -->
<div class="mo" id="modal" onclick="if(event.target===this)closeModal()">
  <div class="mo-box" id="modalBox"></div>
</div>
"""
content = content.replace('</body>', fab_html + '\n</body>', 1)

# ─── 4. Replace renderItems ───────────────────────────────────────────────
old_render = """function renderItems(){
  const grid = document.getElementById('itemsGrid');
  const empty = document.getElementById('emptyState');
  if(!curPersona || !curVersion){
    grid.style.display='none'; empty.style.display='block'; return;
  }
  empty.style.display='none'; grid.style.display='grid';
  const items = ITEMS[curPersona][curVersion];
  grid.innerHTML = items.map((item, i)=>{
    const url = 'https://www.daangn.com/kr/buy-sell/s/?in=%EC%97%AD%EC%82%BC%EB%8F%99-6035&search=' + encodeURIComponent(item.nm);
    const crVal = CAT_CR[item.cat];
    const crHtml = crVal ? `<span class="ic-cr">거래완료율 ${crVal}%</span>` : '';
    const metaTxt = item.meta.replace(/^[📊⚡]\\s*/u, '');
    const metaHtml = metaTxt ? `<span class="ic-mv">${metaTxt}</span>` : '';
    return `
    <div class="ic">
      <div class="ic-img">
        <div class="ic-rank">${i+1}위</div>
        <div class="ic-disc">-${item.disc}</div>
      </div>
      <div class="ic-body">
        <div class="ic-cat">${item.cat}</div>
        <div class="ic-nm">${item.nm}</div>
        <div class="ic-pr">
          <span class="ic-p">${item.p}</span>
          <span class="ic-op">${item.op}</span>
        </div>
        <div class="ic-meta">${crHtml}${metaHtml}</div>
        <div class="ic-hook">${item.hook}</div>
        <a class="ic-btn" href="${url}" target="_blank">당근에서 보기</a>
      </div>
    </div>`;
  }).join('');
}"""

new_render = r"""function renderItems(){
  const grid = document.getElementById('itemsGrid');
  const empty = document.getElementById('emptyState');
  if(!curPersona || !curVersion){
    grid.style.display='none'; empty.style.display='block'; return;
  }
  if(!ITEMS[curPersona]) ITEMS[curPersona]={};
  if(!ITEMS[curPersona][curVersion]) ITEMS[curPersona][curVersion]=[];
  empty.style.display='none'; grid.style.display='grid';
  const items = ITEMS[curPersona][curVersion];
  const pid=curPersona, vid=curVersion;
  grid.innerHTML = items.map((item, i)=>{
    const url = 'https://www.daangn.com/kr/buy-sell/s/?in=%EC%97%AD%EC%82%BC%EB%8F%99-6035&search=' + encodeURIComponent(item.nm);
    const crVal = CAT_CR[item.cat];
    const crHtml = crVal ? `<span class="ic-cr">거래완료율 ${crVal}%</span>` : '';
    const metaTxt = (item.meta||'').replace(/^[📊⚡]\s*/u, '');
    const metaHtml = metaTxt ? `<span class="ic-mv">${metaTxt}</span>` : '';
    const discHtml = item.disc ? `<div class="ic-disc">-${item.disc}</div>` : '';
    const dragAttr = editMode ? 'draggable="true"' : '';
    const delBtn  = editMode ? `<button class="ic-del" onclick="deleteItem('${pid}','${vid}',${i})" title="삭제">×</button>` : '';
    return `
    <div class="ic" style="position:relative" ${dragAttr} data-idx="${i}">
      ${delBtn}
      <div class="ic-img">
        <div class="ic-rank">${i+1}위</div>
        ${discHtml}
      </div>
      <div class="ic-body">
        <div class="ic-cat">${item.cat||''}</div>
        <div class="ic-nm">${item.nm}</div>
        <div class="ic-pr">
          <span class="ic-p">${item.p||''}</span>
          <span class="ic-op">${item.op||''}</span>
        </div>
        <div class="ic-meta">${crHtml}${metaHtml}</div>
        <div class="ic-hook">${item.hook||''}</div>
        <a class="ic-btn" href="${url}" target="_blank">당근에서 보기</a>
      </div>
    </div>`;
  }).join('');
  if(editMode){
    grid.innerHTML += `<div class="add-item-card" onclick="showAddItemModal('${pid}','${vid}')"><div style="font-size:28px">+</div><div>매물 추가</div></div>`;
  }
  if(editMode) setupItemDrag(grid, pid, vid);
}"""

content = content.replace(old_render, new_render, 1)

# ─── 5. Replace init() ───────────────────────────────────────────────────
old_init = """// INIT
function init(){
  // Personas
  const pr = document.getElementById('personaRow');
  PERSONAS.forEach(p=>{
    const d = document.createElement('div');
    d.className='p-card'; d.dataset.pid=p.id;
    d.innerHTML=`<div class="p-em">${p.em}</div><div class="p-nm">${p.name}</div><div class="p-dsc">${p.short}</div>`;
    d.onclick=()=>selectPersona(p.id);
    pr.appendChild(d);
  });
  // Versions
  const vr = document.getElementById('versionRow');
  VERSIONS.forEach(v=>{
    const b = document.createElement('button');
    b.className='v-tab'; b.dataset.vid=v.id;
    b.textContent=v.label;
    b.onclick=()=>selectVersion(v.id);
    vr.appendChild(b);
  });
  // Top combos
  renderTopCombos();
}
init();"""

new_init = """// INIT
function init(){
  loadFromStorage();
  renderPersonaRow();
  renderVersionRow();
  renderTopCombos();
}
init();"""

content = content.replace(old_init, new_init, 1)

# ─── 6. New JS block — insert before "// INIT" ───────────────────────────
new_js = r"""
// ═══════════════════════════════════════════════════════════════════════════
// PERSISTENCE & EDIT MODE
// ═══════════════════════════════════════════════════════════════════════════
let isDirty = false;
let editMode = false;

function loadFromStorage(){
  try{
    const raw = localStorage.getItem('daangn-pt-v2');
    if(!raw) return;
    const d = JSON.parse(raw);
    if(d.personas){ PERSONAS.length=0; d.personas.forEach(p=>PERSONAS.push(p)); }
    if(d.versions){ VERSIONS.length=0; d.versions.forEach(v=>VERSIONS.push(v)); }
    if(d.items){ Object.keys(d.items).forEach(k=>{ ITEMS[k]=d.items[k]; }); }
  }catch(e){ console.error('load failed',e); }
}

function saveAll(){
  localStorage.setItem('daangn-pt-v2', JSON.stringify({
    personas:PERSONAS, versions:VERSIONS, items:ITEMS
  }));
  isDirty=false; updateFab();
  const btn=document.getElementById('fabSave');
  btn.innerHTML='✅ 저장됨';
  setTimeout(()=>{ btn.innerHTML='💾 저장하기'; },1800);
}

function markDirty(){ isDirty=true; updateFab(); }
function updateFab(){
  const el=document.getElementById('fabSave');
  if(el) el.style.display=isDirty?'flex':'none';
}

window.addEventListener('beforeunload', e=>{
  if(isDirty){ e.preventDefault(); e.returnValue=''; }
});

function toggleEditMode(){
  editMode=!editMode;
  const btn=document.getElementById('btn-edit');
  btn.classList.toggle('on',editMode);
  btn.textContent=editMode?'✏️ 편집 중':'✏️ 편집';
  document.body.classList.toggle('edit-on',editMode);
  renderPersonaRow(); renderVersionRow(); renderItems();
}

// ═══════════════════════════════════════════════════════════════════════════
// RENDER ROWS (with edit support)
// ═══════════════════════════════════════════════════════════════════════════
function renderPersonaRow(){
  const pr=document.getElementById('personaRow');
  pr.innerHTML='';
  PERSONAS.forEach(p=>{
    const wrap=document.createElement('div');
    wrap.style.cssText='position:relative;flex:0 0 auto';
    const d=document.createElement('div');
    d.className='p-card'+(curPersona===p.id?' on':'');
    d.dataset.pid=p.id;
    d.innerHTML=`<div class="p-em">${p.em}</div><div class="p-nm">${p.name}</div><div class="p-dsc">${p.short}</div>`;
    d.onclick=()=>selectPersona(p.id);
    wrap.appendChild(d);
    if(editMode){
      const del=document.createElement('button');
      del.className='del-btn'; del.textContent='×'; del.title='삭제';
      del.onclick=e=>{ e.stopPropagation(); deletePersona(p.id); };
      wrap.appendChild(del);
    }
    pr.appendChild(wrap);
  });
  if(editMode){
    const btn=document.createElement('button');
    btn.style.cssText='flex:0 0 auto;width:176px;min-height:92px;background:var(--w);border:2px dashed var(--b);border-radius:16px;padding:14px;cursor:pointer;color:var(--s);font-size:13px;font-weight:700;display:flex;align-items:center;justify-content:center;gap:6px;transition:.15s';
    btn.innerHTML='<span style="font-size:22px">+</span> 페르소나 추가';
    btn.onmouseenter=()=>{btn.style.borderColor='var(--o)';btn.style.color='var(--o)'};
    btn.onmouseleave=()=>{btn.style.borderColor='var(--b)';btn.style.color='var(--s)'};
    btn.onclick=()=>showAddPersonaModal();
    pr.appendChild(btn);
  }
}

function renderVersionRow(){
  const vr=document.getElementById('versionRow');
  vr.innerHTML='';
  VERSIONS.forEach(v=>{
    const wrap=document.createElement('div');
    wrap.style.cssText='position:relative;flex:0 0 auto';
    const b=document.createElement('button');
    b.className='v-tab'+(curVersion===v.id?' on':'');
    b.dataset.vid=v.id; b.textContent=v.label;
    b.onclick=()=>selectVersion(v.id);
    wrap.appendChild(b);
    if(editMode){
      const del=document.createElement('button');
      del.className='del-btn'; del.style.cssText='display:block;top:0;right:0;width:18px;height:18px;font-size:12px;line-height:18px';
      del.textContent='×'; del.title='삭제';
      del.onclick=e=>{ e.stopPropagation(); deleteVersion(v.id); };
      wrap.appendChild(del);
    }
    vr.appendChild(wrap);
  });
  if(editMode){
    const btn=document.createElement('button');
    btn.style.cssText='flex:0 0 auto;padding:9px 17px;border:1.5px dashed var(--b);border-radius:24px;font-size:13px;font-weight:700;cursor:pointer;background:var(--w);color:var(--s);white-space:nowrap;transition:.15s';
    btn.textContent='+ 버전 추가';
    btn.onmouseenter=()=>{btn.style.borderColor='var(--o)';btn.style.color='var(--o)'};
    btn.onmouseleave=()=>{btn.style.borderColor='var(--b)';btn.style.color='var(--s)'};
    btn.onclick=()=>showAddVersionModal();
    vr.appendChild(btn);
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// DELETE
// ═══════════════════════════════════════════════════════════════════════════
function deletePersona(pid){
  if(!confirm('이 페르소나를 삭제하시겠습니까?')) return;
  const idx=PERSONAS.findIndex(p=>p.id===pid);
  if(idx>=0) PERSONAS.splice(idx,1);
  delete ITEMS[pid];
  if(curPersona===pid){ curPersona=null; document.getElementById('pInsight').className='p-insight'; }
  markDirty(); renderPersonaRow(); renderItems();
}

function deleteVersion(vid){
  if(!confirm('이 버전을 삭제하시겠습니까?')) return;
  const idx=VERSIONS.findIndex(v=>v.id===vid);
  if(idx>=0) VERSIONS.splice(idx,1);
  Object.keys(ITEMS).forEach(pid=>{ if(ITEMS[pid]) delete ITEMS[pid][vid]; });
  if(curVersion===vid){ curVersion=null; }
  markDirty(); renderVersionRow(); renderItems();
}

function deleteItem(pid, vid, idx){
  if(!ITEMS[pid]||!ITEMS[pid][vid]) return;
  ITEMS[pid][vid].splice(idx,1);
  markDirty(); renderItems();
}

// ═══════════════════════════════════════════════════════════════════════════
// DRAG & DROP (item reorder)
// ═══════════════════════════════════════════════════════════════════════════
let dragSrcIdx=null;

function setupItemDrag(grid, pid, vid){
  const cards=Array.from(grid.querySelectorAll('.ic[draggable="true"]'));
  cards.forEach((card,idx)=>{
    card.addEventListener('dragstart', e=>{
      dragSrcIdx=idx; e.dataTransfer.effectAllowed='move';
      setTimeout(()=>card.classList.add('dragging'),0);
    });
    card.addEventListener('dragend', ()=>card.classList.remove('dragging'));
    card.addEventListener('dragover', e=>{ e.preventDefault(); card.classList.add('drag-over'); });
    card.addEventListener('dragleave', ()=>card.classList.remove('drag-over'));
    card.addEventListener('drop', e=>{
      e.preventDefault(); card.classList.remove('drag-over');
      if(dragSrcIdx===null||dragSrcIdx===idx) return;
      const arr=ITEMS[pid][vid];
      const [moved]=arr.splice(dragSrcIdx,1);
      arr.splice(idx,0,moved);
      dragSrcIdx=null;
      markDirty(); renderItems();
    });
  });
}

// ═══════════════════════════════════════════════════════════════════════════
// AUTOCOMPLETE
// ═══════════════════════════════════════════════════════════════════════════
let acCache=null;

function getAcData(){
  if(acCache) return acCache;
  const map={};
  Object.values(ITEMS).forEach(pvObj=>{
    if(!pvObj) return;
    Object.values(pvObj).forEach(arr=>{
      if(!Array.isArray(arr)) return;
      arr.forEach(it=>{
        if(!it||!it.nm) return;
        if(!map[it.nm]) map[it.nm]={...it, vol:parseVol(it.meta||'')};
      });
    });
  });
  acCache=Object.values(map).sort((a,b)=>b.vol-a.vol);
  return acCache;
}

function showAcDrop(input, drop){
  const q=input.value.trim();
  const list=getAcData();
  const filtered=q
    ? list.filter(i=>(i.nm&&i.nm.includes(q))||(i.cat&&i.cat.includes(q)))
    : list.slice(0,20);
  if(!filtered.length){ drop.classList.remove('on'); return; }
  drop.innerHTML=filtered.slice(0,20).map(it=>{
    const e=s=>(s||'').replace(/\\/g,'\\\\').replace(/'/g,"\\'").replace(/"/g,'&quot;');
    return `<div class="ac-item" onmousedown="selectAcItem(event,'${e(it.nm)}','${e(it.cat||'')}','${e(it.p||'')}','${e(it.op||'')}','${e(it.disc||'')}','${e(it.meta||'')}','${e(it.hook||'')}')">
      <div class="ac-nm">${it.nm}</div>
      <div class="ac-cat">${it.cat||''}</div>
      <div class="ac-vol">${fmtVol(it.vol)}</div>
    </div>`;
  }).join('');
  drop.classList.add('on');
}

function selectAcItem(e,nm,cat,p,op,disc,meta,hook){
  e.preventDefault();
  const s=(id,v)=>{ const el=document.getElementById(id); if(el) el.value=v; };
  s('mo-nm',nm); s('mo-cat',cat); s('mo-p',p); s('mo-op',op);
  s('mo-disc',disc); s('mo-meta',meta); s('mo-hook',hook);
  const drop=document.querySelector('.ac-drop');
  if(drop) drop.classList.remove('on');
}

// ═══════════════════════════════════════════════════════════════════════════
// MODALS
// ═══════════════════════════════════════════════════════════════════════════
function closeModal(){ document.getElementById('modal').classList.remove('on'); }

function showAddItemModal(pid, vid){
  acCache=null;
  document.getElementById('modalBox').innerHTML=`
    <div class="mo-head">
      <div class="mo-title">매물 추가</div>
      <button class="mo-close" onclick="closeModal()">×</button>
    </div>
    <div class="mo-field">
      <div class="mo-lbl">상품명 * <small style="font-weight:400;color:var(--s)">— 입력하면 자동완성, 공란 클릭 시 인기순</small></div>
      <div class="ac-wrap">
        <input id="mo-nm" class="mo-inp" placeholder="노트북, 자전거, 에어컨…" autocomplete="off"
          oninput="showAcDrop(this,this.closest('.ac-wrap').querySelector('.ac-drop'))"
          onfocus="showAcDrop(this,this.closest('.ac-wrap').querySelector('.ac-drop'))"
          onblur="setTimeout(()=>this.closest('.ac-wrap').querySelector('.ac-drop').classList.remove('on'),200)"/>
        <div class="ac-drop"></div>
      </div>
    </div>
    <div class="mo-row">
      <div class="mo-field"><div class="mo-lbl">카테고리</div><input id="mo-cat" class="mo-inp" placeholder="디지털기기"/></div>
      <div class="mo-field"><div class="mo-lbl">중고가</div><input id="mo-p" class="mo-inp" placeholder="13만원"/></div>
      <div class="mo-field"><div class="mo-lbl">원가(정가)</div><input id="mo-op" class="mo-inp" placeholder="80만원"/></div>
      <div class="mo-field"><div class="mo-lbl">할인율</div><input id="mo-disc" class="mo-inp" placeholder="84%"/></div>
    </div>
    <div class="mo-field"><div class="mo-lbl">검색량/완료율 메모</div><input id="mo-meta" class="mo-inp" placeholder="검색 2.68M/월 · 완료율 46%"/></div>
    <div class="mo-field"><div class="mo-lbl">후킹 문구</div><input id="mo-hook" class="mo-inp" placeholder="월 268만 클릭, 반값에 득템"/></div>
    <button class="mo-btn" onclick="confirmAddItem('${pid}','${vid}')">추가하기</button>
  `;
  document.getElementById('modal').classList.add('on');
  setTimeout(()=>{
    const el=document.getElementById('mo-nm');
    if(el){ el.focus(); showAcDrop(el, el.closest('.ac-wrap').querySelector('.ac-drop')); }
  },150);
}

function confirmAddItem(pid, vid){
  const nm=(document.getElementById('mo-nm').value||'').trim();
  if(!nm){ alert('상품명을 입력해주세요'); return; }
  const g=id=>(document.getElementById(id)||{}).value||'';
  if(!ITEMS[pid]) ITEMS[pid]={};
  if(!ITEMS[pid][vid]) ITEMS[pid][vid]=[];
  ITEMS[pid][vid].push({
    cat:g('mo-cat')||'기타', nm,
    p:g('mo-p'), op:g('mo-op'),
    disc:g('mo-disc').replace('%',''),
    meta:g('mo-meta'), hook:g('mo-hook')
  });
  acCache=null;
  closeModal(); markDirty(); renderItems();
}

function showAddPersonaModal(){
  document.getElementById('modalBox').innerHTML=`
    <div class="mo-head">
      <div class="mo-title">페르소나 추가</div>
      <button class="mo-close" onclick="closeModal()">×</button>
    </div>
    <div class="mo-field"><div class="mo-lbl">이모지</div><input id="mo-em" class="mo-inp" style="font-size:20px" placeholder="🏃"/></div>
    <div class="mo-field"><div class="mo-lbl">이름 *</div><input id="mo-pname" class="mo-inp" placeholder="운동 마니아"/></div>
    <div class="mo-field"><div class="mo-lbl">한줄 설명</div><input id="mo-pshort" class="mo-inp" placeholder="25-40세 · 헬스/러닝"/></div>
    <div class="mo-field"><div class="mo-lbl">설명 (선택)</div><input id="mo-pdesc" class="mo-inp" placeholder="운동 장비 전문 구매자"/></div>
    <button class="mo-btn" onclick="confirmAddPersona()">추가하기</button>
  `;
  document.getElementById('modal').classList.add('on');
  setTimeout(()=>document.getElementById('mo-pname').focus(),100);
}

function confirmAddPersona(){
  const name=(document.getElementById('mo-pname').value||'').trim();
  if(!name){ alert('이름을 입력해주세요'); return; }
  const id='p'+Date.now();
  PERSONAS.push({
    id, em:document.getElementById('mo-em').value.trim()||'👤',
    name, short:document.getElementById('mo-pshort').value.trim()||name,
    desc:document.getElementById('mo-pdesc').value.trim(),
    tags:[name], profile:name, trigger:'-', topQuery:'-', adResp:'-', category:'-', spend:'-'
  });
  if(!ITEMS[id]) ITEMS[id]={};
  VERSIONS.forEach(v=>{ if(!ITEMS[id][v.id]) ITEMS[id][v.id]=[]; });
  closeModal(); markDirty(); renderPersonaRow();
}

function showAddVersionModal(){
  document.getElementById('modalBox').innerHTML=`
    <div class="mo-head">
      <div class="mo-title">버전 추가</div>
      <button class="mo-close" onclick="closeModal()">×</button>
    </div>
    <div class="mo-field"><div class="mo-lbl">이모지</div><input id="mo-vem" class="mo-inp" style="font-size:20px" placeholder="🎪"/></div>
    <div class="mo-field"><div class="mo-lbl">버전 이름 *</div><input id="mo-vlabel" class="mo-inp" placeholder="버전7 · 선물용"/></div>
    <div class="mo-field"><div class="mo-lbl">광고 카피</div><input id="mo-vtitle" class="mo-inp" placeholder="선물은 당근에서 반값에!"/></div>
    <div class="mo-field"><div class="mo-lbl">설명 (선택)</div><input id="mo-vdesc" class="mo-inp" placeholder="선물 시즌 공략…"/></div>
    <button class="mo-btn" onclick="confirmAddVersion()">추가하기</button>
  `;
  document.getElementById('modal').classList.add('on');
  setTimeout(()=>document.getElementById('mo-vlabel').focus(),100);
}

function confirmAddVersion(){
  const label=(document.getElementById('mo-vlabel').value||'').trim();
  if(!label){ alert('버전 이름을 입력해주세요'); return; }
  const em=document.getElementById('mo-vem').value.trim()||'🆕';
  const id='v'+Date.now();
  VERSIONS.push({
    id, label:em+' '+label,
    title:document.getElementById('mo-vtitle').value.trim()||label,
    desc:document.getElementById('mo-vdesc').value.trim(),
    stats:[]
  });
  PERSONAS.forEach(p=>{ if(!ITEMS[p.id]) ITEMS[p.id]={}; ITEMS[p.id][id]=[]; });
  closeModal(); markDirty(); renderVersionRow();
}

"""

content = content.replace('// INIT\nfunction init(){', new_js + '// INIT\nfunction init(){', 1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Done!')
