const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const {chromium}=require('playwright');
(async()=>{
 const candidates=[process.env.READYPROOF_BROWSER,chromium.executablePath(),path.join(process.env.ProgramFiles||'C:/Program Files','Google/Chrome/Application/chrome.exe'),path.join(process.env.ProgramFiles||'C:/Program Files','Microsoft/Edge/Application/msedge.exe')];
 const browser=await chromium.launch({headless:true,executablePath:candidates.find(p=>p&&fs.existsSync(p))});
 const context=await browser.newContext();const page=await context.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
 const items=JSON.parse(process.env.RP_ITEMS),fotos=[],guardadas=[];let envios=0;
 const html=fs.readFileSync('app/templates/carga.html','utf8'),start=html.indexOf('<section id="fotos"'),end=html.indexOf('<section class="card" id="firmas"',start);
 await page.route('http://127.0.0.1:40124/**',async route=>{
  const url=new URL(route.request().url()),method=route.request().method();
  if(url.pathname==='/static/fotos.js')return route.fulfill({contentType:'text/javascript; charset=utf-8',body:fs.readFileSync('app/static/fotos.js','utf8')});
  if(url.pathname.endsWith('/items'))return route.fulfill({json:items});
  if(url.pathname.endsWith('/anotaciones')){
   if(method==='POST'){envios++;guardadas.splice(0,guardadas.length,...route.request().postDataJSON().anotaciones);}
   return route.fulfill({json:guardadas,headers:{ETag:'"ejemplo"'}});
  }
  if(url.pathname.endsWith('/fotos')){
   if(method==='POST')fotos.push({id:route.request().headers()['idempotency-key'],orden:1,ancho:800,alto:600});
   return route.fulfill({json:method==='POST'?fotos[0]:fotos});
  }
  return route.fulfill({contentType:'text/html; charset=utf-8',body:`<!doctype html><meta charset="utf-8"><style>[hidden]{display:none!important}</style><script>window.readyproofSession=Promise.resolve({usuario:{id:'item-ejemplo'},csrf_token:'ejemplo'});window.readyproofFotosBorrador=async()=>({serverId:'carga-ejemplo',pending:false,conflicto:false,estado:'borrador'});window.addEventListener('DOMContentLoaded',()=>window.dispatchEvent(new CustomEvent('readyproof-fotos-contexto',{detail:{localId:'local-ejemplo',serverId:'carga-ejemplo',readOnly:false,estado:'borrador'}})),{once:true});</script>${html.slice(start,end)}<script src="/static/fotos.js"></script>`});
 });
 try{
  await page.goto('http://127.0.0.1:40124/');await page.waitForFunction(()=>!document.getElementById('foto-archivo').disabled);
  const jpeg=await page.evaluate(()=>{const c=document.createElement('canvas');c.width=800;c.height=600;return c.toDataURL('image/jpeg').split(',')[1];});
  await page.locator('#foto-archivo').setInputFiles({name:'ejemplo.jpg',mimeType:'image/jpeg',buffer:Buffer.from(jpeg,'base64')});
  await page.waitForFunction(()=>document.getElementById('fotos-lista').textContent.includes('Guardada'));
  await page.getByRole('button',{name:'Ver y marcar',exact:true}).click();await page.locator('#foto-editor').waitFor({state:'visible'});await page.click('#foto-agregar-marca');
  let row=page.locator('#foto-anotaciones li').first(),item=row.locator('select[id^="foto-item-"]'),code=row.locator('select[id^="foto-codigo-"]');
  assert.deepEqual(await code.locator('option').allTextContents(),['Elegí un código','✓ (cumple)','O (no cumple)','X (no apreciable)','NA (no aplicable)']);
  assert.deepEqual(await code.locator('option').evaluateAll(nodes=>nodes.map(n=>n.value)),['','✓','O','X','NA']);
  assert.equal(await item.locator('option').nth(1).textContent(),items[0].texto);assert.equal(await code.isDisabled(),true);assert.equal(await code.inputValue(),'');
  await item.selectOption(JSON.stringify([items[0].bloque,items[0].campo]));assert.equal(await code.isDisabled(),false);assert.equal(await code.inputValue(),'');assert.equal(envios,0);
  await code.selectOption('O');await row.locator('textarea').fill('Se observa grasa.');await page.click('#foto-guardar-marcas');
  await page.waitForFunction(()=>document.getElementById('foto-marcas-estado').textContent.includes('Marcas guardadas en el servidor'));
  assert.equal(guardadas[0].item.campo,items[0].campo);assert.equal(guardadas[0].codigo,'O');assert.equal(guardadas[0].texto,'Se observa grasa.');
  await page.click('#foto-cerrar-editor');await page.getByRole('button',{name:'Ver y marcar',exact:true}).click();await page.locator('#foto-editor').waitFor({state:'visible'});
  row=page.locator('#foto-anotaciones li').first();item=row.locator('select[id^="foto-item-"]');code=row.locator('select[id^="foto-codigo-"]');
  assert.equal(await item.inputValue(),JSON.stringify([items[0].bloque,items[0].campo]));await item.selectOption(JSON.stringify([items[1].bloque,items[1].campo]));assert.equal(await code.inputValue(),'O');
  assert.deepEqual(errors,[]);console.log('Item recuperado; codigo elegido por el tecnico y no alterado al cambiar item.');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1);});
