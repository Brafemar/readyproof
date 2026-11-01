const assert=require("node:assert/strict"),fs=require("node:fs"),path=require("node:path");
const {chromium}=require("playwright");
(async()=>{
 const executablePath=[process.env.READYPROOF_BROWSER,chromium.executablePath(),path.join(process.env.ProgramFiles||"C:/Program Files","Google/Chrome/Application/chrome.exe"),path.join(process.env.ProgramFiles||"C:/Program Files","Microsoft/Edge/Application/msedge.exe")].find(p=>p&&fs.existsSync(p));assert.ok(executablePath);
 const browser=await chromium.launch({headless:true,executablePath});const context=await browser.newContext({viewport:{width:390,height:844},hasTouch:true,isMobile:true});
 await context.addCookies([{name:process.env.RP_COOKIE_NAME,value:process.env.RP_COOKIE_VALUE,url:process.env.RP_URL,httpOnly:true,sameSite:"Lax"}]);
 const page=await context.newPage(),errors=[];page.on("pageerror",e=>errors.push(e.message));page.setDefaultTimeout(20000);
 try{
  await page.goto(process.env.RP_URL+"/_pruebas/c3b",{waitUntil:"networkidle"});await page.getByRole("button",{name:"Ver y marcar",exact:true}).click();
  await page.waitForFunction(()=>document.getElementById("foto-editor-imagen").naturalWidth===640&&document.querySelectorAll("#foto-anotaciones li").length===1);
  const rows=page.locator("#foto-anotaciones li");assert.equal(await rows.nth(0).locator('select[id^="foto-codigo-"]').inputValue(),"NA");
  await page.click("#foto-agregar-marca");const item=rows.nth(1).locator('select[id^="foto-item-"]');if(await item.count())await item.selectOption({index:1});await rows.nth(1).locator('select[id^="foto-codigo-"]').selectOption("O");await rows.nth(1).locator("textarea").fill("[Ejemplo] Observación guardada");
  await page.click("#foto-guardar-marcas");await page.waitForFunction(()=>document.getElementById("foto-marcas-estado").textContent.includes("guardadas en el servidor"));
  let server=await (await context.request.get(process.env.RP_URL+process.env.RP_FOTO_URL+"/anotaciones")).json();assert.equal(server.length,2);assert.equal(server[1].codigo,"O");
  let liberar,avisar;const retenida=new Promise(resolve=>liberar=resolve),iniciada=new Promise(resolve=>avisar=resolve);let primera=true;
  await page.route("**/anotaciones",async route=>{if(route.request().method()==="POST"&&primera){primera=false;avisar();await retenida;}await route.continue();});
  await rows.nth(1).locator("textarea").fill("[Ejemplo] Primer guardado en curso");await page.click("#foto-guardar-marcas");await iniciada;
  await rows.nth(1).locator("textarea").fill("[Ejemplo] Segundo guardado");await page.click("#foto-guardar-marcas");
  await page.waitForFunction(async()=>{const account=await window.readyproofSession;return new Promise(resolve=>{const r=indexedDB.open("readyproof-fotos-"+account.usuario.id,2);r.onsuccess=()=>{const db=r.result,q=db.transaction("anotaciones").objectStore("anotaciones").getAll();q.onsuccess=()=>{db.close();resolve(q.result[0]?.marcas?.[1]?.texto==="[Ejemplo] Segundo guardado");};};});});
  liberar();await page.waitForFunction(async url=>(await(await fetch(url)).json())[1]?.texto==="[Ejemplo] Segundo guardado",process.env.RP_FOTO_URL+"/anotaciones");await page.unroute("**/anotaciones");
  await page.reload({waitUntil:"networkidle"});await page.getByRole("button",{name:"Ver y marcar",exact:true}).click();await page.waitForFunction(()=>document.querySelectorAll("#foto-anotaciones li").length===2);
  await context.setOffline(true);await rows.nth(1).locator("textarea").fill("[Ejemplo] Edición sin conexión");await page.click("#foto-guardar-marcas");await page.waitForFunction(()=>document.getElementById("foto-marcas-estado").textContent.includes("pendientes de enviar"));
  await context.setOffline(false);await page.waitForFunction(()=>document.getElementById("foto-marcas-estado").textContent.includes("guardadas en el servidor"));
  server=await (await context.request.get(process.env.RP_URL+process.env.RP_FOTO_URL+"/anotaciones")).json();assert.equal(server[1].texto,"[Ejemplo] Edición sin conexión");
  const another=await browser.newContext({viewport:{width:1100,height:800}});await another.addCookies(await context.cookies());const other=await another.newPage();
  await other.goto(process.env.RP_URL+"/_pruebas/c3b",{waitUntil:"networkidle"});await other.getByRole("button",{name:"Ver y marcar",exact:true}).click();await other.waitForFunction(()=>document.getElementById("foto-editor-imagen").naturalWidth===640&&document.querySelectorAll("#foto-anotaciones li").length===2);assert.equal(await other.locator("#foto-anotaciones textarea").nth(1).inputValue(),"[Ejemplo] Edición sin conexión");await another.close();
  await page.locator("#fotos").screenshot({path:path.join(process.env.RP_OUT,"pwa_servidor.png")});assert.deepEqual(errors,[]);
  fs.writeFileSync(path.join(process.env.RP_OUT,"resultado_c3b.json"),JSON.stringify({imagen_desde_servidor:true,lectura_marcas:true,guardado_POST:true,recarga:true,cola_offline:true,guardados_consecutivos:true,otro_dispositivo:true,errores:errors},null,2));
 }finally{await context.close();await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
