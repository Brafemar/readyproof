"use strict";
(() => {
  const MAX_BYTES=2*1024*1024;
  const $=id=>document.getElementById(id);
  let contexto=null, account=null, database=null, locked=false, working=false, converting=null;
  let guard=null, remote=new Map(), remoteKey=null;

  async function estandarizar(file) {
    const url=URL.createObjectURL(file), image=new Image();
    try {
      await new Promise((resolve,reject)=>{image.onload=resolve;image.onerror=()=>reject(new Error("No se pudo leer la foto. Elegí otra imagen o guardala como JPEG y volvé a intentar desde la app."));image.src=url;});
      if(!image.naturalWidth||!image.naturalHeight)throw new Error("No se pudo leer la foto: elegí otra imagen.");
      const ratio=Math.min(1,1600/Math.max(image.naturalWidth,image.naturalHeight));
      const canvas=document.createElement("canvas");
      canvas.width=Math.max(1,Math.round(image.naturalWidth*ratio));canvas.height=Math.max(1,Math.round(image.naturalHeight*ratio));
      const ctx=canvas.getContext("2d");ctx.fillStyle="#fff";ctx.fillRect(0,0,canvas.width,canvas.height);
      ctx.drawImage(image,0,0,canvas.width,canvas.height);
      const blob=await new Promise(resolve=>canvas.toBlob(resolve,"image/jpeg",0.7));
      if(!blob||blob.type!=="image/jpeg")throw new Error("No se pudo preparar la foto: elegí otra imagen desde la app.");
      if(blob.size>MAX_BYTES)throw new Error("La foto supera 2 MB: vuelva a intentar con la foto de la app");
      return {blob,ancho:canvas.width,alto:canvas.height};
    } finally { URL.revokeObjectURL(url); }
  }
  window.readyproofFotos={estandarizar};

  async function storage(mode,method,...args) {
    const db=await database;
    return new Promise((resolve,reject)=>{
      const tx=db.transaction("pendientes",mode),req=tx.objectStore("pendientes")[method](...args);
      tx.oncomplete=()=>resolve(req.result);tx.onerror=()=>reject(tx.error);tx.onabort=()=>reject(tx.error);
    });
  }
  function status(text) { if(!locked)$("fotos-estado").textContent=text; }
  async function api(url,options={}) {
    const response=await fetch(url,{...options,headers:{"X-CSRF-Token":account.csrf_token,...options.headers}});
    const data=await response.json();
    if(!response.ok){if(response.status===401)window.readyproofExpired();throw new Error(data.error||"No se pudo subir la foto. Conservamos la copia en este dispositivo.");}
    return data;
  }
  async function paint() {
    if(!account||locked)return;
    const selected=contexto,items=await storage("readonly","getAll");
    if(locked||selected!==contexto)return;
    const pending=items.filter(row=>row.localId===selected?.localId);
    const saved=remote.get(selected?.serverId)||[];
    const count=pending.length+(converting===selected?.localId?1:0);
    $("agregar-foto").disabled=!selected||selected.readOnly||Boolean(converting)||saved.length+pending.length>=20;
    $("foto-archivo").disabled=$("agregar-foto").disabled;
    $("fotos-lista").replaceChildren();
    for(const row of saved){const li=document.createElement("li");li.textContent=`Foto ${row.orden} · Guardada · ${row.ancho} × ${row.alto} px` ;$("fotos-lista").append(li);}
    for(const row of pending){const li=document.createElement("li");li.textContent=`Foto pendiente de subir · ${row.ancho} × ${row.alto} px` ;$("fotos-lista").append(li);}
    const next=`${selected?.localId}:${count}`;
    if(next!==guard){guard=next;window.dispatchEvent(new CustomEvent("readyproof-fotos-pendientes",{detail:count}));}
  }
  async function flush() {
    if(!account||locked||working||!navigator.onLine)return;
    working=true;
    try {
      const items=(await storage("readonly","getAll")).sort((a,b)=>a.creado.localeCompare(b.creado));
      for(const row of items){
        if(locked||!navigator.onLine)break;
        const draft=await window.readyproofFotosBorrador?.(row.localId);
        if(!draft?.serverId||draft.pending||draft.conflicto||draft.estado!=="borrador")continue;
        const result=await api(`/api/cargas/${draft.serverId}/fotos`,{method:"POST",headers:{"Content-Type":"image/jpeg","Idempotency-Key":row.id},body:row.blob});
        await storage("readwrite","delete",row.id);
        const saved=remote.get(draft.serverId)||[];
        remote.set(draft.serverId,[...saved.filter(item=>item.id!==result.id),result].sort((a,b)=>a.orden-b.orden));
        status("Foto guardada en la planilla.");
      }
    } catch(error){status(error.message||"Sin conexión. La foto queda guardada en este dispositivo para reintentar.");}
    finally {working=false;await paint();}
  }
  async function refresh() {
    if(!account||locked)return;
    const selected=contexto;
    if(selected?.serverId&&navigator.onLine&&remoteKey!==selected.serverId){
      try{remote.set(selected.serverId,await api(`/api/cargas/${selected.serverId}/fotos`));remoteKey=selected.serverId;}
      catch(error){status(error.message);}
    }
    await paint();await flush();
  }
  window.addEventListener("readyproof-fotos-contexto",event=>{
    contexto=event.detail;
    if(account&&!locked)refresh().catch(error=>status(error.message));
  });
  window.addEventListener("online",()=>{remoteKey=null;refresh().catch(error=>status(error.message));});
  window.addEventListener("readyproof-lock",()=>{
    if(locked)return;
    locked=true;contexto=null;$("agregar-foto").disabled=true;$("foto-archivo").value="";$("fotos-lista").replaceChildren();$("fotos-estado").textContent="";
    database?.then(db=>db.close());
  });
  $("agregar-foto").onclick=()=>$("foto-archivo").click();
  $("foto-archivo").onchange=async event=>{
    const file=event.target.files[0],selected=contexto;
    if(!file||!selected||selected.readOnly||locked)return;
    converting=selected.localId;
    window.dispatchEvent(new CustomEvent("readyproof-fotos-pendientes",{detail:1}));
    try{
      await paint();status("Preparando foto…");
      const ready=await estandarizar(file);
      if(locked)return;
      const id=crypto.randomUUID();
      await storage("readwrite","put",{id,localId:selected.localId,blob:ready.blob,ancho:ready.ancho,alto:ready.alto,creado:new Date().toISOString()});
      status("Foto guardada en este dispositivo. Se subirá al conectar y sincronizar el borrador.");
    } catch(error){status(error.message||"No se pudo guardar la foto. Volvé a intentar y no cierres esta pantalla.");}
    finally{converting=null;event.target.value="";await paint();await flush();}
  };
  (async()=>{
    try{
      account=await window.readyproofSession;
      if(locked)return;
      database=new Promise((resolve,reject)=>{
        const req=indexedDB.open("readyproof-fotos-"+account.usuario.id,1);
        req.onupgradeneeded=()=>req.result.createObjectStore("pendientes",{keyPath:"id"});
        req.onsuccess=()=>resolve(req.result);req.onerror=()=>reject(new Error("No se pudo guardar la foto en el dispositivo: revisá el espacio disponible."));
      });
      await database;await refresh();
    } catch(error){status(error.message);}
  })();
})();
