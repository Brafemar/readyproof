"use strict";
(async () => {
  let account;try{account=await window.readyproofSession;}catch{return;}
  const databaseName="readyproof-local-"+account.usuario.id;
  const $ = id => document.getElementById(id);
  const roles = ["tecnico", "responsable"];
  const labels = {fecha:"Fecha",cliente:"Cliente",cuit:"CUIT",telefono:"Teléfono",direccion:"Dirección",edificio:"Edificio",sector:"Sector",empresa_mantenedora:"Empresa mantenedora",numero_mantenedor:"N.° mantenedor certificado",inspector:"Inspector",sistema_designacion:"Sistema / designación"};
  let catalog = null, draft = null, schema = null, syncPromise = null, timer = null;
  let operation = false, previewVersion = -1, previewUrl = null, serviceAvailable = navigator.onLine;
  const controls = [], drawVersion = {tecnico:0,responsable:0};
  const database = new Promise((resolve, reject) => {
    const request = indexedDB.open(databaseName, 1);
    request.onupgradeneeded = () => {
      request.result.createObjectStore("borradores", {keyPath:"localId"});
      request.result.createObjectStore("meta");
    };
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(new Error("No se pudo abrir el almacenamiento del dispositivo."));
  });
  window.addEventListener("readyproof-lock",()=>{database.then(db=>db.close());if(previewUrl)URL.revokeObjectURL(previewUrl);draft=null;document.getElementById("formulario").replaceChildren();document.getElementById("pdf-frame").removeAttribute("src");if(document.getElementById("preview-dialog").open)document.getElementById("preview-dialog").close();});
  async function storage(store, mode, method, ...args) {
    const db = await database;
    return new Promise((resolve, reject) => {
      const tx = db.transaction(store, mode), request = tx.objectStore(store)[method](...args);
      tx.oncomplete = () => resolve(request.result);
      tx.onerror = () => reject(tx.error || new Error("No se pudo guardar en el dispositivo."));
      tx.onabort = () => reject(tx.error || new Error("Se interrumpió el guardado local."));
    });
  }
  function message(text, conflict=false) {
    const element = $("mensaje"); element.replaceChildren(); element.hidden = !text;
    if (text) element.append(document.createTextNode(text));
    if (conflict) {
      const button = document.createElement("button"); button.type="button"; button.className="button secondary";
      button.textContent="Conservar cambios en un borrador nuevo";
      button.onclick=async()=>{const copy=structuredClone(draft); await newDraft(copy); message("Se conservó la copia local en un borrador nuevo.");};
      element.append(button);
    }
  }
  function status(text) { $("save-status").textContent=text; }
  function isReadOnly() { return draft && draft.estado !== "borrador"; }
  function hasSignature(role) { return Boolean(draft?.firmas?.[role] || draft?.firmasServidor?.[role]) && draft?.firmas?.[role] !== null; }
  function update() {
    const online=navigator.onLine && serviceAvailable;
    $("connection-text").textContent=online ? "Conectado" : "Sin conexión";
    document.querySelector(".connection").classList.toggle("offline", !online);
    if (!draft) return;
    const completed=controls.filter(({input})=>input.value.trim()).length + roles.filter(hasSignature).length;
    const total=controls.length + roles.length;
    $("progress").value=Math.round(completed/total*100);
    $("progress-label").textContent=`${completed} de ${total} campos completados`;
    $("estado-carga").textContent={borrador:"Borrador",finalizada:"Finalizada",emitida:"Emitida"}[draft.estado];
    $("action-label").textContent=draft.pending ? "Cambios guardados en el dispositivo" : "Cambios sincronizados";
    controls.forEach(({input})=>{input.disabled=isReadOnly();});
    document.querySelectorAll("[data-clear]").forEach(button=>{button.disabled=isReadOnly();});
    $("completar-ejemplo").disabled=isReadOnly()||operation;
    $("guardar").disabled=isReadOnly()||operation;
    $("vista-previa").disabled=operation||!navigator.onLine;
    $("finalizar").disabled=operation||draft.estado==="emitida"||!navigator.onLine||draft.conflicto||previewVersion!==draft.editVersion||!roles.every(hasSignature);
    $("finalizar").textContent=draft.estado==="finalizada" ? "Reintentar emisión →" : "Finalizar ejemplo →";
    $("finalizar").hidden=draft.estado==="emitida";
    $("descargar").hidden=draft.estado!=="emitida";
    if(draft.serverId) $("descargar").href=`/api/cargas/${draft.serverId}/pdf`;
    for(const role of roles) $("firma-"+role+"-status").textContent=hasSignature(role) ? (draft.firmas?.[role] ? "Firma de prueba guardada" : "Firma guardada en esta planilla") : "Sin firma";
  }
  async function json(url, options={}) {
    const response=await fetch(url,{...options,headers:{"Content-Type":"application/json","X-CSRF-Token":account.csrf_token,...options.headers}});
    let data; try { data=await response.json(); } catch { data={error:"El servicio no devolvió una respuesta válida."}; }
    if(!response.ok){if(response.status===401)window.readyproofExpired();const error=new Error(data.error||"No se pudo completar la operación.");error.status=response.status;throw error;}
    serviceAvailable=true;return data;
  }
  async function draftList() {
    const records=(await storage("borradores","readonly","getAll")).filter(row=>catalog.clientes.some(c=>c.id===row.clienteId));
    records.sort((a,b)=>b.actualizado.localeCompare(a.actualizado));
    const select=$("borradores");select.replaceChildren();
    if(!records.length)select.add(new Option("Sin borradores", ""));
    for(const record of records){
      const name=catalog.clientes.find(c=>c.id===record.clienteId)?.nombre||"[Ejemplo] Carga local";
      select.add(new Option(`${name} · ${new Date(record.actualizado).toLocaleTimeString("es-AR",{hour:"2-digit",minute:"2-digit"})} · ${record.pending?"local":record.estado}`,record.localId));
    }
    if(draft)select.value=draft.localId;
    return records;
  }
  async function persist(target=draft) {
    if(!target)return;
    await storage("borradores","readwrite","put",structuredClone(target));
    await draftList();
  }
  function collect() {
    const result={cabecera:{},bloques:{},observaciones:[]};
    for(const {input,path,definition} of controls){
      const value=input.value.trim();
      if(!value)continue;
      let typed=value;
      if(["numero","entero"].includes(definition.tipo)) typed=Number.isFinite(Number(value))?Number(value):value;
      if(path[0]==="cabecera")result.cabecera[path[1]]=typed;
      else if(path[0]==="bloques"){
        result.bloques[path[1]]??={};result.bloques[path[1]][path[2]]=typed;
      } else result.observaciones[path[1]]=value;
    }
    for(let i=0;i<result.observaciones.length;i++)result.observaciones[i]??="";
    return result;
  }
  function validFields(show=false) {
    let first=null;
    for(const {input,path,definition} of controls){
      input.setCustomValidity("");
      if(input.value && definition.tipo==="texto" && !input.value.startsWith("[Ejemplo] ") && !(path[1]==="empresa_mantenedora"&&input.value==="readyproof")) input.setCustomValidity("Usá un texto ficticio que comience con [Ejemplo].");
      if(!input.checkValidity())first??=input;
    }
    if(first && show){first.scrollIntoView({block:"center"});first.reportValidity();}
    return !first;
  }
  async function changed() {
    if(!draft||isReadOnly())return;
    draft.datos=collect();draft.pending=true;draft.actualizado=new Date().toISOString();draft.editVersion++;
    previewVersion=-1;update();
    try{await persist();status(navigator.onLine?"Guardado en este dispositivo. Sincronizando…":"Guardado en este dispositivo · Sin conexión");}
    catch(error){message(error.message+" No cierres esta pantalla hasta recuperar el guardado.");return;}
    clearTimeout(timer);timer=setTimeout(()=>sync(false),750);
  }
  async function sync(show=false) {
    if(!draft)return false;
    if(syncPromise){await syncPromise;if(draft.pending&&!draft.conflicto)return sync(show);return !draft.pending;}
    if(!navigator.onLine){status("Guardado en este dispositivo · Sin conexión");return false;}
    if(draft.conflicto){if(show)message("La versión del servidor cambió. Se conserva tu copia local.",true);return false;}
    if(draft.estado!=="borrador")return true;
    if(!validFields(show)){status("Guardado local · Revisá los campos antes de sincronizar");return false;}
    const target=draft;
    if(!target.pending&&target.serverId)return true;
    const snapshot=structuredClone(target);
    syncPromise=(async()=>{
      try{
        let result;
        if(!snapshot.serverId){
          result=await json("/api/cargas",{method:"POST",headers:{"Idempotency-Key":snapshot.localId},body:JSON.stringify({sistema_id:snapshot.sistemaId,planilla_id:snapshot.planillaId,datos:snapshot.datos,firmas:snapshot.firmas})});
          if(JSON.stringify(result.datos)!==JSON.stringify(snapshot.datos)){
            target.serverId=result.id;target.revision=result.revision;target.conflicto=true;
            throw Object.assign(new Error("El borrador ya tiene otra versión en el servidor. Tu copia local se conserva."),{status:409});
          }
        }else{
          result=await json(`/api/cargas/${snapshot.serverId}/borrador`,{method:"PUT",body:JSON.stringify({revision:snapshot.revision,datos:snapshot.datos,firmas:snapshot.firmas})});
        }
        target.serverId=result.id;target.revision=result.revision;target.estado=result.estado;target.firmasServidor=result.firmas;
        target.pending=target.editVersion!==snapshot.editVersion;
        await persist(target);
        if(draft===target){status(target.pending?"Guardado local · Hay cambios nuevos por sincronizar":"Guardado en el dispositivo y en el servidor");message("");}
        return !target.pending;
      }catch(error){
        if(error.status===409)target.conflicto=true;
        if(!error.status)serviceAvailable=false;
        await persist(target).catch(()=>{});
        if(draft===target){status("Guardado local · Pendiente de sincronizar");if(show||error.status===409)message(error.message,error.status===409);}
        return false;
      }finally{update();}
    })();
    const result=await syncPromise;syncPromise=null;
    if(target.pending&&!target.conflicto&&target.editVersion!==snapshot.editVersion&&navigator.onLine)timer=setTimeout(()=>sync(false),800);
    return result;
  }
  function inputField(label,definition,path,value){
    const box=document.createElement("div");box.className="field";
    const id="campo-"+controls.length,caption=document.createElement("label");caption.htmlFor=id;caption.textContent=label;
    let input;
    if(definition.tipo==="opcion"){
      input=document.createElement("select");input.add(new Option("Seleccionar…",""));
      for(const option of definition.opciones)input.add(new Option(option,option));
    }else if(path[0]==="observaciones")input=document.createElement("textarea");
    else{input=document.createElement("input");input.type=definition.tipo==="fecha"?"date":["numero","entero"].includes(definition.tipo)?"number":"text";}
    input.id=id;input.name=JSON.stringify(path);input.dataset.path=JSON.stringify(path);
    if(["numero","entero"].includes(definition.tipo)){input.step=definition.tipo==="entero"?"1":"any";input.inputMode=definition.tipo==="entero"?"numeric":"decimal";}
    if(definition.tipo==="texto"){input.maxLength=500;input.placeholder="[Ejemplo] Completá este campo";}
    input.value=value??"";input.addEventListener("input",()=>{input.setCustomValidity("");changed();});
    box.append(caption,input);
    if(definition.unidad){const unit=document.createElement("small");unit.textContent="Unidad: "+definition.unidad;box.append(unit);}
    controls.push({input,path,definition});return box;
  }
  function render(){
    controls.length=0;schema=catalog.definiciones[draft.planillaId].definicion;
    $("cabecera-campos").replaceChildren();$("bloques").replaceChildren();$("observaciones-campos").replaceChildren();
    for(const [key,definition] of Object.entries(schema.cabecera))$("cabecera-campos").append(inputField(labels[key]||key,definition,["cabecera",key],draft.datos.cabecera?.[key]));
    for(const [title,fields] of Object.entries(schema.bloques)){
      const card=document.createElement("section");card.className="card";
      const heading=document.createElement("div");heading.className="card-heading";
      const number=document.createElement("span");number.className="step";number.textContent="02";
      const caption=document.createElement("h2");caption.textContent=title;heading.append(number,caption);
      const grid=document.createElement("div");grid.className="field-grid";
      for(const [label,definition] of Object.entries(fields))grid.append(inputField(label,definition,["bloques",title,label],draft.datos.bloques?.[title]?.[label]));
      card.append(heading,grid);$("bloques").append(card);
    }
    for(let i=0;i<4;i++)$("observaciones-campos").append(inputField("Observación "+(i+1),{tipo:"texto"},["observaciones",i],draft.datos.observaciones?.[i]));
    for(const role of roles){
      const canvas=$("firma-"+role),ctx=canvas.getContext("2d");ctx.clearRect(0,0,canvas.width,canvas.height);
      const value=draft.firmas?.[role],version=++drawVersion[role];
      if(value){const image=new Image();image.onload=()=>{if(drawVersion[role]===version)ctx.drawImage(image,0,0,canvas.width,canvas.height);};image.src=value;}
    }
    $("cliente").value=draft.clienteId;populateSystems();$("sistema").value=draft.sistemaId;populatePlanillas();$("planilla").value=draft.planillaId;
    previewVersion=-1;update();
  }
  function populateSystems(){
    const select=$("sistema");select.replaceChildren();
    for(const item of catalog.sistemas[$("cliente").value]||[])select.add(new Option(item.designacion,item.id));
    select.disabled=!select.options.length;
  }
  function populatePlanillas(){
    const selected=(catalog.sistemas[$("cliente").value]||[]).find(item=>item.id===$("sistema").value);
    const select=$("planilla");select.replaceChildren();
    for(const item of catalog.planillas.filter(item=>item.sistema_tipo===selected?.tipo))select.add(new Option(`${item.codigo} · ${item.version}`,item.id));
    select.disabled=!select.options.length;
  }
  async function newDraft(copy=null){
    clearTimeout(timer);if(syncPromise)await syncPromise;if(draft)await persist();
    const clienteId=$("cliente").value,sistemaId=$("sistema").value,planillaId=$("planilla").value;
    if(!sistemaId||!planillaId)return;
    const cliente=catalog.clientes.find(c=>c.id===clienteId),sistema=catalog.sistemas[clienteId].find(s=>s.id===sistemaId);
    draft={localId:crypto.randomUUID(),clienteId,sistemaId,planillaId,serverId:null,revision:null,estado:"borrador",datos:copy?structuredClone(copy.datos):{cabecera:{cliente:cliente.nombre,sistema_designacion:sistema.designacion,empresa_mantenedora:"readyproof"},bloques:{},observaciones:[]},firmas:copy?structuredClone(copy.firmas):{},firmasServidor:{},pending:true,conflicto:false,editVersion:0,actualizado:new Date().toISOString()};
    render();await persist();status("Borrador guardado en este dispositivo");sync(false);
  }
  async function preview(){
    message("");if(!validFields(true))return;
    clearTimeout(timer);await persist();if(!await sync(true)){if(!navigator.onLine)message("La vista previa requiere conexión. El borrador está guardado en este dispositivo.");return;}
    const version=draft.editVersion;operation=true;update();const dialog=$("preview-dialog");dialog.showModal();$("preview-status").textContent="Preparando PDF con los datos y firmas guardados…";$("pdf-frame").removeAttribute("src");$("abrir-pdf").hidden=true;
    try{
      const response=await fetch(`/api/cargas/${draft.serverId}/vista-previa`,{method:"POST",headers:{"Content-Type":"application/json","X-CSRF-Token":account.csrf_token},body:JSON.stringify({revision:draft.revision})});
      if(!response.ok){const data=await response.json();throw new Error(data.error||"No se pudo generar la vista previa.");}
      if(previewUrl)URL.revokeObjectURL(previewUrl);previewUrl=URL.createObjectURL(await response.blob());
      $("pdf-frame").src=previewUrl;$("abrir-pdf").href=previewUrl;$("abrir-pdf").hidden=false;
      previewVersion=draft.editVersion===version?version:-1;
      $("preview-status").textContent=previewVersion===version?"Vista previa lista. Revisá el documento antes de finalizar.":"El borrador cambió. Generá otra vista previa antes de finalizar.";
    }catch(error){$("preview-status").textContent=error.message;}
    finally{operation=false;update();}
  }
  async function finalize(){
    if(operation||!draft||!roles.every(hasSignature)||previewVersion!==draft.editVersion)return;
    if(!validFields(true)||!await sync(true))return;
    operation=true;update();message("");
    try{
      if(draft.estado==="borrador"){
        const result=await json(`/api/cargas/${draft.serverId}/finalizar`,{method:"POST",body:JSON.stringify({revision:draft.revision})});
        draft.estado=result.estado;draft.revision=result.revision;draft.pending=false;await persist();
      }
      const result=await json(`/api/cargas/${draft.serverId}/emitir`,{method:"POST",body:JSON.stringify({revision:draft.revision})});
      draft.estado=result.estado;draft.revision=result.revision;draft.pending=false;await persist();status("PDF de ejemplo emitido y disponible para descargar");
    }catch(error){message(error.message);await persist().catch(()=>{});}
    finally{operation=false;update();}
  }
  for(const role of roles){
    const canvas=$("firma-"+role),ctx=canvas.getContext("2d");let active=null,last=null,moved=false;
    function point(event){const rect=canvas.getBoundingClientRect();return [(event.clientX-rect.left)*canvas.width/rect.width,(event.clientY-rect.top)*canvas.height/rect.height];}
    canvas.addEventListener("pointerdown",event=>{if(isReadOnly()||!draft)return;event.preventDefault();active=event.pointerId;last=point(event);moved=false;drawVersion[role]++;canvas.setPointerCapture(active);});
    canvas.addEventListener("pointermove",event=>{if(active!==event.pointerId)return;event.preventDefault();const next=point(event);ctx.strokeStyle="#172a2f";ctx.lineWidth=4;ctx.lineCap="round";ctx.lineJoin="round";ctx.beginPath();ctx.moveTo(...last);ctx.lineTo(...next);ctx.stroke();last=next;moved=true;});
    const finish=event=>{if(active!==event.pointerId)return;active=null;if(moved){draft.firmas[role]=canvas.toDataURL("image/png");changed();}};
    canvas.addEventListener("pointerup",finish);canvas.addEventListener("pointercancel",finish);
  }
  document.querySelectorAll("[data-clear]").forEach(button=>button.onclick=()=>{const role=button.dataset.clear;drawVersion[role]++;const canvas=$("firma-"+role);canvas.getContext("2d").clearRect(0,0,canvas.width,canvas.height);draft.firmas[role]=null;changed();});
  $("formulario").addEventListener("submit",event=>event.preventDefault());
  $("guardar").onclick=async()=>{message("");await persist();await sync(true);update();};
  $("vista-previa").onclick=preview;$("finalizar").onclick=finalize;
  $("cerrar-preview").onclick=()=>$("preview-dialog").close();
  $("nuevo").onclick=()=>newDraft();
  $("cliente").onchange=()=>{populateSystems();populatePlanillas();newDraft();};
  $("sistema").onchange=()=>{populatePlanillas();newDraft();};
  $("planilla").onchange=()=>newDraft();
  $("borradores").onchange=async()=>{const selectedId=$("borradores").value;clearTimeout(timer);if(syncPromise)await syncPromise;if(draft)await persist();const selected=await storage("borradores","readonly","get",selectedId);if(selected){draft=selected;render();status(draft.pending?"Borrador local recuperado":"Borrador recuperado");message("");}};
  $("completar-ejemplo").onclick=async()=>{draft.datos=structuredClone(catalog.ejemplo);draft.datos.cabecera.cliente=catalog.clientes.find(c=>c.id===draft.clienteId).nombre;render();await changed();};
  window.addEventListener("offline",()=>{serviceAvailable=false;update();if(draft)status("Guardado en este dispositivo · Sin conexión");});
  window.addEventListener("online",()=>{serviceAvailable=true;update();sync(false);});
  async function boot(){
    try{
      const cached=await storage("meta","readonly","get","catalogo");
      try{
        const [clientes,planillas,ejemplo]=await Promise.all([json("/api/clientes"),json("/api/planillas"),json("/api/ejemplo/saa1")]);
        const sistemas={},definiciones={};
        await Promise.all(clientes.map(async cliente=>{sistemas[cliente.id]=await json(`/api/clientes/${cliente.id}/sistemas`);}));
        await Promise.all(planillas.map(async planilla=>{definiciones[planilla.id]=await json(`/api/planillas/${planilla.id}`);}));
        catalog={clientes,planillas,ejemplo,sistemas,definiciones};await storage("meta","readwrite","put",catalog,"catalogo");
      }catch(error){serviceAvailable=false;if(!cached)throw new Error("No se pudo cargar el catálogo. Conectate al servicio local para iniciar la primera carga.");catalog=cached;}
      $("cliente").replaceChildren();for(const cliente of catalog.clientes)$("cliente").add(new Option(cliente.nombre,cliente.id));$("cliente").disabled=false;
      populateSystems();populatePlanillas();
      const records=await draftList();
      if(!catalog.clientes.length){message("No tenés clientes asignados. Pedí la asignación al administrador.");return;}
      if(records.length){draft=records[0];render();status("Borrador recuperado del dispositivo");}
      else await newDraft();
      if("serviceWorker" in navigator)navigator.serviceWorker.register("/sw.js").catch(()=>{message("No se pudo preparar la reapertura sin conexión. Conservá esta pantalla abierta; el borrador se guarda en el dispositivo.");});
      update();if(draft?.pending)sync(false);
    }catch(error){message(error.message);status("No se pudo preparar el guardado local");}
  }
  boot();
})();
