const {chromium}=require('playwright');
const fs=require('fs');
const assert=require('assert/strict');
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:process.env.READYPROOF_BROWSER||undefined,args:['--no-sandbox']});
 try {
 const page=await browser.newPage({viewport:{width:390,height:844}});
 const html=fs.readFileSync(process.argv[2],'utf8'), js=fs.readFileSync(process.argv[3],'utf8');
 const requests=[];let failure=false;
 await page.route('http://readyproof.test/**',async route=>{
  const request=route.request(),url=new URL(request.url());
  if(url.pathname==='/admin')return route.fulfill({contentType:'text/html',body:html});
  if(url.pathname==='/static/admin.js')return route.fulfill({contentType:'application/javascript',body:js});
  if(url.pathname.startsWith('/api/')){
   requests.push({path:url.pathname,search:url.search,method:request.method()});
   if(url.pathname==='/api/admin/contabilium/arca')return route.fulfill({status:failure?503:200,contentType:'application/json',body:JSON.stringify(failure?{error:'Falta configurar el correo API y la API Key de Contabilium en el servidor.'}:{nombre:'[Ejemplo] Padrón',cuit:'20000000001',contacto:{direccion:'[Ejemplo] Calle',telefono:'0000',email:'ejemplo@example.invalid'}})});
   return route.fulfill({contentType:'application/json',body:'[]'});
  }
  return route.fulfill({body:''});
 });
 await page.goto('http://readyproof.test/admin');
 await page.locator('#cliente-cuit').fill('20-00000000-1');
 await page.locator('#consultar-arca').click();
 await page.waitForFunction(()=>document.getElementById('arca-estado').textContent.includes('Revisalos'));
 assert.equal(await page.locator('#cliente-nombre').inputValue(),'[Ejemplo] Padrón');
 assert.equal(await page.locator('#cliente-direccion').inputValue(),'[Ejemplo] Calle');
 const calls=requests.filter(x=>x.path==='/api/admin/contabilium/arca');
 assert.equal(calls.length,1);assert.equal(calls[0].search,'?cuit=20-00000000-1');assert.equal(calls[0].method,'GET');
 failure=true;await page.locator('#consultar-arca').click();
 await page.waitForFunction(()=>document.getElementById('arca-estado').textContent.includes('Falta configurar'));
 assert.equal(await page.locator('#consultar-arca').isEnabled(),true);
 assert.equal(requests.filter(x=>x.method!=='GET').length,0);
 console.log(JSON.stringify({ruta_correcta:true,sin_guardado_automatico:true,error_visible:true}));
 } finally {await browser.close();}
})().catch(error=>{console.error(error);process.exit(1)});
