"use strict";
(() => {
  const $=id=>document.getElementById(id),csrf=document.querySelector('meta[name="csrf-token"]').content;
  let users=[],clients=[],editing=null,editingClient=null;
  function message(text){$("admin-message").textContent=text;$("admin-message").hidden=false;}
  async function api(url,options={}){const response=await fetch(url,{...options,headers:{"Content-Type":"application/json","X-CSRF-Token":csrf}});const data=await response.json();if(!response.ok){if(response.status===401)location.replace("/login");throw new Error(data.error||"No se pudo completar la operación.");}return data;}
  function reset(){editing=null;$("usuario-form").reset();$("permiso-certificado").hidden=true;$("usuario-login").disabled=false;$("usuario-nombre").disabled=false;$("editor-title").textContent="Crear usuario";$("restablecer-clave").hidden=true;$("usuario-clave").required=true;}
  function edit(user){editing=user.id;$("permiso-certificado").hidden=false;$("usuario-certificado").checked=!!user.certificado_conjunto;$("usuario-login").value=user.login;$("usuario-login").disabled=true;$("usuario-nombre").value=user.nombre;$("usuario-nombre").disabled=true;$("usuario-rol").value=user.rol;$("usuario-activo").checked=user.activo;$("usuario-clave").value="";$("usuario-clave").required=false;$("restablecer-clave").hidden=false;$("editor-title").textContent="Editar cuenta: "+user.login;for(const input of $("cliente-checks").querySelectorAll("input"))input.checked=user.cliente_ids.includes(input.value);$("usuario-form").scrollIntoView({behavior:"smooth"});}
  function cell(row,text){const td=document.createElement("td");td.textContent=text;row.append(td);return td;}
  async function refresh(){
    [users,clients]=await Promise.all([api("/api/admin/usuarios"),api("/api/admin/clientes")]);
    $("usuarios").replaceChildren();$("cliente-checks").replaceChildren();$("sistema-cliente").replaceChildren();
    for(const c of clients){const label=document.createElement("label"),box=document.createElement("input");box.type="checkbox";box.value=c.id;label.append(box,document.createTextNode(c.nombre));$("cliente-checks").append(label);$("sistema-cliente").add(new Option(c.nombre,c.id));}
    $("clientes-lista").replaceChildren();
    for(const c of clients){const row=document.createElement("tr");cell(row,c.nombre);cell(row,c.cuit||"Sin dato");cell(row,c.contacto?.direccion||"Sin dato");cell(row,[c.contacto?.telefono,c.contacto?.email].filter(Boolean).join(" · ")||"Sin dato");const button=document.createElement("button");button.type="button";button.className="button secondary small";button.textContent="Editar cliente";button.onclick=()=>editClient(c);cell(row,"").append(button);$("clientes-lista").append(row);}
    for(const user of users){const row=document.createElement("tr");cell(row,user.login);cell(row,user.nombre);cell(row,user.rol);cell(row,user.activo?"Activa":"Baja");cell(row,user.rol==="admin"?"Todos":clients.filter(c=>user.cliente_ids.includes(c.id)).map(c=>c.nombre).join(", "));const button=document.createElement("button");button.type="button";button.className="button secondary small";button.textContent="Editar";button.onclick=()=>edit(user);cell(row,"").append(button);$("usuarios").append(row);}
    const records=await api("/api/admin/accesos");$("accesos").replaceChildren();for(const record of records){const row=document.createElement("tr");cell(row,new Date(record.fecha).toLocaleString("es-AR"));cell(row,users.find(u=>u.id===record.usuario_id)?.login||"Sin sesión");cell(row,record.evento);cell(row,record.ruta);cell(row,String(record.estado_http));$("accesos").append(row);}
  }
  $("usuario-form").onsubmit=async event=>{event.preventDefault();try{const cliente_ids=[...$("cliente-checks").querySelectorAll("input:checked")].map(i=>i.value);const body={rol:$("usuario-rol").value,cliente_ids};if(editing){body.certificado_conjunto=$("usuario-certificado").checked;body.activo=$("usuario-activo").checked;await api("/api/admin/usuarios/"+editing,{method:"PUT",body:JSON.stringify(body)});}else{Object.assign(body,{login:$("usuario-login").value,nombre:$("usuario-nombre").value,clave:$("usuario-clave").value});await api("/api/admin/usuarios",{method:"POST",body:JSON.stringify(body)});}reset();await refresh();message("Cuenta guardada. Las sesiones de una cuenta modificada deben volver a ingresar.");}catch(error){message(error.message);}};
  $("nuevo-usuario").onclick=reset;
  $("restablecer-clave").onclick=async()=>{try{await api("/api/admin/usuarios/"+editing+"/clave",{method:"POST",body:JSON.stringify({nueva:$("usuario-clave").value})});$("usuario-clave").value="";message("Contraseña reemplazada y sesiones cerradas.");}catch(error){message(error.message);}};
  let consultaCliente=0;
  const cuitActual=()=>$("cliente-cuit").value.trim().replaceAll("-","");
  function cuitValido(){const raw=$("cliente-cuit").value.trim(),cuit=cuitActual();if(!/^(?:[0-9]{11}|[0-9]{2}-[0-9]{8}-[0-9])$/.test(raw))return false;const pesos=[5,4,3,2,7,6,5,4,3,2];let digito=11-pesos.reduce((s,p,i)=>s+p*Number(cuit[i]),0)%11;if(digito===11)digito=0;return digito<10&&digito===Number(cuit[10]);}
  function completarVacios(data,campos){for(const key of campos){const input=$("cliente-"+key),value=key==="nombre"?data.nombre:data.contacto?.[key];if(!input.value.trim()&&value)input.value=value;}}
  function resetClient(){consultaCliente++;editingClient=null;$("cliente-form").reset();$("cliente-editor-title").textContent="Agregar cliente";if($("buscar-cliente-cuit"))$("buscar-cliente-cuit").hidden=false;if($("contabilium-cuit-estado"))$("contabilium-cuit-estado").textContent="";}
  function editClient(cliente){consultaCliente++;editingClient=cliente.id;if($("buscar-cliente-cuit"))$("buscar-cliente-cuit").hidden=true;$("cliente-nombre").value=cliente.nombre;$("cliente-cuit").value=cliente.cuit||"";for(const key of ["direccion","telefono","email"])$("cliente-"+key).value=cliente.contacto?.[key]||"";$("cliente-editor-title").textContent="Editar cliente";$("cliente-form").scrollIntoView({behavior:"smooth"});}
  $("cliente-cuit").addEventListener("input",()=>{consultaCliente++;if($("contabilium-cuit-estado"))$("contabilium-cuit-estado").textContent="";});
  $("cliente-nuevo").onclick=resetClient;
  $("cliente-form").onsubmit=async event=>{event.preventDefault();try{const wasEditing=!!editingClient,body={nombre:$("cliente-nombre").value,cuit:$("cliente-cuit").value.trim()||null,contacto:{direccion:$("cliente-direccion").value,telefono:$("cliente-telefono").value,email:$("cliente-email").value}};await api(editingClient?"/api/admin/clientes/"+editingClient:"/api/admin/clientes",{method:editingClient?"PUT":"POST",body:JSON.stringify(body)});resetClient();await refresh();message(wasEditing?"Cliente guardado.":$("cliente-form").dataset.piloto==="true"?"Cliente de ejemplo creado.":"Cliente creado.");}catch(error){message(error.message);}};
  if($("buscar-cliente-cuit"))$("buscar-cliente-cuit").onclick=async()=>{
    const button=$("buscar-cliente-cuit"),estado=$("contabilium-cuit-estado");
    if(editingClient)return;
    if(!cuitValido()){estado.textContent="Ingresá un CUIT válido de once dígitos.";return;}
    const cuit=cuitActual(),consulta=++consultaCliente;button.disabled=true;estado.textContent="Buscando en Contabilium…";
    try{
      const data=await api("/api/admin/contabilium/cliente-por-cuit?cuit="+encodeURIComponent(cuit));
      if(consulta!==consultaCliente||cuitActual()!==cuit||editingClient)return;
      if(!data.encontrado){estado.textContent="No se encontró ese CUIT en Contabilium. Podés usar Consultar ARCA y completar el resto a mano.";return;}
      if(data.cliente?.cuit!==cuit)throw new Error("La respuesta no corresponde al CUIT consultado.");
      completarVacios(data.cliente,["nombre","direccion","telefono","email"]);
      estado.textContent="Se completaron los campos vacíos desde Contabilium. Revisalos y tocá Guardar cliente cuando decidas guardarlo.";
    }catch(error){if(consulta===consultaCliente)estado.textContent=error.message;}finally{button.disabled=false;}
  };
  if($("consultar-arca"))$("consultar-arca").onclick=async()=>{
    const button=$("consultar-arca"),estado=$("arca-estado");button.disabled=true;
    const informar=text=>{estado.textContent=text;message(text);};
    const cuit=cuitActual(),consulta=++consultaCliente,clienteEditado=editingClient;
    estado.textContent="Consultando ARCA mediante Contabilium…";
    try{
      const data=await api("/api/admin/contabilium/arca?cuit="+encodeURIComponent($("cliente-cuit").value.trim()));
      if(consulta!==consultaCliente||cuitActual()!==cuit||editingClient!==clienteEditado)return;
      completarVacios(data,["nombre","direccion"]);
      informar("Datos recibidos del padrón a través de Contabilium. Revisalos y tocá Guardar cliente para guardarlos.");
    }catch(error){if(consulta===consultaCliente)informar(error.message);}finally{button.disabled=false;}
  };
  if($("contabilium-form"))$("contabilium-form").onsubmit=async event=>{
    event.preventDefault();const button=event.submitter;button.disabled=true;
    try{
      const data=await api("/api/admin/contabilium/clientes?buscar="+encodeURIComponent($("contabilium-buscar").value.trim()));
      const results=$("contabilium-resultados");results.replaceChildren();
      if(!data.clientes.length)results.textContent="No se encontraron clientes. Probá con otro nombre o CUIT.";
      for(const cliente of data.clientes){
        const row=document.createElement("p"),label=document.createElement("span"),sync=document.createElement("button");
        label.textContent=cliente.nombre+" · "+(cliente.cuit||"Sin CUIT")+" ";sync.type="button";sync.className="button secondary small";sync.textContent="Traer / actualizar cliente";
        sync.onclick=async()=>{sync.disabled=true;try{await api("/api/admin/contabilium/sincronizar",{method:"POST",body:JSON.stringify({contabilium_id:cliente.contabilium_id})});await refresh();message("Cliente sincronizado. Seleccionalo al crear una planilla nueva; los borradores anteriores conservan sus datos.");}catch(error){message(error.message);}finally{sync.disabled=false;}};
        row.append(label,sync);results.append(row);
      }
    }catch(error){message(error.message);}finally{button.disabled=false;}
  };
  $("sistema-form").onsubmit=async event=>{event.preventDefault();try{await api("/api/admin/clientes/"+$("sistema-cliente").value+"/sistemas",{method:"POST",body:JSON.stringify({tipo:$("sistema-tipo").value,designacion:$("sistema-nombre").value})});$("sistema-nombre").value="";message("Sistema de ejemplo creado.");}catch(error){message(error.message);}};
  reset();refresh().catch(error=>message(error.message));
})();
