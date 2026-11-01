const assert=require("node:assert/strict");
const fs=require("node:fs"),path=require("node:path"),vm=require("node:vm");
if(process.argv[2]==="validar"){
  const input=JSON.parse(process.env.RP_CASO),elements=new Map();
  const window={addEventListener(){},readyproofSession:new Promise(()=>{})};
  const document={getElementById(id){if(!elements.has(id))elements.set(id,{});return elements.get(id);}};
  vm.runInNewContext(fs.readFileSync("app/static/fotos.js","utf8"),{window,document,console});
  try{
    const result=input.numerar?window.readyproofFotos.numerarMarcas(input.marcas):window.readyproofFotos.validarMarcas(input.marcas);
    process.stdout.write(JSON.stringify({ok:true,marcas:result}));
  }catch(error){process.stdout.write(JSON.stringify({ok:false,error:error.message}));}
}else{
  const {chromium}=require("playwright");
  (async()=>{
    const candidates=[process.env.READYPROOF_BROWSER,chromium.executablePath(),path.join(process.env.ProgramFiles||"C:/Program Files","Google/Chrome/Application/chrome.exe"),path.join(process.env.ProgramFiles||"C:/Program Files","Microsoft/Edge/Application/msedge.exe")];
    const executablePath=candidates.find(p=>p&&fs.existsSync(p));assert.ok(executablePath,"Falta navegador local para la prueba.");
    const mobile=process.env.RP_MOVIL==="1";
    const browser=await chromium.launch({headless:true,executablePath});
    const context=await browser.newContext({viewport:mobile?{width:390,height:844}:{width:1200,height:900},isMobile:mobile,hasTouch:mobile,locale:"es-AR"});
    const page=await context.newPage(),errors=[];page.on("pageerror",error=>errors.push(error.message));page.setDefaultTimeout(15000);
    const rows=()=>page.locator("#foto-anotaciones li");
    async function foto(x,y){await page.locator("#foto-editor-imagen").scrollIntoViewIfNeeded();const rect=await page.locator("#foto-editor-imagen").boundingBox();assert.ok(rect&&rect.width>0);const cx=rect.x+rect.width*x,cy=rect.y+rect.height*y;if(mobile)await page.touchscreen.tap(cx,cy);else await page.mouse.click(cx,cy);}
    async function saved(){await page.click("#foto-guardar-marcas");await page.waitForFunction(()=>document.getElementById("foto-marcas-estado").textContent.includes("Marcas guardadas"));}
    async function record(){return page.evaluate(()=>new Promise((resolve,reject)=>{const r=indexedDB.open("readyproof-fotos-c3-usuario",2);r.onsuccess=()=>{const db=r.result,q=db.transaction("anotaciones").objectStore("anotaciones").getAll();q.onsuccess=()=>{db.close();resolve(q.result[0]);};q.onerror=()=>{db.close();reject(q.error);};};}));}
    try{
      await page.goto(process.env.RP_URL,{waitUntil:"networkidle"});
      await page.waitForFunction(()=>!document.getElementById("foto-archivo").disabled);
      const image=await page.evaluate(()=>{const c=document.createElement("canvas");c.width=800;c.height=600;const g=c.getContext("2d");g.fillStyle="#e0e7eb";g.fillRect(0,0,800,600);g.fillStyle="#111";g.font="30px sans-serif";g.fillText("[Ejemplo] Foto de campo",60,70);return c.toDataURL("image/jpeg").split(",")[1];});
      await page.locator("#foto-archivo").setInputFiles({name:"foto.jpg",mimeType:"image/jpeg",buffer:Buffer.from(image,"base64")});
      await page.waitForFunction(()=>document.getElementById("fotos-lista").textContent.includes("Guardada"));
      await page.getByRole("button",{name:"Ver y marcar",exact:true}).click();
      await page.waitForFunction(()=>document.getElementById("foto-editor-imagen").naturalWidth===800);
      await foto(.25,.3);assert.equal(await rows().count(),1);
      await rows().nth(0).locator("select").selectOption("O");
      await page.click("#foto-guardar-marcas");await page.waitForFunction(()=>document.getElementById("foto-marcas-estado").textContent.includes("Completá el texto"));
      await rows().nth(0).locator("textarea").fill("[Ejemplo] Revisar filtro <img src=x onerror=alert(1)>");
      assert.equal(await rows().nth(0).locator("textarea").getAttribute("maxlength"),"140");
      await foto(.75,.7);await rows().nth(1).locator("select").selectOption("NA");await saved();
      await page.getByRole("button",{name:"Editar marca 1",exact:true}).click();assert.equal(await rows().count(),2);assert.equal(await rows().nth(0).getAttribute("class"),"seleccionada");
      await page.click("#foto-agregar-marca");await rows().nth(2).locator("select").selectOption("✓");await saved();
      await page.getByRole("button",{name:"Borrar marca 2",exact:true}).click();await saved();
      assert.deepEqual(await page.locator("#foto-marcas button").allTextContents(),["1","2"]);
      let data=await record();assert.deepEqual(data.marcas.map(m=>m.numero),[1,2]);assert.deepEqual(data.marcas.map(m=>m.codigo),["O","✓"]);
      assert.ok(Math.abs(data.marcas[0].x-.25)<.015);assert.ok(Math.abs(data.marcas[0].y-.3)<.015);assert.equal(data.marcas[1].x,.5);assert.equal(data.marcas[1].y,.5);
      assert.equal(await page.locator("#foto-anotaciones img").count(),0);
      await page.reload({waitUntil:"networkidle"});await page.getByRole("button",{name:"Ver y marcar",exact:true}).click();await page.waitForFunction(()=>document.querySelectorAll("#foto-anotaciones li").length===2);
      await rows().nth(0).locator("textarea").fill("");
      await page.waitForFunction(()=>new Promise(resolve=>{const r=indexedDB.open("readyproof-fotos-c3-usuario",2);r.onsuccess=()=>{const db=r.result,q=db.transaction("anotaciones").objectStore("anotaciones").getAll();q.onsuccess=()=>{db.close();resolve(q.result[0]?.borradorMarcas?.[0]?.texto==="");};};}));
      await page.reload({waitUntil:"networkidle"});await page.getByRole("button",{name:"Ver y marcar",exact:true}).click();await page.waitForFunction(()=>document.querySelectorAll("#foto-anotaciones li").length===2);
      assert.equal(await rows().nth(0).locator("textarea").inputValue(),"");
      await context.setOffline(true);await rows().nth(0).locator("textarea").fill("[Ejemplo] Texto corregido sin conexión");await saved();await context.setOffline(false);
      data=await record();assert.equal(data.marcas[0].texto,"[Ejemplo] Texto corregido sin conexión");
      await page.evaluate(()=>window.c3Contexto(true));assert.equal(await page.locator("#foto-agregar-marca").isDisabled(),true);assert.equal(await rows().nth(0).locator("select").isDisabled(),true);assert.equal(await rows().nth(0).locator("textarea").isDisabled(),true);
      await foto(.1,.8);assert.equal(await rows().count(),2);
      assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
      await page.locator("#fotos").screenshot({path:path.join(process.env.RP_OUT,"marcado.png")});
      const other=await context.newPage();await other.goto(process.env.RP_URL+"?usuario=c3-otro",{waitUntil:"networkidle"});await other.getByRole("button",{name:"Ver y marcar",exact:true}).click();await other.waitForFunction(()=>document.getElementById("foto-editor-imagen").naturalWidth===800&&document.querySelectorAll("#foto-anotaciones li").length===2);assert.equal(await other.locator("#foto-editor").isVisible(),true);await other.close();
      await page.evaluate(()=>{window.dispatchEvent(new CustomEvent("readyproof-lock"));window.dispatchEvent(new CustomEvent("readyproof-lock"));});
      assert.equal(await page.locator("#foto-editor").isHidden(),true);assert.equal(await page.locator("#foto-editor-imagen").getAttribute("src"),null);assert.equal(await rows().count(),0);assert.deepEqual(errors,[]);
      fs.writeFileSync(path.join(process.env.RP_OUT,"resultado.json"),JSON.stringify({movil:mobile,marcas:2,numeracion:true,coordenadas:true,seleccion_sin_duplicados:true,borrado_renumera:true,validacion_O_vacio:true,borrador_recargado:true,guardado_offline:true,solo_lectura:true,lectura_autorizada_otra_cuenta:true,limpieza_al_cerrar_sesion:true,sin_desborde:true,errores:errors},null,2));
    }finally{await context.close();await browser.close();}
  })().catch(error=>{console.error(error);process.exitCode=1;});
}
