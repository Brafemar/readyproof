const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const vm = require('node:vm');

async function guard(file, name, state) {
  const source = fs.readFileSync(file, 'utf8');
  const start = source.indexOf(`window.${name} = async () => {`);
  assert.ok(start >= 0);
  const end = source.indexOf('\n  };', start) + 5;
  const context = {window: {}, ...state};
  vm.runInNewContext(source.slice(start, end), context);
  return context.window[name]();
}
async function guards() {
  let count = 0;
  const draft = {localId:'ficticio',pending:false,conflicto:false,editVersion:3};
  const state = {operation:false,syncPromise:null,firmasActivas:new Set(),draft,storage:async()=>({...draft})};
  const carga = changes => guard('app/static/carga.js','readyproofActualizacionCarga',{...state,...changes});
  assert.equal(await carga({}), ''); count++;
  assert.match(await carga({operation:true}), /operación/); count++;
  assert.match(await carga({syncPromise:Promise.resolve()}), /operación/); count++;
  assert.match(await carga({firmasActivas:new Set(['tecnico'])}), /firma/); count++;
  assert.match(await carga({draft:{...draft,pending:true}}), /sincronizá/); count++;
  assert.match(await carga({draft:{...draft,conflicto:true}}), /conflicto/); count++;
  assert.match(await carga({storage:async()=>({...draft,editVersion:2})}), /guardar/); count++;
  assert.equal(await carga({draft:null}), ''); count++;
  const photo = {account:{},database:Promise.resolve(),locked:false,converting:null,working:false,sincronizandoMarcas:false,editor:null,escritura:Promise.resolve(),storage:async()=>[],almacen:async()=>[]};
  const fotos = changes => guard('app/static/fotos.js','readyproofActualizacionFotos',{...photo,...changes});
  assert.equal(await fotos({}), ''); count++;
  assert.match(await fotos({converting:'ficticio'}), /preparación/); count++;
  assert.match(await fotos({working:true}), /sincronización/); count++;
  assert.match(await fotos({sincronizandoMarcas:true}), /sincronización/); count++;
  assert.match(await fotos({editor:{}}), /cerrá la foto/); count++;
  assert.match(await fotos({storage:async()=>[{}]}), /pendientes/); count++;
  for (const row of [{borradorMarcas:[]},{pendienteServidor:true},{conflicto:true}]) {
    assert.match(await fotos({almacen:async()=>[row]}), /pendientes/); count++;
  }
  assert.match(await fotos({database:null}), /almacenamiento/); count++;
  console.log(JSON.stringify({casos_guardas:count}));
}
async function browserTest() {
  const {chromium}=require('playwright');
  let loads = 0;
  const server = http.createServer((req,res)=>{
    const url = req.url.split('?')[0];
    if(url === '/static/pwa.js' || url === '/static/pwa.css') {
      res.setHeader('Content-Type', url.endsWith('.js')?'application/javascript':'text/css');
      res.end(fs.readFileSync('app'+url));return;
    }
    if (url !== '/first' && url !== '/trabajo') {res.writeHead(204);res.end();return;}
    loads++;
    res.setHeader('Content-Type','text/html; charset=utf-8');
    res.end('<!doctype html><html><head><link rel="stylesheet" href="/static/pwa.css"><script src="/static/pwa.js" defer></script></head><body><form id="formulario"><input id="dato" value="[Ejemplo] Conservar"></form><section id="fotos"></section></body></html>');
  });
  await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
  const candidates=[process.env.READYPROOF_BROWSER,chromium.executablePath(),path.join(process.env.ProgramFiles||'C:/Program Files','Google/Chrome/Application/chrome.exe'),path.join(process.env.ProgramFiles||'C:/Program Files','Microsoft/Edge/Application/msedge.exe')];
  const executablePath=candidates.find(p=>p&&fs.existsSync(p));assert.ok(executablePath);
  let browser;
  try {
    browser=await chromium.launch({headless:true,executablePath});
    const context=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true});
    await context.addInitScript(()=>{
      const sw=new EventTarget();sw.controller=location.pathname==='/first'?null:{id:'anterior'};
      sw.register=async()=>({});
      Object.defineProperty(navigator,'serviceWorker',{value:sw});window.swPrueba=sw;
    });
    const page=await context.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
    await page.goto(`http://127.0.0.1:${server.address().port}/first`);
    await page.waitForFunction(()=>document.documentElement.dataset.pwa==='registrada');
    await page.evaluate(()=>{swPrueba.controller={id:'primero'};swPrueba.dispatchEvent(new Event('controllerchange'));});
    assert.equal(await page.locator('.pwa-actualizacion').count(),0,'La primera instalación no es una actualización pendiente.');
    await page.goto(`http://127.0.0.1:${server.address().port}/trabajo`);
    await page.waitForFunction(()=>document.documentElement.dataset.pwa==='registrada');
    const before=loads;
    await page.evaluate(()=>{swPrueba.controller={id:'nuevo'};swPrueba.dispatchEvent(new Event('controllerchange'));swPrueba.dispatchEvent(new Event('controllerchange'));});
    await page.getByText('Nueva versión disponible',{exact:true}).waitFor();
    assert.equal(await page.locator('.pwa-actualizacion').count(),1);
    assert.equal(loads,before,'El cambio de controlador no debe recargar.');
    assert.equal(await page.inputValue('#dato'),'[Ejemplo] Conservar');
    const update=page.getByRole('button',{name:'Actualizar readyproof'});
    await update.click();await page.getByText('Esperá a que termine de abrir la planilla antes de actualizar.').waitFor();assert.equal(loads,before);
    await page.evaluate(()=>{window.readyproofActualizacionCarga=async()=> 'Borrador pendiente de sincronizar';window.readyproofActualizacionFotos=async()=>'';});
    await update.click();await page.getByText('Borrador pendiente de sincronizar').waitFor();assert.equal(loads,before);
    await page.evaluate(()=>{window.readyproofActualizacionCarga=async()=>'';window.readyproofActualizacionFotos=async()=>{throw new Error('Almacenamiento no disponible');};});
    await update.click();await page.getByText('Almacenamiento no disponible').waitFor();assert.equal(loads,before);
    await page.evaluate(()=>{
      window.timeoutOriginal=window.setTimeout;
      window.setTimeout=(fn,ms,...args)=>timeoutOriginal(fn,ms===15000?30:ms,...args);
      window.readyproofActualizacionFotos=()=>new Promise(()=>{});
    });
    await update.click();await page.getByText(/No se pudo comprobar el guardado en 15 segundos/).waitFor();assert.equal(loads,before);
    assert.equal(await page.locator('dialog[open]').count(),0);
    await page.evaluate(()=>{
      window.setTimeout=window.timeoutOriginal;
      window.readyproofActualizacionFotos=async()=>'';
      const form=document.createElement('form');form.id='otro-formulario';
      const input=document.createElement('input');input.id='otro-dato';form.append(input);document.body.append(form);
    });
    await page.fill('#otro-dato','[Ejemplo] Edición pendiente');
    await update.click();await page.getByText('Terminá el formulario abierto y volvé a la pantalla de trabajo antes de actualizar.').waitFor();assert.equal(loads,before);
    await page.evaluate(()=>document.getElementById('otro-formulario').remove());
    await page.screenshot({path:path.join(process.env.RP_OUT,'aviso_actualizacion.png')});
    await page.evaluate(()=>{window.readyproofActualizacionFotos=async()=>'';});
    await Promise.all([page.waitForNavigation(),update.click()]);
    assert.equal(loads,before+1,'Solo el botón y las guardas aprobadas pueden recargar.');
    assert.deepEqual(errors,[]);
    console.log(JSON.stringify({primera_instalacion_sin_aviso:true,sin_recarga_automatica:true,bloqueo_guardas:true,error_almacenamiento_no_recarga:true,recarga_explicita:true,errores_javascript:errors}));
  } finally {if(browser)await browser.close();await new Promise(resolve=>server.close(resolve));}
}
(process.argv[2]==='guardas'?guards():browserTest()).catch(error=>{console.error(error);process.exitCode=1;});
