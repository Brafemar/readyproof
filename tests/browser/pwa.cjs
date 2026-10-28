const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const {chromium}=require('playwright');
(async()=>{
 const out=process.env.RP_OUT,base=process.env.RP_URL;
 const candidates=[process.env.READYPROOF_BROWSER,'C:/Program Files/Google/Chrome/Application/chrome.exe',chromium.executablePath(),'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'];
 const profile=path.join(out,'perfil_chrome');assert.equal(fs.existsSync(profile),false);
 const context=await chromium.launchPersistentContext(profile,{headless:false,executablePath:candidates.find(p=>p&&fs.existsSync(p)),viewport:{width:1100,height:820},locale:'es-AR'});
 const page=context.pages()[0],errors=[];page.on('pageerror',error=>errors.push(error.message));
 try{
  await page.goto(base+'/login');await page.locator('#login').fill(process.env.RP_LOGIN);await page.locator('#clave').fill(process.env.RP_PASSWORD);
  await Promise.all([page.waitForURL(base+'/'),page.getByRole('button',{name:'Ingresar',exact:true}).click()]);
  await page.locator('#cabecera-campos input').first().waitFor();
  await page.evaluate(()=>navigator.serviceWorker.ready);
  await page.waitForFunction(()=>navigator.serviceWorker.controller!==null);
  await page.reload();await page.locator('#cabecera-campos input').first().waitFor();
  const cdp=await context.newCDPSession(page);await cdp.send('Page.enable');
  const manifest=await cdp.send('Page.getAppManifest');assert.equal(manifest.errors.length,0,JSON.stringify(manifest.errors));
  const data=JSON.parse(manifest.data);assert.equal(data.name,'readyproof');assert.equal(data.display,'standalone');assert.equal(data.icons.length,4);
  const install=await cdp.send('Page.getInstallabilityErrors');assert.deepEqual(install.installabilityErrors,[]);
  const worker=await page.evaluate(async()=>{const r=await navigator.serviceWorker.ready;return {scope:r.scope,status:r.active.state,url:r.active.scriptURL};});
  assert.equal(worker.scope,base+'/');assert.equal(worker.status,'activated');assert.equal(worker.url,base+'/sw.js');
  const registrations=await page.evaluate(()=>navigator.serviceWorker.getRegistrations().then(rows=>rows.map(r=>r.scope)));assert.deepEqual(registrations,[base+'/']);
  const icons=await page.evaluate(async data=>Promise.all(data.icons.map(async icon=>{const image=new Image();image.src=icon.src;await image.decode();return {src:icon.src,width:image.naturalWidth,height:image.naturalHeight};})),data);
  for(const icon of icons){assert.ok([192,512].includes(icon.width));assert.equal(icon.width,icon.height);}
  await page.screenshot({path:path.join(out,'pwa_conectada.png'),fullPage:true});
  // El indicador onLine no demuestra acceso al servidor. Se corta el servidor
  // efímero además de emular Offline para probar también los fetch del worker.
  fs.writeFileSync(path.join(out,'desconectar.request'),'offline');
  await page.waitForFunction(()=>true);
  const deadline=Date.now()+20000;
  while(!fs.existsSync(path.join(out,'desconectado.ok'))){assert.ok(Date.now()<deadline,'No se confirmó el corte del servidor de prueba');await new Promise(resolve=>setTimeout(resolve,100));}
  await context.setOffline(true);await page.reload();await page.locator('#cabecera-campos input').first().waitFor();
  const offlineAsset=await page.evaluate(()=>fetch('/static/carga.js').then(async r=>({ok:r.ok,body:(await r.text()).length})));assert.equal(offlineAsset.ok,true);assert.ok(offlineAsset.body>1000);
  const apiBlocked=await page.evaluate(()=>fetch('/api/auth/sesion',{cache:'no-store'}).then(()=>false,()=>true));assert.equal(apiBlocked,true,'La API debe ser inaccesible con el servidor apagado.');
  const cached=await page.evaluate(async()=>{const names=await caches.keys();let urls=[];for(const name of names){const c=await caches.open(name);urls.push(...(await c.keys()).map(r=>r.url));}return urls;});
  assert.ok(cached.includes(base+'/'));assert.equal(cached.some(url=>new URL(url).pathname.startsWith('/api/')||new URL(url).pathname.endsWith('.pdf')),false);
  assert.deepEqual(errors,[]);await page.screenshot({path:path.join(out,'pwa_sin_conexion.png'),fullPage:true});
  await context.setOffline(false);
  const report={servidor:base,manifest:{name:data.name,display:data.display,iconos:icons},installability_errors:install.installabilityErrors,worker,registros:registrations.length,offline:true,servidor_apagado_en_prueba:true,api_inaccesible:apiBlocked,assets_en_cache:cached.length,errores_javascript:errors};
  fs.writeFileSync(path.join(out,'navegador.json'),JSON.stringify(report,null,2));console.log(JSON.stringify(report));
 }finally{await context.close();}
})().catch(error=>{console.error(error.stack);process.exitCode=1;});
