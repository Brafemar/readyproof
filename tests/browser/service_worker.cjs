const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const source=fs.readFileSync(process.env.RP_SW_SOURCE||'app/static/sw.js','utf8');
function worker({network,match,put=async()=>{}}){
  const events={};
  vm.runInNewContext(source,{
    URL,Response,
    self:{location:{origin:'http://127.0.0.1:8876'},addEventListener:(name,fn)=>events[name]=fn},
    fetch:network,caches:{open:async()=>({match,put})}
  });
  return (path)=>{
    let response;
    events.fetch({request:{url:'http://127.0.0.1:8876'+path,method:'GET'},respondWith:promise=>response=promise,
      waitUntil:()=>{throw new Error('La respuesta debe gestionar su propia escritura de caché.');}});
    return response;
  };
}
(async()=>{
  const offline=async()=>{throw new Error('sin red');};
  let fetch=worker({network:offline,match:async()=>undefined});
  let response=await fetch('/static/carga.js?revision=3');
  assert.ok(response instanceof Response,'Siempre debe devolver Response ante falta de red y caché.');
  assert.equal(response.status,503);
  fetch=worker({network:offline,match:async(request,options)=>{
    assert.equal(options.ignoreSearch,true);return new Response('copia disponible');
  }});
  assert.equal(await (await fetch('/static/carga.js?revision=3')).text(),'copia disponible');
  fetch=worker({network:async()=>new Response('red disponible'),put:async()=>{throw new Error('sin espacio');}});
  assert.equal(await (await fetch('/static/carga.js')).text(),'red disponible');
  assert.equal(fetch('/api/clientes'),undefined,'La API nunca se intercepta ni se archiva.');
  console.log('SW: cache miss 503, copia sin query, falla de escritura y API excluida: OK');
})().catch(error=>{console.error(error);process.exitCode=1;});
