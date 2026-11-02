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
  window.readyproofFotos={estandarizar,validarMarca,validarMarcas,numerarMarcas};

  async function almacen(store,mode,method,...args) {
    const db=await database;
    return new Promise((resolve,reject)=>{
      const tx=db.transaction(store,mode),req=tx.objectStore(store)[method](...args);
      tx.oncomplete=()=>resolve(req.result);tx.onerror=()=>reject(tx.error);tx.onabort=()=>reject(tx.error);
    });
  }
  const storage=(mode,method,...args)=>almacen("pendientes",mode,method,...args);
  const RESULTADOS=["✓","O","X","NA"];
  const SIGNIFICADO_RESULTADOS={"✓":"cumple","O":"no cumple","X":"no apreciable","NA":"no aplicable"};
  let editor=null, editorURL=null, editorToken=0, escritura=Promise.resolve(), sincronizandoMarcas=false, repetirSincronizacion=false;
  window.readyproofActualizacionFotos = async () => {
    if (!account || !database || locked) return "Esperá a que se abra la sesión y el almacenamiento de fotos.";
    if (converting || working || sincronizandoMarcas) return "Esperá a que termine la preparación o la sincronización de las fotos.";
    if (editor) return "Guardá las marcas y cerrá la foto antes de actualizar.";
    const pendingWrite = escritura;
    await pendingWrite;
    const photos = await storage("readonly", "getAll");
    const marks = await almacen("anotaciones", "readonly", "getAll");
    if (converting || working || sincronizandoMarcas || editor || pendingWrite !== escritura || photos.length || marks.some(row => row.pendienteServidor || row.borradorMarcas != null || row.conflicto))
      return "Hay fotos o marcas pendientes. Guardalas y sincronizalas antes de actualizar.";
    return "";
  };

  function numerarMarcas(marcas) { return marcas.map((marca,i)=>({...marca,numero:i+1})); }
  function validarMarca(marca) {
    if(!Number.isFinite(marca.x)||!Number.isFinite(marca.y)||marca.x<0||marca.x>1||marca.y<0||marca.y>1)
      throw new Error("La posición debe estar dentro de la foto: volvé a colocar la marca.");
    if(!RESULTADOS.includes(marca.codigo))throw new Error("Elegí un código válido: ✓, O, X o NA.");
    if(typeof marca.texto!=="string"||Array.from(marca.texto).length>140)
      throw new Error("El texto debe tener hasta 140 caracteres: acortá la observación.");
    if(["O","X"].includes(marca.codigo)&&!marca.texto.trim())
      throw new Error(`Completá el texto de la observación para el código ${marca.codigo}.`);
    return {...marca,x:marca.x,y:marca.y,codigo:marca.codigo,texto:marca.texto};
  }
  function validarMarcas(marcas) {
    return numerarMarcas(marcas.map((marca,i)=>{
      try{return validarMarca(marca);}catch(error){throw new Error(`Marca ${i+1}: ${error.message}`);}
    }));
  }
  function soloLectura() { return locked||!contexto||contexto.readOnly||editor?.localId!==contexto.localId; }
  function mensajeEditor(text) { if(!locked)$("foto-marcas-estado").textContent=text; }
  function cerrarEditor() {
    editorToken++;editor=null;
    if(editorURL)URL.revokeObjectURL(editorURL);editorURL=null;
    $("foto-servidor-version").hidden=true;$("foto-servidor-lista").replaceChildren();
    $("foto-editor").hidden=true;$("foto-editor-imagen").removeAttribute("src");
    $("foto-marcas").replaceChildren();$("foto-anotaciones").replaceChildren();$("foto-marcas-estado").textContent="";
  }
  function escribirAnotaciones(values,combinar=null) {
    const task=escritura.then(async()=>{
      if(locked)throw new Error("La sesión se cerró: volvé a ingresar antes de guardar las marcas.");
      const previous=await almacen("anotaciones","readonly","get",values.id);
      await almacen("anotaciones","readwrite","put",{...previous,...values,...(combinar?combinar(previous):{}),actualizado:new Date().toISOString()});
    });
    escritura=task.catch(()=>{});return task;
  }
  function guardarBorradorMarcas() {
    const active=editor;if(!active||soloLectura())return;
    active.revision++;
    mensajeEditor("Borrador de marcas en este dispositivo. Completá los datos y presioná Guardar marcas.");
    escribirAnotaciones({id:active.id,localId:active.localId,borradorMarcas:numerarMarcas(active.marcas).map(m=>({...m}))}).then(()=>paint())
      .catch(error=>{if(editor===active)mensajeEditor("No se pudo guardar el borrador: "+error.message);});
  }
  function seleccionarMarca(id,focus=false) {
    if(!editor)return;editor.seleccion=id;
    for(const button of $("foto-marcas").children)button.classList.toggle("seleccionada",button.dataset.id===id);
    for(const row of $("foto-anotaciones").children)row.classList.toggle("seleccionada",row.dataset.id===id);
    if(focus)$("foto-codigo-"+id)?.focus();
  }
  function pintarMarcadores() {
    $("foto-marcas").replaceChildren();if(!editor)return;
    editor.marcas.forEach((marca,i)=>{
      const button=document.createElement("button");button.type="button";button.className="foto-marca";
      button.dataset.id=marca.id;button.textContent=String(i+1);button.style.left=`${marca.x*100}%`;button.style.top=`${marca.y*100}%`;
      button.setAttribute("aria-label",`Editar marca ${i+1}`);
      button.onclick=event=>{event.stopPropagation();seleccionarMarca(marca.id,true);};
      $("foto-marcas").append(button);
    });
    seleccionarMarca(editor.seleccion);
  }
  function pintarEditor() {
    if(!editor)return;const readOnly=soloLectura();
    $("foto-editor-titulo").textContent=editor.orden?`Marcas de la foto ${editor.orden}`:"Marcas de la foto pendiente";
    $("foto-guardar-marcas").disabled=readOnly;$("foto-agregar-marca").disabled=readOnly;
    $("foto-anotaciones").replaceChildren();
    editor.marcas.forEach((marca,i)=>{
      const li=document.createElement("li");li.dataset.id=marca.id;
      const heading=document.createElement("strong");heading.textContent=`Marca ${i+1}`;li.append(heading);
      const codeLabel=document.createElement("label");codeLabel.textContent="Código";codeLabel.htmlFor="foto-codigo-"+marca.id;
      const select=document.createElement("select");select.id=codeLabel.htmlFor;select.disabled=readOnly;
      for(const value of ["",...RESULTADOS]){const option=document.createElement("option");option.value=value;option.textContent=value?`${value} (${SIGNIFICADO_RESULTADOS[value]})`:"Elegí un código";select.append(option);}select.value=marca.codigo;
      const label=document.createElement("label");label.htmlFor="foto-texto-"+marca.id;
      const textarea=document.createElement("textarea");textarea.id=label.htmlFor;textarea.rows=3;textarea.maxLength=140;textarea.value=marca.texto;textarea.disabled=readOnly;
      const hint=document.createElement("span");hint.className="foto-texto-ayuda";
      const updateHint=()=>{textarea.required=["O","X"].includes(marca.codigo);label.textContent=textarea.required?"Texto obligatorio":"Texto (opcional)";hint.textContent=`${Array.from(marca.texto).length}/140 caracteres`;};updateHint();
      select.onchange=()=>{if(soloLectura())return;marca.codigo=select.value;updateHint();guardarBorradorMarcas();};
      textarea.oninput=()=>{if(soloLectura())return;marca.texto=textarea.value;updateHint();guardarBorradorMarcas();};
      const remove=document.createElement("button");remove.type="button";remove.className="button secondary small";remove.textContent=`Borrar marca ${i+1}`;remove.disabled=readOnly;
      remove.onclick=()=>{if(soloLectura())return;const active=editor;active.marcas=active.marcas.filter(m=>m.id!==marca.id);active.seleccion=active.marcas[Math.min(i,active.marcas.length-1)]?.id;guardarBorradorMarcas();pintarEditor();};
      const items=editor.items||[];
      if(items.length||marca.item){
        const itemLabel=document.createElement("label");itemLabel.textContent="Ítem del punto 2";itemLabel.htmlFor="foto-item-"+marca.id;
        const itemSelect=document.createElement("select");itemSelect.id=itemLabel.htmlFor;itemSelect.disabled=readOnly;
        const opciones=[...items];if(marca.item&&!opciones.some(row=>row.bloque===marca.item.bloque&&row.campo===marca.item.campo))opciones.push(marca.item);
        const empty=document.createElement("option");empty.value="";empty.textContent="Elegí el ítem";itemSelect.append(empty);
        const grupos=new Map();for(const item of opciones){if(!grupos.has(item.bloque)){const grupo=document.createElement("optgroup");grupo.label=item.bloque;itemSelect.append(grupo);grupos.set(item.bloque,grupo);}const option=document.createElement("option");option.value=JSON.stringify([item.bloque,item.campo]);option.textContent=item.texto;grupos.get(item.bloque).append(option);}
        itemSelect.value=marca.item?JSON.stringify([marca.item.bloque,marca.item.campo]):"";
        select.disabled=readOnly||!marca.item;
        itemSelect.onchange=()=>{if(soloLectura())return;const item=opciones.find(row=>JSON.stringify([row.bloque,row.campo])===itemSelect.value);if(item)marca.item={...item};else delete marca.item;select.disabled=soloLectura()||!marca.item;guardarBorradorMarcas();};
        li.append(itemLabel,itemSelect);
      }
      li.append(codeLabel,select,label,textarea,hint,remove);$("foto-anotaciones").append(li);
    });
    pintarMarcadores();
    mostrarVersionServidor();
    if(readOnly)mensajeEditor("Solo lectura: la planilla no permite editar las marcas.");
  }
  function agregarMarca(x,y) {
    if(!editor||soloLectura())return;
    const marca={id:crypto.randomUUID(),x,y,codigo:"",texto:""};editor.marcas.push(marca);editor.seleccion=marca.id;
    guardarBorradorMarcas();pintarEditor();seleccionarMarca(marca.id,true);
  }
  async function apiMarcas(cargaId,fotoId,options={}) {
    const response=await fetch(`/api/cargas/${cargaId}/fotos/${fotoId}/anotaciones`,{cache:"no-store",...options,headers:{"X-CSRF-Token":account.csrf_token,...options.headers}});
    const data=await response.json();
    if(!response.ok){if(response.status===401)window.readyproofExpired();const error=new Error(data.error||"No se pudieron guardar las marcas: conservamos el borrador para reintentar.");error.estado=response.status;throw error;}
    return {marcas:data,version:response.headers.get("ETag")};
  }
  async function leerMarcasServidor(cargaId,fotoId,localId) {
    const result=await apiMarcas(cargaId,fotoId);
    await escribirAnotaciones({id:fotoId,localId,serverId:cargaId},previous=>{
      const legado=previous&&Object.hasOwn(previous,"marcas")&&!previous.versionServidor;
      const preservar=previous?.borradorMarcas!=null||previous?.pendienteServidor||legado;
      return {servidorMarcas:result.marcas,versionActual:result.version,
        ...(!preservar?{marcas:result.marcas,versionServidor:result.version,conflicto:false}:{}),
        ...(legado?{borradorMarcas:previous.borradorMarcas??previous.marcas,versionServidor:result.version,conflicto:result.marcas.length>0}:{} )};
    });
    return result;
  }
  function mostrarVersionServidor() {
    if(!editor)return;
    const panel=$("foto-servidor-version");panel.hidden=!editor.conflicto;
    $("foto-servidor-lista").replaceChildren();
    for(const marca of editor.servidorMarcas||[]){const li=document.createElement("li");li.textContent=`${marca.numero} · ${marca.codigo} · ${marca.texto||"Sin texto"}`;$("foto-servidor-lista").append(li);}
    if(!(editor.servidorMarcas||[]).length){const li=document.createElement("li");li.textContent="Sin marcas en el servidor.";$("foto-servidor-lista").append(li);}
    $("foto-confirmar-version").disabled=soloLectura();
  }
  async function leerItems(cargaId) {
    const controller=new AbortController(),timer=setTimeout(()=>controller.abort(),15000);
    try{
      const response=await fetch(`/api/cargas/${cargaId}/fotos/items`,{cache:"no-store",signal:controller.signal});
      if(!response.ok)throw new Error("No se pudieron leer los ítems de la planilla: conectate y reabrí la foto.");
      const rows=await response.json();
      return Array.isArray(rows)?rows.filter(row=>typeof row.bloque==="string"&&typeof row.campo==="string"&&typeof row.texto==="string"):[];
    }finally{clearTimeout(timer);}
  }
  async function abrirEditor(id,localId) {
    const token=++editorToken,selected=contexto;
    try {
      await escritura;
      let foto=await almacen("imagenes","readonly","get",id)||await storage("readonly","get",id),aviso="";
      if(selected?.serverId&&navigator.onLine){
        try{
          await leerMarcasServidor(selected.serverId,id,localId);
          if(!foto?.blob){
            const response=await fetch(`/api/cargas/${selected.serverId}/fotos/${id}/imagen`,{cache:"no-store"});
            if(!response.ok){if(response.status===401)window.readyproofExpired();throw new Error("No se pudo leer la foto del servidor: revisá tu sesión y volvé a intentar.");}
            foto={...(remote.get(selected.serverId)||[]).find(row=>row.id===id),id,localId,blob:await response.blob()};
            if(locked) return;
            await almacen("imagenes","readwrite","put",foto);
          }
        }catch(error){if(error.estado===401||error.estado===403||error.estado===404)throw error;aviso="No se pudo actualizar el servidor. Conservamos la copia local. ";}
      }
      if(!foto?.blob)throw new Error("La foto no está disponible sin conexión en este dispositivo: conectate para leerla del servidor.");
      let items=[];
      if(selected?.serverId&&navigator.onLine){try{items=await leerItems(selected.serverId);}catch(error){aviso+=error.message+" ";}}
      const saved=await almacen("anotaciones","readonly","get",id);
      if(locked||token!==editorToken||contexto?.localId!==localId)return;
      if(editorURL)URL.revokeObjectURL(editorURL);
      editorURL=URL.createObjectURL(foto.blob);
      editor={id,localId,serverId:selected.serverId,orden:foto.orden,items,marcas:(saved?.borradorMarcas??saved?.marcas??[]).map(m=>({...m})),revision:0,versionServidor:saved?.versionServidor,versionActual:saved?.versionActual,servidorMarcas:saved?.servidorMarcas||[],conflicto:saved?.conflicto};
      $("foto-editor-imagen").src=editorURL;$("foto-editor").hidden=false;pintarEditor();mostrarVersionServidor();
      mensajeEditor(soloLectura()?"Solo lectura: la planilla no permite editar las marcas.":aviso+(editor.conflicto?"Las marcas cambiaron en el servidor. Compará las versiones antes de guardar.":"Tocá la foto para agregar una marca. Presioná Guardar marcas para enviarlas al servidor."));
    } catch(error){status(error.message);}
  }
  async function guardarMarcas() {
    if(!editor||soloLectura())return;const active=editor,revision=active.revision;
    try{
      if(active.conflicto)throw new Error("Compará las marcas actuales del servidor y confirmá la versión antes de guardar.");
      const marcas=validarMarcas(active.marcas);
      await escribirAnotaciones({id:active.id,localId:active.localId,serverId:active.serverId,marcas,borradorMarcas:null,pendienteServidor:true,versionServidor:active.versionServidor,conflicto:false,envioId:crypto.randomUUID(),revisionEditor:revision});
      if(editor===active&&active.revision===revision)mensajeEditor("Marcas guardadas en este dispositivo, pendientes de enviar al servidor.");
      await paint();await sincronizarAnotaciones();
    }catch(error){if(editor===active)mensajeEditor(error.message);}
  }
  async function sincronizarAnotaciones() {
    if(locked||!account||!navigator.onLine)return;
    if(sincronizandoMarcas){repetirSincronizacion=true;return;}
    sincronizandoMarcas=true;
    try{
      await escritura;
      const items=await almacen("anotaciones","readonly","getAll");
      for(const row of items){
        if(locked||!navigator.onLine)break;
        if(!row.pendienteServidor||row.conflicto||row.borradorMarcas!=null)continue;
        const draft=await window.readyproofFotosBorrador?.(row.localId);
        if(!draft?.serverId||draft.pending||draft.conflicto||draft.estado!=="borrador"||await storage("readonly","get",row.id))continue;
        try{
          const headers={"Content-Type":"application/json"};if(row.versionServidor)headers["If-Match"]=row.versionServidor;
          const result=await apiMarcas(draft.serverId,row.id,{method:"POST",headers,body:JSON.stringify({anotaciones:validarMarcas(row.marcas)})});
          await escribirAnotaciones({id:row.id},previous=>previous?.envioId===row.envioId?{marcas:result.marcas,pendienteServidor:false,versionServidor:result.version,versionActual:result.version,servidorMarcas:result.marcas}:{versionServidor:result.version,versionActual:result.version,servidorMarcas:result.marcas});
          if(editor?.id===row.id){editor.versionServidor=result.version;editor.versionActual=result.version;editor.servidorMarcas=result.marcas;if(editor.revision===row.revisionEditor)mensajeEditor("Marcas guardadas en el servidor. Todavía no se incluyen en el PDF.");}
        }catch(error){
          if(error.estado===409){
            const latest=await apiMarcas(draft.serverId,row.id);
            await escribirAnotaciones({id:row.id,conflicto:true,servidorMarcas:latest.marcas,versionActual:latest.version});
            if(editor?.id===row.id){editor.conflicto=true;editor.servidorMarcas=latest.marcas;editor.versionActual=latest.version;mostrarVersionServidor();}
          }
          if(editor?.id===row.id)mensajeEditor(error.message);else status(error.message);
        }
      }
    }finally{
      sincronizandoMarcas=false;await paint();
      if(repetirSincronizacion){repetirSincronizacion=false;await sincronizarAnotaciones();}
    }
  }
  $("foto-confirmar-version").onclick=async()=>{
    if(!editor||soloLectura())return;const active=editor;
    try{
      await escribirAnotaciones({id:active.id,versionServidor:active.versionActual,pendienteServidor:false,conflicto:false,borradorMarcas:numerarMarcas(active.marcas)});
      if(editor!==active)return;active.versionServidor=active.versionActual;active.conflicto=false;mostrarVersionServidor();
      mensajeEditor("Versión del servidor revisada. Completá tus marcas y presioná Guardar marcas para reemplazar el conjunto.");await paint();
    }catch(error){mensajeEditor(error.message);}
  };
  async function guardarFotoLocal(row) {
    const db=await database;
    await new Promise((resolve,reject)=>{
      const tx=db.transaction(["pendientes","imagenes"],"readwrite");
      tx.objectStore("pendientes").put(row);tx.objectStore("imagenes").put(row);
      tx.oncomplete=resolve;tx.onerror=()=>reject(tx.error);tx.onabort=()=>reject(tx.error);
    });
  }
  $("foto-lienzo").onclick=event=>{
    if(event.target.closest("button")||soloLectura())return;
    const image=$("foto-editor-imagen"),rect=image.getBoundingClientRect();
    if(!image.naturalWidth||!rect.width||!rect.height)return;
    const x=(event.clientX-rect.left)/rect.width,y=(event.clientY-rect.top)/rect.height;
    if(x>=0&&x<=1&&y>=0&&y<=1)agregarMarca(x,y);
  };
  $("foto-agregar-marca").onclick=()=>agregarMarca(0.5,0.5);
  $("foto-guardar-marcas").onclick=guardarMarcas;
  $("foto-cerrar-editor").onclick=cerrarEditor;

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
    const marcasLocales=await almacen("anotaciones","readonly","getAll");
    if(locked||selected!==contexto)return;
    const count=pending.length+(converting===selected?.localId?1:0)+marcasLocales.filter(row=>row.localId===selected?.localId&&(row.pendienteServidor||row.borradorMarcas!=null)).length;
    $("agregar-foto").disabled=!selected||selected.readOnly||Boolean(converting)||saved.length+pending.length>=20;
    $("foto-archivo").disabled=$("agregar-foto").disabled;
    $("fotos-lista").replaceChildren();
    for(const [rows,pendingPhoto] of [[saved,false],[pending,true]])for(const row of rows){
      const li=document.createElement("li"),label=document.createElement("span"),button=document.createElement("button");
      label.textContent=pendingPhoto?`Foto pendiente de subir · ${row.ancho} × ${row.alto} px`:`Foto ${row.orden} · Guardada · ${row.ancho} × ${row.alto} px`;
      button.type="button";button.className="button secondary small";button.textContent="Ver y marcar";button.onclick=()=>abrirEditor(row.id,selected.localId);
      li.append(label,button);$("fotos-lista").append(li);
    }
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
        await almacen("imagenes","readwrite","put",{...row,orden:result.orden});
        await storage("readwrite","delete",row.id);
        const saved=remote.get(draft.serverId)||[];
        remote.set(draft.serverId,[...saved.filter(item=>item.id!==result.id),result].sort((a,b)=>a.orden-b.orden));
        if(editor?.id===row.id){editor.orden=result.orden;$("foto-editor-titulo").textContent=`Marcas de la foto ${result.orden}`;}
        status("Foto guardada en la planilla.");
      }
    } catch(error){status(error.message||"Sin conexión. La foto queda guardada en este dispositivo para reintentar.");}
    finally {working=false;await paint();}
    await sincronizarAnotaciones();
  }
  async function refresh() {
    if(!account||locked)return;
    const selected=contexto;
    if(selected?.serverId&&navigator.onLine&&remoteKey!==selected.serverId){
      try{
        const fotos=await api(`/api/cargas/${selected.serverId}/fotos`);remote.set(selected.serverId,fotos);
        for(const foto of fotos){if(locked)break;await leerMarcasServidor(selected.serverId,foto.id,selected.localId);}
        if(!locked)remoteKey=selected.serverId;
      }
      catch(error){status(error.message);}
    }
    await paint();await flush();
  }
  window.addEventListener("readyproof-fotos-contexto",event=>{
    const previous=contexto;contexto=event.detail;
    if(editor&&editor.localId!==contexto?.localId)cerrarEditor();
    else if(editor&&previous?.readOnly!==contexto?.readOnly)pintarEditor();
    if(account&&!locked)refresh().catch(error=>status(error.message));
  });
  window.addEventListener("online",()=>{remoteKey=null;refresh().catch(error=>status(error.message));});
  window.addEventListener("readyproof-lock",()=>{
    if(locked)return;
    cerrarEditor();locked=true;contexto=null;$("agregar-foto").disabled=true;$("foto-archivo").value="";$("fotos-lista").replaceChildren();$("fotos-estado").textContent="";
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
      await guardarFotoLocal({id,localId:selected.localId,blob:ready.blob,ancho:ready.ancho,alto:ready.alto,creado:new Date().toISOString()});
      status("Foto guardada en este dispositivo. Se subirá al conectar y sincronizar el borrador.");
    } catch(error){status(error.message||"No se pudo guardar la foto. Volvé a intentar y no cierres esta pantalla.");}
    finally{converting=null;event.target.value="";await paint();await flush();}
  };
  (async()=>{
    try{
      account=await window.readyproofSession;
      if(locked)return;
      database=new Promise((resolve,reject)=>{
        const req=indexedDB.open("readyproof-fotos-"+account.usuario.id,2);
        req.onupgradeneeded=()=>{
          for(const store of ["pendientes","imagenes","anotaciones"])
            if(!req.result.objectStoreNames.contains(store))req.result.createObjectStore(store,{keyPath:"id"});
        };
        req.onsuccess=()=>resolve(req.result);req.onerror=()=>reject(new Error("No se pudo guardar la foto en el dispositivo: revisá el espacio disponible."));
      });
      await database;await refresh();
    } catch(error){status(error.message);}
  })();
})();
