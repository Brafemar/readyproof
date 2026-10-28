const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const {chromium}=require('playwright');
(async()=>{
 const candidates=[process.env.READYPROOF_BROWSER,chromium.executablePath(),path.join(process.env.ProgramFiles||'C:/Program Files','Google/Chrome/Application/chrome.exe'),path.join(process.env['ProgramFiles(x86)']||'C:/Program Files (x86)','Microsoft/Edge/Application/msedge.exe')];
 const browser=await chromium.launch({headless:true,executablePath:candidates.find(p=>p&&fs.existsSync(p))});
 const context=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true,locale:'es-AR'});
 const page=await context.newPage(),record=JSON.parse(process.env.RP_BORRADOR),base=process.env.RP_URL;
 try{
  await page.goto(base+'/login');await page.locator('#login').fill(process.env.RP_LOGIN);await page.locator('#clave').fill(process.env.RP_PASSWORD);
  await Promise.all([page.waitForURL(base+'/'),page.getByRole('button',{name:'Ingresar',exact:true}).click()]);
  await page.locator('#cabecera-campos input').first().waitFor();
  await page.evaluate(async record=>{
   const account=await window.readyproofSession;
   await new Promise((resolve,reject)=>{const r=indexedDB.open('readyproof-local-'+account.usuario.id,1);r.onsuccess=()=>{const tx=r.result.transaction('borradores','readwrite');tx.objectStore('borradores').clear();tx.objectStore('borradores').put(record);tx.oncomplete=()=>{r.result.close();resolve();};tx.onerror=()=>reject(tx.error);};});
  },record);
  const [restored]=await Promise.all([
   page.waitForResponse(r=>r.url().endsWith('/api/cargas/'+record.serverId)&&r.request().method()==='GET'),
   page.reload()
  ]);assert.equal(restored.status(),200);
  await page.waitForFunction(name=>document.querySelector('#cabecera-campos input')&&document.getElementById('responsable-nombre').value===name,record.responsable.nombre_firmante);
  assert.equal(await page.locator('body').getAttribute('data-modo-piloto'),'false');
  assert.equal(await page.locator('.page-foot').textContent(),'readyproof · Registro de servicio.');
  assert.equal(await page.locator('#completar-ejemplo').isVisible(),false);
  const [saved]=await Promise.all([
   page.waitForResponse(r=>r.url().endsWith('/borrador')&&r.request().method()==='PUT'),
   page.locator('#responsable-nombre').fill('Responsable de ensayo [Ejemplo]')
  ]);assert.equal(saved.status(),200);
  const [preview]=await Promise.all([page.waitForResponse(r=>r.url().endsWith('/vista-previa'),{timeout:90000}),page.locator('#vista-previa').click()]);
  assert.equal(preview.status(),200);await page.waitForFunction(()=>document.getElementById('preview-status').textContent.includes('Vista previa lista'),null,{timeout:90000});
  await page.locator('#cerrar-preview').click();await page.locator('#preview-dialog').waitFor({state:'hidden'});
  await page.waitForFunction(()=>!document.getElementById('finalizar').disabled);
  const [emission]=await Promise.all([page.waitForResponse(r=>r.url().endsWith('/emitir'),{timeout:90000}),page.locator('#finalizar').click()]);
  assert.equal(emission.status(),201,await emission.text());const row=await emission.json();
  assert.equal(row.estado,'emitida');assert.ok(row.numero_registro);assert.equal(row.revision_publica,0);
  fs.writeFileSync(process.env.RP_RESULTADO,JSON.stringify({id:row.id,estado:row.estado,modo:'REAL',datos_ficticios:true}));
 }finally{await browser.close();}
})().catch(error=>{console.error(error);process.exitCode=1;});
