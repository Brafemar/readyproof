const {chromium}=require('playwright');
const fs=require('fs'),assert=require('assert/strict');
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:process.env.READYPROOF_BROWSER||undefined,args:['--no-sandbox']});
 try{
  const page=await browser.newPage({viewport:{width:390,height:844}});
  const html=fs.readFileSync(process.argv[2],'utf8'),js=fs.readFileSync(process.argv[3],'utf8');
  const calls=[];let modo='encontrado',release;
  await page.route('http://readyproof.test/**',async route=>{
   const req=route.request(),url=new URL(req.url());
   if(url.pathname==='/admin')return route.fulfill({contentType:'text/html',body:html});
   if(url.pathname==='/static/admin.js')return route.fulfill({contentType:'application/javascript',body:js});
   if(url.pathname.startsWith('/api/')){
    calls.push({path:url.pathname,method:req.method(),cuit:url.searchParams.get('cuit')});
    const cliente={nombre:'[Ejemplo] Cliente',cuit:'20000000001',contacto:{direccion:'[Ejemplo] Calle',telefono:'0000',email:'contacto@example.invalid'}};
    if(url.pathname.endsWith('/cliente-por-cuit')){
     if(modo==='demora')await new Promise(resolve=>release=resolve);
     return route.fulfill({status:modo==='error'?502:200,contentType:'application/json',body:JSON.stringify(modo==='error'?{error:'Error de API simulado.'}:{encontrado:modo!=='ausente',cliente:modo==='ausente'?null:cliente})});
    }
    if(url.pathname.endsWith('/arca'))return route.fulfill({contentType:'application/json',body:JSON.stringify({...cliente,nombre:'[Ejemplo] Padrón'})});
    return route.fulfill({contentType:'application/json',body:'[]'});
   }
   return route.fulfill({body:''});
  });
  await page.goto('http://readyproof.test/admin');
  const boton=page.locator('#buscar-cliente-cuit'),estado=page.locator('#contabilium-cuit-estado');
  assert.equal(calls.filter(x=>x.path.includes('contabilium')).length,0);
  await page.locator('#cliente-cuit').fill('82000000000');await boton.click();
  await estado.filter({hasText:'CUIT válido'}).waitFor();
  assert.equal(calls.filter(x=>x.path.endsWith('/cliente-por-cuit')).length,0);
  await page.locator('#cliente-cuit').fill('20-00000000-1');
  await page.locator('#cliente-telefono').fill('[Ejemplo] Manual');await boton.click();
  await estado.filter({hasText:'Se completaron'}).waitFor();
  assert.equal(await page.locator('#cliente-nombre').inputValue(),'[Ejemplo] Cliente');
  assert.equal(await page.locator('#cliente-email').inputValue(),'contacto@example.invalid');
  assert.equal(await page.locator('#cliente-telefono').inputValue(),'[Ejemplo] Manual');
  assert.equal(calls.find(x=>x.path.endsWith('/cliente-por-cuit')).cuit,'20000000001');
  modo='ausente';await page.locator('#cliente-nuevo').click();await page.locator('#cliente-cuit').fill('20000000001');await boton.click();
  await estado.filter({hasText:'No se encontró'}).waitFor();
  assert.equal(calls.filter(x=>x.path.endsWith('/arca')).length,0);
  await page.locator('#consultar-arca').click();await page.locator('#arca-estado').filter({hasText:'Revisalos'}).waitFor();
  assert.equal(await page.locator('#cliente-nombre').inputValue(),'[Ejemplo] Padrón');
  assert.equal(await page.locator('#cliente-direccion').inputValue(),'[Ejemplo] Calle');
  assert.equal(await page.locator('#cliente-email').inputValue(),'');
  modo='error';await boton.click();await estado.filter({hasText:'Error de API'}).waitFor();
  assert.equal(await page.locator('#cliente-nombre').inputValue(),'[Ejemplo] Padrón');
  modo='demora';await page.locator('#cliente-nuevo').click();await page.locator('#cliente-cuit').fill('20000000001');await boton.click();
  await page.waitForFunction(()=>document.getElementById('buscar-cliente-cuit').disabled);
  await page.locator('#cliente-cuit').fill('27000000006');release();await boton.waitFor({state:'visible'});
  await page.waitForFunction(()=>!document.getElementById('buscar-cliente-cuit').disabled);
  assert.equal(await page.locator('#cliente-nombre').inputValue(),'');
  assert.equal(calls.filter(x=>x.method!=='GET').length,0);
  console.log(JSON.stringify({sin_guardado_automatico:true,no_sobrescribe:true,arca_manual:true,respuesta_vieja_descartada:true}));
 }finally{await browser.close();}
})().catch(error=>{console.error(error);process.exit(1)});
