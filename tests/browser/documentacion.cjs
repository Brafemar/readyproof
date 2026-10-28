const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const {chromium}=require('playwright');
(async()=>{
  const candidates=[process.env.READYPROOF_BROWSER,chromium.executablePath(),path.join(process.env.ProgramFiles||'C:/Program Files','Google/Chrome/Application/chrome.exe'),path.join(process.env['ProgramFiles(x86)']||'C:/Program Files (x86)','Microsoft/Edge/Application/msedge.exe')];
  const browser=await chromium.launch({headless:true,executablePath:candidates.find(p=>p&&fs.existsSync(p))});
  const context=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true,locale:'es-AR'});
  const page=await context.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
  const base=process.env.RP_URL;
  try{
    await page.goto(base+'/login');await page.locator('#login').fill(process.env.RP_LOGIN);await page.locator('#clave').fill(process.env.RP_PASSWORD);
    await Promise.all([page.waitForURL(base+'/'),page.getByRole('button',{name:'Ingresar',exact:true}).click()]);
    await page.goto(base+'/cuenta');
    const button=page.getByRole('button',{name:'Enviar documentación por correo',exact:true});
    assert.equal(await button.isEnabled(),true);
    await page.getByLabel('Tu correo',{exact:true}).fill('tecnico@example.invalid');
    await page.getByRole('button',{name:'Guardar correo',exact:true}).click();
    await page.waitForFunction(()=>document.getElementById('documentacion-estado').textContent.includes('Correo guardado:'));
    await button.click();
    assert.equal(await page.locator('#documentacion-destinatario').inputValue(),'tecnico@example.invalid');
    await page.locator('#documentacion-destinatario').fill('destino@example.invalid');
    await page.locator('#confirmar-documentacion').dblclick();
    await page.waitForFunction(()=>document.getElementById('documentacion-estado').textContent.includes('archivada, sin envío real'));
    await page.locator('#cerrar-documentacion').click();
    await page.reload();assert.equal(await page.getByLabel('Tu correo',{exact:true}).inputValue(),'tecnico@example.invalid');
    assert.equal(await page.locator('#actual').inputValue(),'');
    assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth),true);
    assert.deepEqual(errors,[]);
    await page.screenshot({path:path.join(process.env.RP_OUT,'mi_cuenta_android.png'),fullPage:true});
    fs.writeFileSync(path.join(process.env.RP_OUT,'resultado.json'),JSON.stringify({boton:true,correo_guardado:true,doble_clic_sin_duplicado:true,movil:true,errores:errors},null,2));
  }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
