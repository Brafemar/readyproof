"use strict";
(() => {
  const key="readyproof-cuenta-activa";
  let channel;
  async function expired(){sessionStorage.removeItem(key);window.dispatchEvent(new Event("readyproof-lock"));location.replace("/login");}
  window.readyproofExpired=expired;
  window.readyproofSession=(async()=>{
    let data;
    try{
      const response=await fetch("/api/auth/sesion",{cache:"no-store"});
      if(!response.ok)throw new Error("No se pudo comprobar la sesión.");
      data=await response.json();
      if(!data.usuario){await expired();throw new Error("Iniciá sesión.");}
      sessionStorage.setItem(key,JSON.stringify(data));
    }catch(error){
      const cached=sessionStorage.getItem(key);
      if(!cached){await expired();throw error;}
      data=JSON.parse(cached);
      if(!data.usuario||new Date(data.vence_en).getTime()<=Date.now()){await expired();throw error;}
    }
    const tools=document.getElementById("account-tools");if(tools)tools.hidden=false;
    const label=document.getElementById("usuario-actual");if(label)label.textContent=data.usuario.nombre;
    const admin=document.getElementById("administracion");if(admin)admin.hidden=data.usuario.rol!=="admin";
    channel=new BroadcastChannel("readyproof-cuenta");
    channel.onmessage=event=>{if(event.data==="logout"||(event.data?.type==="login"&&event.data.usuario!==data.usuario.id))expired();};
    channel.postMessage({type:"login",usuario:data.usuario.id});
    setTimeout(()=>expired(),Math.max(0,new Date(data.vence_en).getTime()-Date.now()));
    const logout=document.getElementById("salir");if(logout)logout.onclick=async()=>{
      if(!navigator.onLine){alert("Conectate al servidor para cerrar la sesión y retirar los borradores de este dispositivo.");return;}
      if(!confirm("Al salir se retiran de este navegador los borradores de esta cuenta, incluidos los cambios pendientes. ¿Cerrar sesión?"))return;
      const response=await fetch("/api/auth/logout",{method:"POST",headers:{"X-CSRF-Token":data.csrf_token}});
      if(!response.ok){alert("No se pudo cerrar la sesión. Revisá la conexión.");return;}
      window.dispatchEvent(new Event("readyproof-lock"));
      indexedDB.deleteDatabase("readyproof-local-"+data.usuario.id);
      sessionStorage.removeItem(key);channel.postMessage("logout");location.replace("/login");
    };
    return data;
  })();
})();