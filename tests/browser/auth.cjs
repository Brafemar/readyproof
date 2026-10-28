const assert=require("node:assert/strict"),fs=require("node:fs"),path=require("node:path");
const {chromium}=require("playwright");
(async()=>{
  const vm=require('node:vm'),source=fs.readFileSync('app/static/carga.js','utf8');
  const start=source.indexOf('  async function sync(show=false)'),end=source.indexOf('  function inputField',start);
  assert.ok(start>=0&&end>start);
  await vm.runInNewContext(`(async()=>{let finish;let draft={pending:true},syncPromise=new Promise(resolve=>finish=resolve);${source.slice(start,end)}const waiting=sync();draft=null;finish(false);return await waiting;})()`)
    .then(result=>assert.equal(result,false));
  const candidates=[process.env.READYPROOF_BROWSER,chromium.executablePath(),"C:/Program Files/Google/Chrome/Application/chrome.exe","C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"];
  const executable=candidates.find(p=>p&&fs.existsSync(p));assert.ok(executable);
  const browser=await chromium.launch({headless:true,executablePath:executable}),context=await browser.newContext({viewport:{width:1440,height:1000},locale:"es-AR"}),page=await context.newPage();
  const errors=[];page.on("pageerror",e=>errors.push(e.message));const base=process.env.RP_URL,out=process.env.RP_OUT;fs.mkdirSync(out,{recursive:true});
  try{
    await page.goto(base+"/login");await page.locator("#login").fill(process.env.RP_LOGIN);await page.locator("#clave").fill(process.env.RP_PASSWORD);
    await Promise.all([page.waitForURL(base+"/"),page.getByRole("button",{name:"Ingresar",exact:true}).click()]);
    await page.locator("#administracion").waitFor({state:"visible"});
    await page.getByRole("link",{name:"Administración",exact:true}).click();await page.waitForURL(base+"/admin");
    await page.locator("#usuarios tr").first().waitFor();
    await page.locator("#usuario-login").fill("tecnico-browser");await page.locator("#usuario-nombre").fill("[Ejemplo] Técnico navegador");await page.locator("#usuario-clave").fill(process.env.RP_SECOND_PASSWORD);await page.locator("#cliente-checks input").first().check();
    await page.getByRole("button",{name:"Guardar usuario",exact:true}).click();
    await page.getByRole("row").filter({hasText:"tecnico-browser"}).waitFor();
    assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
    await page.screenshot({path:path.join(out,"administracion.png"),fullPage:true});
    const csrf=(await (await context.request.get(base+"/api/auth/sesion")).json()).csrf_token;
    assert.equal((await context.request.post(base+"/api/auth/logout",{headers:{"X-CSRF-Token":csrf}})).status(),200);
    await page.goto(base+"/login");await page.locator("#login").fill("tecnico-browser");await page.locator("#clave").fill(process.env.RP_SECOND_PASSWORD);
    await Promise.all([page.waitForURL(base+"/"),page.getByRole("button",{name:"Ingresar",exact:true}).click()]);
    await page.locator("#cabecera-campos input").first().waitFor();
    assert.equal(await page.locator("#administracion").isVisible(),false);
    assert.equal((await context.request.get(base+"/api/admin/usuarios")).status(),403);
    const session=(await (await context.request.get(base+"/api/auth/sesion")).json());
    const names=await page.evaluate(()=>indexedDB.databases().then(rows=>rows.map(r=>r.name)));
    assert.ok(names.includes("readyproof-local-"+session.usuario.id));
    page.on("dialog",dialog=>dialog.accept());await page.locator("#salir").click();await page.waitForURL(base+"/login");
    assert.equal((await context.request.get(base+"/api/clientes")).status(),401);
    await page.waitForFunction(id=>indexedDB.databases().then(rows=>!rows.some(r=>r.name==="readyproof-local-"+id)),session.usuario.id);
    assert.deepEqual(errors,[]);
    await page.screenshot({path:path.join(out,"login.png")});
    const report={alta_usuario_desde_pantalla:true,asignacion_cliente:true,tecnico_sin_administracion:true,logout_revocado:true,errores_javascript:errors};fs.writeFileSync(path.join(out,"auth_resultado.json"),JSON.stringify(report,null,2));console.log(JSON.stringify(report));
  }finally{await context.close();await browser.close();}
})().catch(error=>{console.error(error.stack);process.exitCode=1;});
