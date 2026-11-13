const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const {chromium}=require('playwright');
const base=process.env.RP_URL,out=process.env.RP_OUT,expected=JSON.parse(process.env.RP_SELECTION);
(async()=>{
  const candidates=[process.env.READYPROOF_BROWSER,chromium.executablePath(),path.join(process.env.ProgramFiles||'C:/Program Files','Google/Chrome/Application/chrome.exe'),path.join(process.env['ProgramFiles(x86)']||'C:/Program Files (x86)','Microsoft/Edge/Application/msedge.exe')];
  const executablePath=candidates.find(item=>item&&fs.existsSync(item));assert.ok(executablePath);
  const browser=await chromium.launch({headless:true,executablePath});
  const mobile=expected.contacto!==null;
  const context=await browser.newContext({locale:'es-AR',viewport:mobile?{width:390,height:844}:{width:1280,height:900},
    isMobile:mobile,hasTouch:mobile});
  const page=await context.newPage(),errors=[];
  page.on('pageerror',error=>errors.push(error.message));
  async function record(){return page.evaluate(()=>new Promise((resolve,reject)=>{
    const user=JSON.parse(sessionStorage.getItem('readyproof-cuenta-activa')).usuario.id;
    const open=indexedDB.open('readyproof-local-'+user,1);
    open.onerror=()=>reject(open.error);open.onsuccess=()=>{
      const db=open.result,tx=db.transaction('borradores'),request=tx.objectStore('borradores').get(document.getElementById('borradores').value);
      request.onsuccess=()=>{resolve(request.result);db.close();};request.onerror=()=>reject(request.error);
    };
  }));}
  async function selected(id,value,key){
    await page.locator('#'+id).selectOption(value);
    await page.waitForFunction(({id,value})=>document.getElementById(id).value===value,{id,value});
    let saved;
    for(let attempt=0;attempt<100;attempt++){
      saved=await record();if(saved?.[key]===value && (mobile||!saved.pending))break;
      await new Promise(resolve=>setTimeout(resolve,100));
    }
    assert.equal(saved[key],value);
    if(!mobile)assert.equal(saved.pending,false);
  }
  try{
    await page.goto(base+'/login');await page.locator('#login').fill(process.env.RP_LOGIN);await page.locator('#clave').fill(process.env.RP_PASSWORD);
    await Promise.all([page.waitForURL(base+'/'),page.getByRole('button',{name:'Ingresar',exact:true}).click()]);
    await page.locator('#cabecera-campos input').first().waitFor();
    if(!mobile)await page.waitForFunction(()=>document.getElementById('save-status').textContent.includes('y en el servidor'));
    await page.evaluate(()=>{window.selectionEvents={};for(const id of ['cliente','sistema','planilla'])document.getElementById(id).addEventListener('change',()=>window.selectionEvents[id]=(window.selectionEvents[id]||0)+1);});
    assert.equal(await page.locator('#cliente option').count(),2);
    assert.match(await page.locator('#seleccion-ayuda').textContent(),/2 clientes disponibles/);
    await selected('cliente',expected.otro_cliente,'clienteId');
    assert.equal(await page.locator('#sistema').inputValue(),expected.otro_sistema);
    if(mobile){
      const etiquetas={cuit:'CUIT',telefono:'Teléfono',direccion:'Dirección'};
      for(const [campo,valor] of Object.entries(expected.contacto)){
        assert.equal(await page.getByLabel(etiquetas[campo],{exact:true}).inputValue(),valor);
        assert.equal((await record()).datos.cabecera[campo],valor);
      }
      for(const etiqueta of ['Edificio','Sector'])assert.equal(await page.getByLabel(etiqueta,{exact:true}).inputValue(),'');
      assert.equal(await page.evaluate(()=>innerWidth),390);
      await page.getByLabel('Dirección',{exact:true}).scrollIntoViewIfNeeded();
      await page.screenshot({path:path.join(out,'autocompletado_390.png')});
      const telefonoEditado='[Ejemplo] Teléfono de obra';
      await page.getByLabel('Teléfono',{exact:true}).fill(telefonoEditado);
      await page.getByLabel('Dirección',{exact:true}).fill('');
      let editado;
      for(let attempt=0;attempt<100;attempt++){
        editado=await record();
        if(editado?.datos.cabecera.telefono===telefonoEditado && editado.datos.cabecera.direccion===undefined)break;
        await new Promise(resolve=>setTimeout(resolve,100));
      }
      assert.equal(editado.datos.cabecera.telefono,telefonoEditado);
      assert.equal(editado.datos.cabecera.direccion,undefined);
      await page.reload();
      await page.locator('#cabecera-campos input').first().waitFor();
      assert.equal(await page.getByLabel('Teléfono',{exact:true}).inputValue(),telefonoEditado);
      assert.equal(await page.getByLabel('Dirección',{exact:true}).inputValue(),'');
      await page.locator('#cliente[data-catalogo-reconciliado=true]:enabled').waitFor();
      await selected('cliente',expected.cliente,'clienteId');
      for(const etiqueta of Object.values(etiquetas))assert.equal(await page.getByLabel(etiqueta,{exact:true}).inputValue(),'');
      assert.deepEqual(errors,[]);
      fs.writeFileSync(path.join(out,'resultado.json'),JSON.stringify({ancho_px:390,autocompletado:true,
        edicion_conservada:true,borrado_manual_conservado:true,edificio_y_sector_manuales:true},null,2));
      return;
    }
    await selected('cliente',expected.cliente,'clienteId');
    await selected('sistema',expected.segundo_sistema,'sistemaId');
    await selected('planilla',expected.otra_planilla,'planillaId');
    const events=await page.evaluate(()=>window.selectionEvents);
    assert.ok(events.cliente>=2 && events.sistema>=1 && events.planilla>=1);
    assert.equal(await page.locator('#cliente').isEnabled(),true);
    assert.equal(await page.locator('#sistema').isEnabled(),true);
    assert.equal(await page.locator('#planilla').isEnabled(),true);
    await page.evaluate(()=>navigator.serviceWorker.ready.then(()=>true));
    await page.waitForFunction(()=>Boolean(navigator.serviceWorker.controller));
    await context.setOffline(true);
    const fallback=await page.evaluate(async()=>{const response=await fetch('/static/carga.js?prueba=sin-red');return {status:response.status,body:(await response.text()).length};});
    assert.equal(fallback.status,200);assert.ok(fallback.body>100);
    await context.setOffline(false);await page.reload();
    await page.locator('#cabecera-campos input').first().waitFor();
    assert.equal((await record()).planillaId,expected.otra_planilla);
    assert.deepEqual(errors,[]);
    await page.screenshot({path:path.join(out,'selectores.png')});
    fs.writeFileSync(path.join(out,'resultado.json'),JSON.stringify({cambios:events,recarga:true,indexeddb_conservada:true,errores:errors},null,2));
  }finally{await browser.close();}
})().catch(error=>{console.error(error);process.exitCode=1;});
