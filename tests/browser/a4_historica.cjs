const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const {chromium}=require('playwright');
(async()=>{
 const candidates=[process.env.READYPROOF_BROWSER,chromium.executablePath(),path.join(process.env.ProgramFiles||'C:/Program Files','Google/Chrome/Application/chrome.exe'),path.join(process.env['ProgramFiles(x86)']||'C:/Program Files (x86)','Microsoft/Edge/Application/msedge.exe')];
 const browser=await chromium.launch({headless:true,executablePath:candidates.find(p=>p&&fs.existsSync(p))});
 const context=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true,locale:'es-AR'});
 const page=await context.newPage(),errors=[];page.on('pageerror',error=>errors.push(error.message));
 const base=process.env.RP_URL,old=JSON.parse(process.env.RP_HISTORICA);
 try{
  await page.goto(base+'/login');await page.locator('#login').fill(process.env.RP_LOGIN);await page.locator('#clave').fill(process.env.RP_PASSWORD);
  await Promise.all([page.waitForURL(base+'/'),page.getByRole('button',{name:'Ingresar',exact:true}).click()]);
  await page.waitForFunction(()=>document.getElementById('save-status').textContent.includes('y en el servidor'));
  await page.evaluate(async record=>{
   const account=await window.readyproofSession;
   await new Promise((resolve,reject)=>{const r=indexedDB.open('readyproof-local-'+account.usuario.id,1);r.onsuccess=()=>{const tx=r.result.transaction('borradores','readwrite');const store=tx.objectStore('borradores');store.clear();store.put(record);tx.oncomplete=()=>{r.result.close();resolve();};tx.onerror=()=>reject(tx.error);};});
  },old);
  await page.reload();await page.locator('#copiar-a4').waitFor({state:'visible'});
  assert.equal(await page.locator('#descargar').textContent(),'Descargar PDF anterior');
  assert.equal(await page.locator('#enviar-pdf').isDisabled(),true);
  assert.equal(await page.locator('#vista-previa').isDisabled(),true);
  await page.locator('#copiar-a4').click();
  await page.waitForFunction(()=>document.getElementById('save-status').textContent.includes('y en el servidor'));
  assert.equal(await page.locator('#copiar-a4').isVisible(),false);
  assert.ok((await page.locator('#firma-tecnico-status').textContent()).includes('guardada'));
  assert.equal(await page.locator('#finalizar').isDisabled(),true);
  await page.locator('#responsable-nombre').fill('[Ejemplo] Responsable de prueba');
  await page.locator('#responsable-dni').fill('00000000');
  await page.waitForFunction(()=>document.getElementById('save-status').textContent.includes('y en el servidor'));
  const [previewResponse]=await Promise.all([
   page.waitForResponse(r=>r.url().endsWith('/vista-previa')&&r.request().method()==='POST',{timeout:90000}),
   page.locator('#vista-previa').click()
  ]);
  assert.equal(previewResponse.status(),200);
  await page.waitForFunction(()=>document.getElementById('preview-status').textContent.includes('Vista previa lista'),null,{timeout:90000});
  await page.locator('#cerrar-preview').click();
  await page.locator('#preview-dialog').waitFor({state:'hidden'});
  await page.waitForFunction(()=>!document.getElementById('finalizar').disabled);
  const [response]=await Promise.all([
   page.waitForResponse(r=>r.url().endsWith('/emitir')&&r.request().method()==='POST',{timeout:90000}),
   page.locator('#finalizar').click()
  ]);
  assert.equal(response.status(),201,await response.text());
  const result=await response.json();assert.notEqual(result.id,old.serverId);
  await page.locator('#descargar').waitFor({state:'visible'});assert.equal(await page.locator('#descargar').textContent(),'Descargar PDF');
  assert.deepEqual(errors,[]);
  await page.screenshot({path:path.join(process.env.RP_OUT,'copia_A4_movil.png')});
  fs.writeFileSync(path.join(process.env.RP_OUT,'resultado.json'),JSON.stringify({carga_id:result.id,anterior:old.serverId,copia:true,errores:errors},null,2));
 }finally{await browser.close();}
})().catch(error=>{console.error(error);process.exitCode=1;});
