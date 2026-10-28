"use strict";
(() => {
  const form=document.getElementById('buscar-registro'),status=document.getElementById('buscar-estado'),result=document.getElementById('buscar-resultado');
  const labels={numero_registro:'Registro',cliente:'Cliente',sistema:'Sistema',planilla:'Planilla',estado:'Estado',revision_publica:'Revisión',fecha_emision:'Fecha de emisión'};
  form.addEventListener('submit',async event=>{
    event.preventDefault();result.replaceChildren();status.textContent='Buscando…';
    if(!form.reportValidity())return;
    const button=form.querySelector('button');button.disabled=true;
    try{
      const response=await fetch('/api/carga/buscar?numero='+encodeURIComponent(document.getElementById('numero-registro').value.trim()),{cache:'no-store'});
      if(response.status===401){location.replace('/login');return;}
      const row=await response.json();if(!response.ok)throw new Error(row.error||'No se pudo consultar el registro.');
      for(const [key,label] of Object.entries(labels)){
        const term=document.createElement('dt'),value=document.createElement('dd');term.textContent=label;value.textContent=row[key]??'—';result.append(term,value);
      }
      status.textContent='Registro encontrado.';
    }catch(error){status.textContent=navigator.onLine?error.message:'La búsqueda necesita conexión al servidor.';}
    finally{button.disabled=false;}
  });
})();
