"""Cierra la evidencia de etapa 5 únicamente después de las verificaciones."""
import compileall
from datetime import datetime,timezone
from hashlib import sha256
import json
from pathlib import Path
import re
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
OUT=ROOT/'out/etapa5_planillas'


def read(name):return json.loads((OUT/name).read_text(encoding='utf-8'))


def checks():
    assert all(compileall.compile_dir(str(ROOT/name),quiet=2) for name in ('app','tests','scripts','migraciones'))
    manifest=read('manifiesto_transferencia.json')
    patterns=[r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',r'AIza[0-9A-Za-z_-]{35}',
        r'gh[pousr]_[0-9A-Za-z]{30,}',r'ya29\.[0-9A-Za-z_-]{30,}',r'1//[0-9A-Za-z_-]{50,}',r'AKIA[0-9A-Z]{16}']
    findings=[]
    for relative in manifest['archivos']:
        path=ROOT/relative
        assert '.env' not in path.parts and path.suffix not in {'.db','.dump','.enc','.key','.pem'}
        if path.suffix not in {'.py','.js','.json','.html','.css','.md','.ps1','.sh','.ini','.txt'}:continue
        for number,line in enumerate(path.read_text(encoding='utf-8-sig').splitlines(),1):
            if any(re.search(pattern,line) for pattern in patterns):findings.append({'archivo':relative,'linea':number})
    result={'compileall_codigo':0,'archivos_examinados':len(manifest['archivos']),
        'patrones_secretos_detectados':findings,'env_incluidos':False}
    (OUT/'compilacion_y_revision.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    assert not findings,'Revisar candidatos sin imprimir sus valores.'
    return result


def final():
    validation=checks();applied=read('aplicar.json');tests=read('pruebas_consolidadas.json')
    backup=read('verificar.json');restored=read('pruebas_restauradas.json')
    assert applied['estado']=='etapa5_aplicada' and applied['estados']=={'YA_EXISTE':16,'IMPORTADA':63}
    assert applied['total']==79 and not applied['errores']
    assert all(row['sigla_validada'] and row['coincide_nombre_archivo'] for row in applied['planillas'])
    assert tests['estado']=='aprobada' and tests['casos_unicos']==525 and tests['fallos_pendientes']==0
    assert backup['restauracion']['schema']==applied['schema'] and not backup['restauracion']['produccion_modificada']
    assert restored['estado']=='pruebas_restauradas_aprobadas' and restored['casos']==189 and not restored['fallos']
    assert restored['base_restaurada_sin_cambios']
    visual=read('revision_visual/indice.json');assert len(visual)==63 and sum(r['paginas'] for r in visual)==97
    report={'etapa':5,'fecha_utc':datetime.now(timezone.utc).isoformat(),'estado':'verificada_en_modo_piloto',
        'importacion':applied,'pruebas':tests,'pruebas_sobre_restauracion':restored,'respaldo_y_restauracion':backup,
        'compilacion_y_revision':validation,'pdf_nuevos':visual,'sistemas':read('sistemas_finales.json'),
        'revision_publica':{'original':0,'primera_correccion':1},'modo_real_habilitado':False,
        'observaciones_unidades':[{'codigo':'SG-PEM-IFI-SCC-1','unidad_encontrada':'MPa',
            'unidad_esperada':'bar','estado':'REVISAR_CON_MARTIN',
            'decision_jorge':'Conservar el kit literal en etapa 5; no bloquea su cierre en modo piloto.',
            'confirmacion_requerida':'Martín debe confirmar MPa vs bar antes de etapa 6 y de habilitar uso real.',
            'correccion_eventual':'Migración 016, si Martín confirma que corresponde; no ejecutada.',
            'unidades_o_valores_modificados':False}],
        'etapa6_iniciada':False,'pendientes':['Confirmación normativa de unidades SCC antes de etapa 6 y uso real; demás decisiones con Martín.',
            'Asociación de las 63 nuevas a manuales reales cuando se carguen las ediciones correctas.',
            'Calendario S1–S5 y alcance ampliado: establecimientos, datos dinámicos, precargas y anulación.',
            'Autorización independiente para etapa 6 y uso real.']}
    (OUT/'etapa5_planillas.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'estado':report['estado'],'planillas':79,'sistemas':15,'tests':525,'recorridos_restaurados':189}))


if __name__=='__main__':
    if '--solo-controles' in sys.argv:print(json.dumps(checks()))
    else:final()
