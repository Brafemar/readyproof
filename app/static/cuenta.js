"use strict";
(() => {
  const form=document.getElementById("correo-cuenta"),email=document.getElementById("email-cuenta");
  const save=document.getElementById("guardar-correo"),send=document.getElementById("enviar-documentacion"),status=document.getElementById("documentacion-estado");
  const csrf=document.querySelector('input[name="csrf_token"]').value,keyName="readyproof-documentacion-"+form.dataset.usuario;
  const dialog=document.getElementById("documentacion-dialog"),modalForm=document.getElementById("documentacion-form"),recipient=document.getElementById("documentacion-destinatario"),confirm=document.getElementById("confirmar-documentacion"),close=document.getElementById("cerrar-documentacion"),modalStatus=document.getElementById("documentacion-modal-estado");
  let savedEmail=email.value,busy=false,sent=false;
  function update(){save.disabled=busy;send.disabled=busy;confirm.disabled=busy||sent;close.disabled=busy;recipient.disabled=busy||sent;}
  async function api(path,options){
    const response=await fetch(path,{...options,headers:{"Content-Type":"application/json","X-CSRF-Token":csrf,...options.headers}});
    let data;try{data=await response.json();}catch{throw new Error("No se pudo leer la respuesta. No repitas el envío; consultá a Administración.");}
    return {response,data};
  }
  email.addEventListener("input",()=>{update();status.textContent=modalStatus.textContent="Guardá el correo modificado antes de enviar.";});
  form.addEventListener("submit",async event=>{
    event.preventDefault();if(busy||!form.reportValidity())return;
    busy=true;update();
    try{
      const {response,data}=await api("/api/usuario/correo",{method:"PUT",body:JSON.stringify({email:email.value})});
      if(!response.ok)throw new Error(data.error||"No se pudo guardar el correo.");
      savedEmail=data.email;email.value=savedEmail;status.textContent=modalStatus.textContent="Correo guardado: "+savedEmail+".";
    }catch(error){status.textContent=modalStatus.textContent=error.message;}
    finally{busy=false;update();}
  });
  send.addEventListener("click",()=>{if(busy)return;sent=false;recipient.value=savedEmail||email.value;modalStatus.textContent="";update();dialog.showModal();recipient.focus();});
  close.addEventListener("click",()=>{if(!busy)dialog.close();});
  dialog.addEventListener("cancel",event=>{if(busy)event.preventDefault();});
  modalForm.addEventListener("submit",async event=>{
    event.preventDefault();if(busy||sent||!modalForm.reportValidity())return;
    busy=true;update();status.textContent=modalStatus.textContent="Enviando documentación…";
    try{
      let key=sessionStorage.getItem(keyName);
      if(!key){key=crypto.randomUUID();sessionStorage.setItem(keyName,key);}
      const {response,data}=await api("/api/usuario/enviar-documentacion",{method:"POST",headers:{"Idempotency-Key":key},body:JSON.stringify({destinatario:recipient.value})});
      if(!response.ok){if(data.estado==="fallo")sessionStorage.removeItem(keyName);throw new Error(data.error||"No se pudo confirmar el envío. Consultá a Administración.");}
      if(data.estado==="enviado")status.textContent=modalStatus.textContent="Gmail aceptó el correo a "+data.destinatario+". Revisá tu bandeja y spam; se adjuntaron las guías, sin contraseñas.";
      else if(data.estado==="archivado")status.textContent=modalStatus.textContent="Modo de prueba: documentación archivada, sin envío real.";
      else throw new Error("El envío no está confirmado. Consultá a Administración.");
      sent=true;
      sessionStorage.removeItem(keyName);
    }catch(error){status.textContent=modalStatus.textContent=error.message+" No se reenvía automáticamente.";}
    finally{busy=false;update();}
  });
  update();
})();
