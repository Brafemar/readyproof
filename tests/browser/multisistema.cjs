const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const {chromium}=require('playwright');
(async()=>{
 const candidates=[process.env.READYPROOF_BROWSER,chromium.executablePath(),path.join(process.env.ProgramFiles||'C:/Program Files','Google/Chrome/Application/chrome.exe'),path.join(process.env['ProgramFiles(x86)']||'C:/Program Files (x86)','Microsoft/Edge/Application/msedge.exe')];
 const browser=await chromium.launch({headless:true,executablePath:candidates.find(p=>p&&fs.existsSync(p))});
 const context=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true,locale:'es-AR'});
 const page=await context.newPage(),errors=[];page.on('pageerror',error=>errors.push(error.message));
 const base=process.env.RP_URL;let forms=0;
 try{
  await page.goto(base+'/login');await page.locator('#login').fill(process.env.RP_LOGIN);await page.locator('#clave').fill(process.env.RP_PASSWORD);
  await Promise.all([page.waitForURL(base+'/'),page.getByRole('button',{name:'Ingresar',exact:true}).click()]);
  await page.waitForFunction(()=>document.getElementById('save-status').textContent.includes('y en el servidor'));
  const client=(await (await context.request.get(base+'/api/clientes')).json())[0];
  const systems=await (await context.request.get(base+'/api/clientes/'+client.id+'/sistemas')).json();
  const sheets=await (await context.request.get(base+'/api/planillas')).json();
  assert.equal(systems.length,15);assert.equal(sheets.length,79);
  for(const type of ['SAA','SDI','SBC','SAL','SAP','SCC','SDC','SEP','SGE','SHC','SIM','SRA','SRE','SSA','STM']){
   const system=systems.find(s=>s.tipo===type);await page.selectOption('#sistema',system.id);
   for(const sheet of sheets.filter(p=>p.sistema_tipo===type)){
    await page.selectOption('#planilla',sheet.id);
    await page.waitForFunction(code=>document.getElementById('codigo-planilla').textContent===code,sheet.codigo);
    await page.waitForFunction(()=>document.getElementById('save-status').textContent.includes('y en el servidor'));
    await page.locator('#completar-ejemplo').click();
    await page.waitForFunction(()=>document.getElementById('save-status').textContent.includes('y en el servidor'));
    const schema=(await (await context.request.get(base+'/api/planillas/'+sheet.id)).json()).definicion;
    const expected=Object.values(schema.bloques).reduce((sum,fields)=>sum+Object.keys(fields).length,0);
    assert.equal(await page.locator('#bloques input,#bloques select').count(),expected);
    assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth),true,sheet.codigo);
    if(sheet.codigo==='SG-PEM-IFI-SDI-2'){
      assert.equal(await page.locator('.sheet-table').count(),3);
      await page.screenshot({path:path.join(process.env.RP_OUT,'SDI-2_movil.png')});
    }
    forms++;
   }
  }
  assert.deepEqual(errors,[]);
  fs.writeFileSync(path.join(process.env.RP_OUT,'resultado.json'),JSON.stringify({formularios:forms,sistemas:15,errores:errors},null,2));
 }catch(error){await page.screenshot({path:path.join(process.env.RP_OUT,'error.png'),fullPage:true});console.error(await page.evaluate(()=>({ancho:innerWidth,total:document.documentElement.scrollWidth,fuera:[...document.querySelectorAll('main,.card,.field-grid,.sheet-table-scroll,.page-heading')].map(e=>({clase:e.className,ancho:e.getBoundingClientRect().width,derecha:e.getBoundingClientRect().right}))})));throw error;}finally{await browser.close();}
})().catch(error=>{console.error(error);process.exitCode=1;});
