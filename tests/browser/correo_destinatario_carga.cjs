const {chromium}=require('playwright');
const fs=require('fs'),path=require('path'),assert=require('assert/strict');
(async()=>{
 const input=JSON.parse(fs.readFileSync(0,'utf8'));
 const browser=await chromium.launch({headless:true,executablePath:process.env.READYPROOF_BROWSER||undefined,args:['--no-sandbox']});
 const report={caso:input.caso,ancho_px:390,destinatario_conservado:false,sin_envios:false};
 try{
  const context=await browser.newContext({viewport:{width:390,height:844},serviceWorkers:'block'}),page=await context.newPage();
  let envios=0;const pending=[];
  await context.route('**/*',async route=>{
   const url=new URL(route.request().url());
   if(url.origin!==input.url)return route.abort();
   if(url.pathname==='/api/correo/configuracion'){
    await new Promise(resolve=>pending.push(async config=>{await route.fulfill({json:config});resolve();}));return;
   }
   if(url.pathname.endsWith('/enviar')){envios++;return route.abort();}
   return route.continue();
  });
  await page.goto(input.url+'/login');await page.locator('#login').fill(input.usuario.login);await page.locator('#clave').fill(input.usuario.clave);
  await Promise.all([page.waitForURL(input.url+'/'),page.locator('button[type=submit]').click()]);await page.waitForLoadState('networkidle');
  await page.evaluate(async input=>{
   const user=await window.readyproofSession,open=indexedDB.open('readyproof-local-'+user.usuario.id,1);
   const db=await new Promise((resolve,reject)=>{open.onsuccess=()=>resolve(open.result);open.onerror=()=>reject(open.error);});
   const tx=db.transaction('borradores','readwrite');
   tx.objectStore('borradores').put({localId:'destinatario-regresion',clienteId:input.cliente_id,sistemaId:input.sistema_id,planillaId:input.planilla_id,
    serverId:input.carga.id,revision:input.carga.revision,estado:'emitida',datos:input.carga.datos,responsable:input.carga.responsable,
    firmas:{},firmasServidor:input.carga.firmas,firmantes:input.carga.firmantes,pdfHash:input.carga.pdf_sha256,
    pending:false,conflicto:false,editVersion:0,actualizado:'2099-01-01T00:00:00.000Z'});
   await new Promise((resolve,reject)=>{tx.oncomplete=resolve;tx.onerror=()=>reject(tx.error);});db.close();
  },input);
  await page.reload();await page.locator('#enviar-pdf').waitFor({state:'visible'});await page.waitForLoadState('networkidle');
  const waitRequest=async count=>{for(let i=0;i<200&&pending.length<count;i++)await new Promise(r=>setTimeout(r,10));assert.ok(pending.length>=count,'No llegó la solicitud de configuración');};
  await page.locator('#enviar-pdf').click();await waitRequest(1);
  const field=page.locator('#correo-destinatario');
  if(input.caso!=='sin_edicion')await field.fill('escrito@example.invalid');
  if(input.caso==='borrado')await field.fill('');
  await page.screenshot({path:path.join(input.out,'antes_de_configuracion.png')});
  if(input.caso==='reapertura'){
   await page.locator('#cerrar-correo').click();await page.locator('#enviar-pdf').click();await waitRequest(2);
   assert.equal(await field.inputValue(),'');await field.fill('nuevo@example.invalid');
   await pending[1]({habilitado:true,destinatarios:['nuevo-predeterminado@example.invalid']});
   await page.locator('#correo-estado').filter({hasText:'Confirmá el destinatario'}).waitFor();
   await pending[0]({habilitado:true,destinatarios:['viejo-predeterminado@example.invalid']});await page.waitForLoadState('networkidle');
   assert.equal(await field.inputValue(),'nuevo@example.invalid');
   assert.deepEqual(await page.locator('#correo-destinatarios option').evaluateAll(nodes=>nodes.map(n=>n.value)),['nuevo-predeterminado@example.invalid']);
  }else{
   await pending[0]({habilitado:true,destinatarios:input.caso==='vacio'?[]:['predeterminado@example.invalid']});
   await page.locator('#correo-estado').filter({hasText:'Confirmá el destinatario'}).waitFor();
   const expected=input.caso==='borrado'?'':input.caso==='sin_edicion'?'predeterminado@example.invalid':'escrito@example.invalid';
   assert.equal(await field.inputValue(),expected);
  }
  assert.equal(envios,0);report.destinatario_conservado=true;report.sin_envios=true;
  await page.screenshot({path:path.join(input.out,'despues_de_configuracion.png')});
  await page.locator('#cerrar-correo').click();
 }catch(error){report.error={tipo:error.name,mensaje:String(error.message).replaceAll(input.usuario.clave,'[OCULTO]')};process.exitCode=1;}
 finally{fs.writeFileSync(path.join(input.out,'resultado.json'),JSON.stringify(report,null,2));await browser.close();}
 console.log(JSON.stringify(report));
})().catch(error=>{console.log(JSON.stringify({error: error.name}));process.exitCode=1;});
