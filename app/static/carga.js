"use strict";
(async () => {
  const piloto=document.body.dataset.modoPiloto!=='false';
  const empresa=document.body.dataset.empresaMantenedora||'readyproof', certificado=document.body.dataset.certificado||'';
  let account;try{account=await window.readyproofSession;}catch{return;}
  const databaseName="readyproof-local-"+account.usuario.id;
  const $ = id => document.getElementById(id);
  const roles = ["tecnico", "responsable"];
  const responsableInputs={nombre_firmante:"responsable-nombre",dni_firmante:"responsable-dni",cargo_firmante:"responsable-cargo"};
  function responsableActual(){return Object.fromEntries(Object.entries(responsableInputs).map(([key,id])=>[key,key==="dni_firmante"?$(id).value:$(id).value.trim()]));}
  function validarFirmantes(show=false){
    let first=null;
    for(const [key,id] of Object.entries(responsableInputs)){
      const input=$(id);input.setCustomValidity("");
      if(key==="nombre_firmante"&&!input.value.trim())input.setCustomValidity("El nombre del responsable es obligatorio.");
      if(piloto && key!=="dni_firmante" && input.value.trim() && !input.value.trim().startsWith("[Ejemplo] "))input.setCustomValidity("Usá datos ficticios que comiencen con [Ejemplo].");
      if(!input.checkValidity())first??=input;
    }
    if(show&&first){first.scrollIntoView({block:"center"});first.reportValidity();}
    return !first&&roles.every(hasSignature);
  }
  const labels = {fecha:"Fecha",cliente:"Cliente",cuit:"CUIT",telefono:"Teléfono",direccion:"Dirección",edificio:"Edificio",sector:"Sector",empresa_mantenedora:"Empresa mantenedora",numero_mantenedor:"N.° mantenedor certificado",inspector:"Inspector",sistema_designacion:"Sistema / designación"};
  let catalog = null, draft = null, schema = null, syncPromise = null, timer = null;
  let operation = false, previewVersion = -1, previewUrl = null, serviceAvailable = navigator.onLine;
  const controls = [], drawVersion = {tecnico:0,responsable:0};
  const firmasActivas = new Set();
  window.readyproofActualizacionCarga = async () => {
    if (operation || syncPromise || firmasActivas.size) return "Esperá a que termine la operación o la firma antes de actualizar.";
    if (!draft) return "";
    if (draft.pending || draft.conflicto) return "Guardá y sincronizá el borrador; resolvé cualquier conflicto antes de actualizar.";
    const selected = draft;
    const saved = await storage("borradores", "readonly", "get", selected.localId);
    if (draft !== selected || operation || syncPromise || firmasActivas.size || draft.pending || draft.conflicto || !saved || saved.editVersion !== draft.editVersion || saved.pending !== draft.pending)
      return "Todavía hay cambios por guardar. Esperá a que se sincronicen antes de actualizar.";
    return "";
  };
  const database = new Promise((resolve, reject) => {
    const request = indexedDB.open(databaseName, 1);
    request.onupgradeneeded = () => {
      request.result.createObjectStore("borradores", {keyPath:"localId"});
      request.result.createObjectStore("meta");
    };
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(new Error("No se pudo abrir el almacenamiento del dispositivo."));
  });
  window.addEventListener("readyproof-lock",()=>{database.then(db=>db.close());if(previewUrl)URL.revokeObjectURL(previewUrl);draft=null;document.getElementById("correo-dialog").close();document.getElementById("correo-destinatario").value="";document.getElementById("correo-estado").textContent="";document.getElementById("formulario").replaceChildren();document.getElementById("pdf-frame").removeAttribute("src");if(document.getElementById("preview-dialog").open)document.getElementById("preview-dialog").close();});
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
  function historica() { return draft && !catalog.planillas.some(item=>item.id===draft.planillaId); }
  function permiteCopiaA4() { return historica() && catalog.definiciones[draft.planillaId]?.codigo==="SG-PEM-IFI-SAA-1"; }
  function isReadOnly() { return draft && (draft.estado !== "borrador" || historica()); }
  function hasSignature(role) { return Boolean(draft?.firmas?.[role] || draft?.firmasServidor?.[role]) && draft?.firmas?.[role] !== null; }
  let fotosPendientes=0;
  window.addEventListener("readyproof-fotos-pendientes",event=>{fotosPendientes=event.detail;update();});
  window.readyproofFotosBorrador=localId=>storage("borradores","readonly","get",localId);
  function update() {
    const online=navigator.onLine && serviceAvailable;
    $("connection-text").textContent=online ? "Conectado" : "Sin conexión";
    document.querySelector(".connection").classList.toggle("offline", !online);
    window.dispatchEvent(new CustomEvent("readyproof-fotos-contexto",{detail:draft?{localId:draft.localId,serverId:draft.serverId,readOnly:isReadOnly(),estado:draft.estado,pending:draft.pending,conflicto:draft.conflicto}:null}));
    if (!draft) return;
    const completed=controls.filter(({input})=>input.value.trim()).length + roles.filter(hasSignature).length + Object.values(responsableInputs).filter(id=>$(id).value.trim()).length;
    const total=controls.length + roles.length + Object.keys(responsableInputs).length;
    $("progress").value=Math.round(completed/total*100);
    $("progress-label").textContent=`${completed} de ${total} campos completados`;
    $("estado-carga").textContent={borrador:"Borrador",finalizada:"Finalizada",emitida:"Emitida"}[draft.estado];
    if(draft.numeroRegistro)$("estado-carga").textContent+=` · Registro ${draft.numeroRegistro} · Revisión ${draft.revisionPublica}`;
    $("desbloquear").hidden=!draft.puedeDesbloquear||historica();
    $("desbloquear").disabled=operation||!online||draft.pending||draft.conflicto;
    $("ver-emisiones").hidden=!draft.serverId;
    $("ver-emisiones").disabled=operation||!online;
    $("action-label").textContent=draft.pending ? "Cambios guardados en el dispositivo" : "Cambios sincronizados";
    controls.forEach(({input})=>{input.disabled=isReadOnly();});
    Object.values(responsableInputs).forEach(id=>{$(id).disabled=isReadOnly();});
    document.querySelectorAll("[data-clear]").forEach(button=>{button.disabled=isReadOnly();});
    $("completar-ejemplo").hidden=!piloto;
    $("completar-ejemplo").disabled=isReadOnly()||operation;
    $("guardar").disabled=isReadOnly()||operation;
    $("vista-previa").disabled=operation||!navigator.onLine||historica();
    $("finalizar").disabled=fotosPendientes>0||operation||draft.estado==="emitida"||!navigator.onLine||draft.conflicto||previewVersion!==draft.editVersion||!validarFirmantes();
    $("finalizar").textContent=draft.estado==="finalizada" ? "Reintentar emisión →" : (piloto?"Finalizar ejemplo →":"Finalizar planilla →");
    $("finalizar").hidden=draft.estado==="emitida"||historica();
    $("copiar-a4").hidden=!permiteCopiaA4();
    $("copiar-a4").disabled=operation||!online;
    $("descargar").textContent=historica()?"Descargar PDF anterior":"Descargar PDF";
    $("descargar").hidden=draft.estado!=="emitida";
    $("enviar-pdf").hidden=draft.estado!=="emitida";
    $("enviar-pdf").disabled=operation||!online||historica();
    if(draft.serverId) $("descargar").href=`/api/cargas/${draft.serverId}/pdf`;
    for(const role of roles) $("firma-"+role+"-status").textContent=hasSignature(role) ? (draft.firmas?.[role] ? "Firma de prueba guardada" : "Firma guardada en esta planilla") : "Sin firma";
  }
  async function json(url, options={}) {
    const response=await fetch(url,{...options,headers:{"Content-Type":"application/json","X-CSRF-Token":account.csrf_token,...options.headers}});
    let data; try { data=await response.json(); } catch { data={error:"El servicio no devolvió una respuesta válida."}; }
    if(!response.ok){if(response.status===401)window.readyproofExpired();const error=new Error(data.error||"No se pudo completar la operación.");error.status=response.status;throw error;}
    serviceAvailable=true;return data;
  }
  function metadata(target,result){
    target.numeroRegistro=result.numero_registro;target.revisionPublica=result.revision_publica;
    target.pdfHash=result.pdf_sha256;
    target.puedeDesbloquear=result.puede_desbloquear;
  }
  async function refrescarPermisos(){
    const target=draft;
    if(!target?.serverId||target.pending||!navigator.onLine)return;
    try{
      const result=await json(`/api/cargas/${target.serverId}`);
      if(result.revision!==target.revision){target.puedeDesbloquear=false;target.conflicto=true;if(draft===target)message("La carga cambió en otro dispositivo. Tu copia local se conserva.",true);}
      else metadata(target,result);
      await persist(target);update();
    }catch{target.puedeDesbloquear=false;update();}
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
      if(piloto && input.value && definition.tipo==="texto" && !input.value.startsWith("[Ejemplo] ") && !(path[1]==="empresa_mantenedora"&&input.value==="readyproof")) input.setCustomValidity("Usá un texto ficticio que comience con [Ejemplo].");
      if(!input.checkValidity())first??=input;
    }
    if(first && show){first.scrollIntoView({block:"center"});first.reportValidity();}
    return !first;
  }
  async function changed() {
    if(!draft||isReadOnly())return;
    draft.datos=collect();draft.responsable=responsableActual();draft.pending=true;draft.actualizado=new Date().toISOString();draft.editVersion++;
    previewVersion=-1;update();
    try{await persist();status(navigator.onLine?"Guardado en este dispositivo. Sincronizando…":"Guardado en este dispositivo · Sin conexión");}
    catch(error){message(error.message+" No cierres esta pantalla hasta recuperar el guardado.");return;}
    clearTimeout(timer);timer=setTimeout(()=>sync(false),750);
  }
  async function sync(show=false) {
    if(!draft)return false;
    if(syncPromise){await syncPromise;if(!draft)return false;if(draft.pending&&!draft.conflicto)return sync(show);return !draft.pending;}
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
          result=await json("/api/cargas",{method:"POST",headers:{"Idempotency-Key":snapshot.localId},body:JSON.stringify({sistema_id:snapshot.sistemaId,planilla_id:snapshot.planillaId,datos:snapshot.datos,firmas:snapshot.firmas,responsable:snapshot.responsable||{}})});
          if(JSON.stringify(result.datos)!==JSON.stringify(snapshot.datos)||JSON.stringify(result.responsable)!==JSON.stringify({nombre_firmante:"",dni_firmante:"",cargo_firmante:"",...snapshot.responsable})){
            target.serverId=result.id;target.revision=result.revision;target.conflicto=true;
            throw Object.assign(new Error("El borrador ya tiene otra versión en el servidor. Tu copia local se conserva."),{status:409});
          }
        }else{
          result=await json(`/api/cargas/${snapshot.serverId}/borrador`,{method:"PUT",body:JSON.stringify({revision:snapshot.revision,datos:snapshot.datos,firmas:snapshot.firmas,responsable:snapshot.responsable||{}})});
        }
        target.serverId=result.id;target.revision=result.revision;target.estado=result.estado;target.firmasServidor=result.firmas;target.firmantes=result.firmantes;
        metadata(target,result);
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
    if(draft===target&&target.pending&&!target.conflicto&&target.editVersion!==snapshot.editVersion&&navigator.onLine)timer=setTimeout(()=>sync(false),800);
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
    if(definition.tipo==="texto"){input.maxLength=500;input.placeholder=piloto?"[Ejemplo] Completá este campo":"Completá este campo";}
    input.value=value??"";input.addEventListener("input",()=>{input.setCustomValidity("");changed();});
    box.append(caption,input);
    if(definition.unidad){const unit=document.createElement("small");unit.textContent="Unidad: "+definition.unidad;box.append(unit);}
    controls.push({input,path,definition});return box;
  }
  function render(){
    controls.length=0;schema=catalog.definiciones[draft.planillaId].definicion;
    $("codigo-planilla").textContent=schema.codigo||catalog.definiciones[draft.planillaId].codigo;
    document.querySelector(".page-heading h1").textContent=schema.titulo||"Información general";
    document.querySelector(".page-heading p").textContent=schema.sistema||"Sistema de abastecimiento de agua";
    $("pdf-frame").title="Vista previa PDF de "+$("codigo-planilla").textContent;
    $("cabecera-campos").replaceChildren();$("bloques").replaceChildren();$("observaciones-campos").replaceChildren();
    for(const [key,definition] of Object.entries(schema.cabecera))$("cabecera-campos").append(inputField(labels[key]||key,definition,["cabecera",key],draft.datos.cabecera?.[key]));
    for(const [title,fields] of Object.entries(schema.bloques)){
      const card=document.createElement("section");card.className="card";
      const heading=document.createElement("div");heading.className="card-heading";
      const number=document.createElement("span");number.className="step";number.textContent="02";
      const caption=document.createElement("h2");caption.textContent=title;heading.append(number,caption);
      const grid=document.createElement("div");grid.className="field-grid";
      const table=schema.tablas?.[title];
      const field=(key)=>inputField(fields[key].etiqueta||key,fields[key],["bloques",title,key],draft.datos.bloques?.[title]?.[key]);
      if(table){
        for(const [key,definition] of Object.entries(fields))if(definition.tipo==="fecha")grid.append(field(key));
        const scroll=document.createElement("div");scroll.className="sheet-table-scroll";scroll.tabIndex=0;scroll.setAttribute("role","region");scroll.setAttribute("aria-label",title);
        const element=document.createElement("table");element.className="sheet-table";
        const head=element.createTHead().insertRow();for(const text of [table.columna_etiqueta||"ELEMENTOS",...table.columnas]){const th=document.createElement("th");th.scope="col";th.textContent=text;head.append(th);}
        const body=element.createTBody();
        for(const row of table.filas){const tr=body.insertRow(),th=document.createElement("th");th.scope="row";th.textContent=row.etiqueta;tr.append(th);for(const key of row.campos)tr.insertCell().append(field(key));}
        scroll.append(element);grid.append(scroll);
        const help=document.createElement("p");help.className="matrix-help";help.textContent="✓ cumple · O no cumple · X no apreciable · NA no aplicable. Deslizá la tabla para ver todas las columnas.";grid.append(help);
      }else for(const key of Object.keys(fields))grid.append(field(key));
      card.append(heading,grid);$("bloques").append(card);
    }
    for(let i=0;i<4;i++)$("observaciones-campos").append(inputField("Observación "+(i+1),{tipo:"texto"},["observaciones",i],draft.datos.observaciones?.[i]));
    for(const [key,id] of Object.entries(responsableInputs)){$(id).value=draft.responsable?.[key]||"";}
    const signer=draft.firmantes?.tecnico;
    $("tecnico-identidad").textContent=(signer?.login||account.usuario.login)+" · "+(signer?.nombre||account.usuario.nombre);
    for(const role of roles){
      const canvas=$("firma-"+role),ctx=canvas.getContext("2d");ctx.clearRect(0,0,canvas.width,canvas.height);
      const value=draft.firmas?.[role],version=++drawVersion[role];
      if(value){const image=new Image();image.onload=()=>{if(drawVersion[role]===version)ctx.drawImage(image,0,0,canvas.width,canvas.height);};image.src=value;}
    }
    $("cliente").value=draft.clienteId;populateSystems();$("sistema").value=draft.sistemaId;populatePlanillas();if(catalog.planillas.some(item=>item.id===draft.planillaId))$("planilla").value=draft.planillaId;
    previewVersion=-1;update();
    if(historica())message(permiteCopiaA4()?"Esta carga conserva el formato anterior. Usá Crear copia A4 para revisarla y emitirla en una sola hoja.":"Esta carga conserva su versión anterior. Creá una carga nueva y revisá las unidades; no se copian mediciones entre versiones.");
  }
  function populateSystems(){
    const select=$("sistema");select.replaceChildren();
    for(const item of catalog.sistemas[$("cliente").value]||[])select.add(new Option(item.tipo+" · "+item.designacion,item.id));
    select.disabled=!select.options.length;
  }
  function populatePlanillas(){
    const selected=(catalog.sistemas[$("cliente").value]||[]).find(item=>item.id===$("sistema").value);
    const select=$("planilla");select.replaceChildren();
    for(const item of catalog.planillas.filter(item=>item.sistema_tipo===selected?.tipo))select.add(new Option(`${item.codigo} · ${item.nombre||item.version}`,item.id));
    select.disabled=!select.options.length;
    const count=catalog.clientes.length, systems=$("sistema").options.length, sheets=select.options.length;
    const help=$("seleccion-ayuda");
    if(help){
      help.textContent=!count ? "No hay clientes asignados." : !systems ? "Este cliente no tiene sistemas disponibles." : !sheets ? "Este sistema no tiene planillas de carga habilitadas." : `${count} ${count===1?"cliente disponible":"clientes disponibles"} · ${systems} ${systems===1?"sistema":"sistemas"} · ${sheets} ${sheets===1?"planilla":"planillas"}.`;
      if(account.usuario.rol==="admin")help.textContent+=" Podés administrar clientes y sistemas desde Administración.";
    }
  }
  async function newDraft(copy=null){
    clearTimeout(timer);if(syncPromise)await syncPromise;if(draft)await persist();
    const clienteId=$("cliente").value,sistemaId=$("sistema").value,planillaId=$("planilla").value;
    if(!sistemaId||!planillaId)return;
    const cliente=catalog.clientes.find(c=>c.id===clienteId),sistema=catalog.sistemas[clienteId].find(s=>s.id===sistemaId);
    draft={localId:crypto.randomUUID(),clienteId,sistemaId,planillaId,serverId:null,revision:null,estado:"borrador",datos:copy?structuredClone(copy.datos):{cabecera:{cliente:cliente.nombre,sistema_designacion:sistema.designacion,empresa_mantenedora:empresa,...(piloto?{}:{numero_mantenedor:certificado})},bloques:{},observaciones:[]},firmas:copy?structuredClone(copy.firmas):{},firmasServidor:{},responsable:copy?structuredClone(copy.responsable||{}):{},pending:true,conflicto:false,editVersion:0,actualizado:new Date().toISOString()};
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
    if(operation||!draft||!validarFirmantes(true)||previewVersion!==draft.editVersion)return;
    if(!validFields(true)||!await sync(true))return;
    operation=true;update();message("");
    try{
      if(draft.estado==="borrador"){
        const result=await json(`/api/cargas/${draft.serverId}/finalizar`,{method:"POST",body:JSON.stringify({revision:draft.revision})});
        draft.estado=result.estado;draft.revision=result.revision;draft.pending=false;await persist();
      }
      const result=await json(`/api/cargas/${draft.serverId}/emitir`,{method:"POST",body:JSON.stringify({revision:draft.revision})});
      draft.estado=result.estado;draft.revision=result.revision;draft.pending=false;metadata(draft,result);await persist();status(piloto?"PDF de ejemplo emitido y disponible para descargar":"PDF emitido y disponible para descargar");
    }catch(error){message(error.message);await persist().catch(()=>{});}
    finally{operation=false;update();}
  }
  for(const role of roles){
    const canvas=$("firma-"+role),ctx=canvas.getContext("2d");let active=null,last=null,moved=false;
    function point(event){const rect=canvas.getBoundingClientRect();return [(event.clientX-rect.left)*canvas.width/rect.width,(event.clientY-rect.top)*canvas.height/rect.height];}
    canvas.addEventListener("pointerdown",event=>{if(isReadOnly()||!draft)return;event.preventDefault();active=event.pointerId;firmasActivas.add(role);last=point(event);moved=false;drawVersion[role]++;canvas.setPointerCapture(active);});
    canvas.addEventListener("pointermove",event=>{if(active!==event.pointerId)return;event.preventDefault();const next=point(event);ctx.strokeStyle="#172a2f";ctx.lineWidth=4;ctx.lineCap="round";ctx.lineJoin="round";ctx.beginPath();ctx.moveTo(...last);ctx.lineTo(...next);ctx.stroke();last=next;moved=true;});
    const finish=event=>{if(active!==event.pointerId)return;active=null;firmasActivas.delete(role);if(moved){draft.firmas[role]=canvas.toDataURL("image/png");changed();}};
    canvas.addEventListener("pointerup",finish);canvas.addEventListener("pointercancel",finish);
  }
  document.querySelectorAll("[data-clear]").forEach(button=>button.onclick=()=>{const role=button.dataset.clear;drawVersion[role]++;const canvas=$("firma-"+role);canvas.getContext("2d").clearRect(0,0,canvas.width,canvas.height);draft.firmas[role]=null;changed();});
  $("formulario").addEventListener("submit",event=>event.preventDefault());
  $("guardar").onclick=async()=>{message("");await persist();await sync(true);update();};
  Object.values(responsableInputs).forEach(id=>$(id).addEventListener("input",changed));
  $("vista-previa").onclick=preview;$("finalizar").onclick=finalize;
  $("desbloquear").onclick=()=>{if(operation||draft.pending||draft.conflicto)return;$("motivo-desbloqueo").value="";$("desbloqueo-dialog").showModal();};
  $("cancelar-desbloqueo").onclick=()=>$("desbloqueo-dialog").close();
  $("desbloqueo-form").onsubmit=async event=>{
    event.preventDefault();
    if(operation||!draft?.puedeDesbloquear||draft.pending||draft.conflicto||!$("desbloqueo-form").reportValidity())return;
    const target=draft;operation=true;update();$("confirmar-desbloqueo").disabled=true;
    try{
      const result=await json(`/api/cargas/${target.serverId}/desbloquear`,{method:"POST",body:JSON.stringify({revision:target.revision,motivo:$("motivo-desbloqueo").value})});
      target.estado=result.estado;target.revision=result.revision;target.datos=result.datos;
      target.firmas={};target.firmasServidor=result.firmas;target.firmantes=result.firmantes;target.responsable=result.responsable;
      target.pending=false;metadata(target,result);target.editVersion++;previewVersion=-1;
      await persist(target);$("desbloqueo-dialog").close();render();
      message("El PDF anterior quedó conservado en Emisiones anteriores. Revisá los datos y volvé a firmar antes de emitir.");
    }catch(error){message(error.message,error.status===409);}
    finally{operation=false;$("confirmar-desbloqueo").disabled=false;update();}
  };
  $("ver-emisiones").onclick=async()=>{
    if(operation||!draft?.serverId)return;
    operation=true;update();
    try{
      const rows=await json(`/api/cargas/${draft.serverId}/emisiones`),list=$("emisiones-lista");list.replaceChildren();
      if(!rows.length)list.textContent="No hay revisiones archivadas. Los PDF históricos se conservan al desbloquearlos.";
      for(const row of rows){const item=document.createElement("p"),link=document.createElement("a");link.href=row.url;link.textContent=`${row.numero_registro?"Registro "+row.numero_registro:"Original sin número"} · Revisión ${row.revision_publica} · Descargar PDF`;item.append(link);list.append(item);}
      $("emisiones-dialog").showModal();
    }catch(error){message(error.message);}
    finally{operation=false;update();}
  };
  $("cerrar-emisiones").onclick=()=>$("emisiones-dialog").close();
  $("desbloqueo-dialog").addEventListener("cancel",event=>{if(operation)event.preventDefault();});
  window.addEventListener("readyproof-lock",()=>{
    clearTimeout(timer);
    for(const id of ["desbloqueo-dialog","emisiones-dialog"])if($(id).open)$(id).close();
    $("motivo-desbloqueo").value="";$("emisiones-lista").replaceChildren();
  });
  $("cerrar-preview").onclick=()=>$("preview-dialog").close();
  $("nuevo").onclick=()=>newDraft();
  async function selectedDraft(){
    try{await newDraft();}
    catch(error){message(error.message);status("No se pudo cambiar de planilla. Se conservan los borradores guardados.");}
  }
  $("cliente").onchange=async()=>{populateSystems();populatePlanillas();await selectedDraft();};
  $("sistema").onchange=async()=>{populatePlanillas();await selectedDraft();};
  $("planilla").onchange=selectedDraft;
  $("borradores").onchange=async()=>{const selectedId=$("borradores").value;clearTimeout(timer);if(syncPromise)await syncPromise;if(draft)await persist();const selected=await storage("borradores","readonly","get",selectedId);if(selected){draft=selected;render();status(draft.pending?"Borrador local recuperado":"Borrador recuperado");message("");await refrescarPermisos();}};
  $("completar-ejemplo").onclick=async()=>{draft.responsable={nombre_firmante:"[Ejemplo] Responsable de prueba",dni_firmante:"00000000",cargo_firmante:"[Ejemplo] Encargado"};draft.datos=structuredClone(catalog.definiciones[draft.planillaId].ejemplo||catalog.ejemplo);draft.datos.cabecera.cliente=catalog.clientes.find(c=>c.id===draft.clienteId).nombre;draft.datos.cabecera.sistema_designacion=catalog.sistemas[draft.clienteId].find(s=>s.id===draft.sistemaId).designacion;render();await changed();};
  window.addEventListener("offline",()=>{serviceAvailable=false;update();if(draft)status("Guardado en este dispositivo · Sin conexión");});
  window.addEventListener("online",()=>{serviceAvailable=true;update();sync(false);});
  $("copiar-a4").onclick=async()=>{
    if(operation||!permiteCopiaA4())return;
    const original=structuredClone(draft);operation=true;update();
    try{await newDraft(original);message("Copia A4 creada. Revisá los datos y las dos firmas, generá la vista previa y finalizá.");}
    catch(error){message(error.message);}
    finally{operation=false;update();}
  };
  let correoBusy=false, correoReady=false, correoCarga=null, correoEnvios=[],correoConsulta=0,correoDestinoEditado=false;
  function correoStatus(row){
    if(row.estado==="enviado")return `Correo enviado a ${row.destinatario}. Gmail aceptó el PDF adjunto; verificá la recepción en destino.`;
    return `Existe una solicitud de envío a ${row.destinatario}, sin entrega confirmada. Consultá a Administración antes de repetir.`;
  }
  function correoUpdate(){
    const previous=correoEnvios.find(row=>row.destinatario===$("correo-destinatario").value.trim());
    $("confirmar-envio").disabled=correoBusy||!correoReady||Boolean(previous);
    $("correo-destinatario").disabled=correoBusy;
    $("cerrar-correo").disabled=correoBusy;
    if(previous)$("correo-estado").textContent=correoStatus(previous);
    else if(correoReady&&!correoBusy)$("correo-estado").textContent=piloto?"Confirmá el destinatario y presioná Enviar PDF. Solo destinatarios de prueba habilitados.":"Confirmá el destinatario antes de enviar la planilla emitida.";
  }
  $("enviar-pdf").onclick=async()=>{
    if(operation||!draft||draft.estado!=="emitida")return;
    correoReady=false;correoEnvios=[];correoCarga=draft.serverId;
    const consulta=++correoConsulta,carga=correoCarga,pdfHash=draft.pdfHash;
    correoDestinoEditado=false;$("correo-destinatario").value="";
    $("correo-dialog").showModal();$("correo-estado").textContent="Consultando el servicio de correo…";correoUpdate();
    try{
      const [config,rows]=await Promise.all([json("/api/correo/configuracion"),json(`/api/cargas/${carga}/envios`)]);
      if(consulta!==correoConsulta||!$("correo-dialog").open||draft?.serverId!==carga)return;
      correoEnvios=rows.filter(row=>row.pdf_sha256===pdfHash);correoReady=config.habilitado;
      $("correo-destinatarios").replaceChildren();
      for(const address of config.destinatarios)$("correo-destinatarios").append(new Option(address,address));
      if(!correoDestinoEditado)$("correo-destinatario").value=config.destinatarios[0]||"";
      if(!correoReady)$("correo-estado").textContent="Administración debe habilitar el envío de planillas en este entorno.";
      correoUpdate();
    }catch(error){if(consulta===correoConsulta&&$("correo-dialog").open)$("correo-estado").textContent=error.message;}
  };
  $("cerrar-correo").onclick=()=>{if(!correoBusy){correoConsulta++;$("correo-dialog").close();}};
  $("correo-dialog").addEventListener("cancel",event=>{if(correoBusy)event.preventDefault();else correoConsulta++;});
  $("correo-destinatario").addEventListener("input",()=>{correoDestinoEditado=true;correoUpdate();});
  $("correo-form").onsubmit=async event=>{
    event.preventDefault();
    if(correoBusy||!correoReady||!$("correo-form").reportValidity())return;
    const recipient=$("correo-destinatario").value.trim(), target=draft;
    if(correoEnvios.some(row=>row.destinatario===recipient)||target?.serverId!==correoCarga)return;
    correoBusy=true;operation=true;correoUpdate();update();$("correo-estado").textContent="Enviando el PDF firmado…";
    try{
      const solicitud=target.pdfHash+":"+recipient;
      target.solicitudesCorreo??={};target.solicitudesCorreo[solicitud]??=crypto.randomUUID();
      await persist(target);
      const response=await fetch(`/api/cargas/${correoCarga}/enviar`,{method:"POST",headers:{"Content-Type":"application/json","X-CSRF-Token":account.csrf_token,"Idempotency-Key":target.solicitudesCorreo[solicitud]},body:JSON.stringify({destinatario:recipient,inmediato:true})});
      const result=await response.json();
      if(response.status===401)window.readyproofExpired();
      if(result.id){correoEnvios.unshift(result);$("correo-estado").textContent=correoStatus(result);}
      else throw new Error(result.error||"No se pudo confirmar el envío.");
    }catch(error){$("correo-estado").textContent=error.message+". Si hubo un corte, cerrá y volvé a abrir este cuadro para consultar el resultado.";correoReady=false;}
    finally{correoBusy=false;operation=false;correoUpdate();update();}
  };
  async function boot(){
    try{
      const cached=await storage("meta","readonly","get","catalogo");
      try{
        const [clientes,planillas,ejemplo]=await Promise.all([json("/api/clientes"),json("/api/planillas"),json("/api/ejemplo/saa1")]);
        const sistemas={},definiciones={};
        await Promise.all(clientes.map(async cliente=>{sistemas[cliente.id]=await json(`/api/clientes/${cliente.id}/sistemas`);}));
        await Promise.all(planillas.map(async planilla=>{definiciones[planilla.id]=await json(`/api/planillas/${planilla.id}`);}));
        const anteriores=await storage("borradores","readonly","getAll");
        for(const record of anteriores){
          if(!definiciones[record.planillaId]&&clientes.some(cliente=>cliente.id===record.clienteId))definiciones[record.planillaId]=await json(`/api/planillas/${record.planillaId}`);
        }
        catalog={clientes,planillas,ejemplo,sistemas,definiciones};await storage("meta","readwrite","put",catalog,"catalogo");
      }catch(error){serviceAvailable=false;if(!cached)throw new Error("No se pudo cargar el catálogo. Conectate al servicio local para iniciar la primera carga.");catalog=cached;}
      $("cliente").replaceChildren();for(const cliente of catalog.clientes)$("cliente").add(new Option(cliente.nombre,cliente.id));$("cliente").disabled=false;
      populateSystems();populatePlanillas();
      const records=await draftList();
      if(!catalog.clientes.length){message("No tenés clientes asignados. Pedí la asignación al administrador.");return;}
      if(records.length){draft=records[0];render();status("Borrador recuperado del dispositivo");}
      else await newDraft();
      update();if(draft?.pending)sync(false);
      else await refrescarPermisos();
    }catch(error){message(error.message);status("No se pudo preparar el guardado local");}
  }
  boot();
})();
