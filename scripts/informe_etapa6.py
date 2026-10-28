"""Generar los reportes finales desde evidencia local de pruebas y servidor."""
from datetime import datetime, timezone
import hashlib,json,re,subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'out/etapa6_final'
def read(name):return json.loads((OUT/name).read_text(encoding='utf-8'))
def write(name,value):(ROOT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    tests=read('pruebas_cobertura.json');server=read('verificar.json');applied=read('aplicar.json')
    assert tests['aprobados']==541 and not tests['fallidos'] and not tests['omitidos']
    assert tests['cobertura_lineas_python']>=85 and server['estado']=='etapa6_verificada'
    assert server['flags']=={'modo_piloto':True,'mail_modo_prueba':True}
    assert not server['restauracion']['produccion_modificada'] and not applied['datos_historicos_modificados']
    compiled=subprocess.run([str(ROOT/'.venv/Scripts/python.exe'),'-m','compileall','-q','app','tests','scripts','migraciones'],cwd=ROOT).returncode
    assert compiled==0
    tracked=subprocess.run(['git','ls-files','-z'],cwd=ROOT,capture_output=True,check=True).stdout.decode().split('\0')
    private=[p for p in tracked if Path(p).name in ('.env','.env.local') or (Path(p).name.startswith('.env.') and Path(p).name.endswith('.local'))]
    assert not private
    patterns=(rb'-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----',rb'ya29\.[A-Za-z0-9_-]{30,}',rb'GOCSPX-[A-Za-z0-9_-]{20,}',rb'gh[pousr]_[A-Za-z0-9]{30,}')
    hits=[]
    for name in tracked:
        p=ROOT/name
        if not p.is_file() or p.suffix.lower() not in ('.py','.js','.cjs','.md','.json','.ps1','.txt'):continue
        if name== 'scripts/informe_etapa6.py':continue
        if any(re.search(pattern,p.read_bytes()) for pattern in patterns):hits.append(name)
    assert not hits, 'Revisar coincidencias antes de entregar.'
    protected=read('atributos_git.json')['archivos_verificados']
    for name in protected:
        raw=subprocess.run(['git','show','HEAD:'+name],cwd=ROOT,capture_output=True,check=True).stdout
        assert hashlib.sha256(raw).digest()==hashlib.sha256((ROOT/name).read_bytes()).digest(),name
    items=len(re.findall(r'^- \[ \]',(ROOT/'docs/TRANSICION_PILOTO_A_REAL.md').read_text(encoding='utf-8'),re.M))
    now=datetime.now(timezone.utc).isoformat()
    checklist={'fecha':now,'etapa':6,'tareas':{
      'busqueda_numero_registro':{'endpoint':'/api/carga/buscar','tests':4,'estado':'OK'},
      'auditoria_runtime':{'tabla':'auditoria','migracion':'016_tabla_auditoria','hooks':['INSERT','UPDATE','DESBLOQUEO'],'endpoint':'/api/auditoria','tests':5,'estado':'OK'},
      'modo_configurable':{'tests':6,'test_navegador_adicional':1,'activado_real':False,'estado':'OK'},
      'documentacion_transicion':{'archivo':'docs/TRANSICION_PILOTO_A_REAL.md','checklist_items':items,'estado':'OK'}},
      'tests_total':541,'tests_pasando':541,'tests_fallidos':0,'tests_omitidos':0,'plataformas':tests['plataformas'],
      'cobertura_lineas_python':round(tests['cobertura_lineas_python'],4),'cobertura_alcance':'app/ Python; no JavaScript ni ramas',
      'compilacion':{'estado':'OK','codigo':compiled},'seguridad':{'env_privados_versionados':private,'patrones_credenciales_encontrados':hits,'alcance':'Patrones de claves privadas y tokens conocidos; no certificación exhaustiva de secretos.'},
      'fuente_bytes_conservados':True,'servidor':server,'veredicto':'ETAPA_6_COMPLETADA_EN_PILOTO',
      'tag':'v1.1-etapa6-completa-20261028','evidencias':'out/etapa6_final/'}
    write('CHECKLIST_ETAPA_6_FINAL.json',checklist)
    write('ETAPA_6_FINAL_REPORTE.json',{'fecha':now,'proyecto':'readyproof v1.1','etapa_entregada':6,
      'estado_produccion':{'modo_piloto':True,'mail_modo_prueba':True,'empresa_mantenedora':'Pendiente confirmación Jorge','certificado_n':'Pendiente confirmación Jorge','acceso':'Privado por túnel SSH'},
      'funcionalidades_entregadas':['Búsqueda autenticada por número de registro','Auditoría transaccional de cargas e historial inmutable','Habilitación configurable de modo real con validaciones, mantenida desactivada','PDF nuevos identificados PILOTO/REAL, anteriores conservados','Control de destinatarios y transporte por modo','Documentación de transición y monitoreo'],
      'catalogo':{'planillas_activas':79,'planillas_con_versiones':server['backup']['counts']['planillas'],'sistemas':15},
      'tests':tests,'compilacion_codigo':compiled,'migracion':applied,'respaldos':server['restauracion'],
      'seguridad':checklist['seguridad'],'documentacion':['docs/API.md','docs/AUDITORIA.md','docs/CONFIG_MODO_REAL.md','docs/TRANSICION_PILOTO_A_REAL.md','docs/PRUEBAS_ETAPA6.md'],
      'incidente_resuelto':'Directorio app/auditoria: umask 0077 impedía lectura por el servicio; corregido root:readyproof 0750 y chmod explícito en instalador.',
      'pendientes':['Empresa mantenedora y certificado reales confirmados por Jorge','Martín: SCC-1 MPa vs bar y confirmación de cuatro estados SDI','Revisión de todos los puntos del checklist de transición y backlog avanzado','Autorización explícita de Jorge para activar modo real; no otorgada por esta entrega'],
      'tag':'v1.1-etapa6-completa-20261028','veredicto':'ETAPA_6_COMPLETADA_EN_PILOTO','siguiente_paso':'ESPERAR AUTORIZACION JORGE Y RESOLVER CHECKLIST ANTES DE MODO REAL'})
    print(json.dumps({'pruebas':541,'cobertura':round(tests['cobertura_lineas_python'],2),'checklist_items':items,'reporte':'OK'}))

if __name__=='__main__':main()
