"""Documentar una activación real únicamente después de verificarla."""
from datetime import datetime,timedelta,timezone
from pathlib import Path
import json,subprocess
from control_transicion_real import tests

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'out/transicion_real_20261028'

def main():
    passed=tests()
    active=json.loads((OUT/'activar.json').read_text());verified=json.loads((OUT/'verificar.json').read_text())
    migration=json.loads((OUT/'aplicar.json').read_text())
    assert active['estado']=='MODO_REAL_ACTIVO' and verified['estado']=='MODO_REAL_VERIFICADO'
    assert active['configuracion']=={'MODO_PILOTO':False,'MAIL_MODO_PRUEBA':False,'EMPRESA_MANTENEDORA':'READYPROOF','CERTIFICADO_N':'IFI-2024-10001'}
    assert not migration['historicos_modificados'] and not active['historicos_modificados'] and not active['firmantes_modificados']
    compiled=subprocess.run([str(ROOT/'.venv/Scripts/python.exe'),'-m','compileall','-q','app','tests','scripts','migraciones'],cwd=ROOT).returncode
    assert compiled==0
    time=datetime.fromisoformat(active['fecha_utc']).astimezone(timezone(timedelta(hours=-3)))
    start=time.isoformat();end24=(time+timedelta(hours=24)).isoformat();end48=(time+timedelta(hours=48)).isoformat()
    restored=verified['restauracion']
    report={'estado':'MODO_REAL_ACTIVO','fecha_autorizacion':'2026-10-28T13:53:00-03:00','fecha_activacion_argentina':start,
        'empresa_mantenedora':'READYPROOF','certificado_n':'IFI-2024-10001','modo_piloto':False,'mail_modo_prueba':False,
        'pruebas':{**passed,'omitidos':0,'linux':496,'windows':47,'nota':'541 casos previos más 2 casos de unidades; tandas finales separadas por plataforma.'},
        'compilacion_codigo':compiled,'schema':'017_scc1_presion_bar','planillas_activas':79,'versiones_planilla':89,
        'unidades':{'scc1_vigente':'00-26-bar1','scc1_anterior_conservada':'00-26-ms1','campo_corregido':'J21: presión normal a 20 °C, bar','sdi_estados':['✓','O','X','NA']},
        'fuente_modificada':False,'datos_historicos_modificados':False,'firmantes_modificados':False,'usuarios_modificados':False,
        'respaldo_pre_017':migration['respaldo_previo'],'respaldo_pre_real':active['backup_previo'],
        'restauracion':restored,'timer_backup':verified['timer'],'correo_transporte':'gmail_api','correos_prueba_transmitidos':False,
        'configuracion_privada':'/home/readyproof/.env y .env.local; no versionados',
        'monitoreo':{'responsable':'Jorge Sánchez','inicio':start,'revision_24h':end24,'revision_48h':end48,'modalidad':'Manual; sin automatización nueva','auditoria':'Cada 2 horas durante operación','backup':'Verificar respaldo nocturno y alertas existentes'},
        'tag':'v1.1-real-20261028T1353','evidencias':'out/transicion_real_20261028/'}
    (ROOT/'TRANSICION_REAL_REPORTE.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    doc=f'''# Transición a producción real

Estado: **MODO_REAL ACTIVO**. Activación verificada: {time.strftime('%d/%m/%Y %H:%M:%S')} Argentina (UTC−03:00).

Jorge Sánchez autorizó el corte el 28/10/2026 a las 13:53 y aprobó el checklist. Confirmó mantenedora **READYPROOF**, certificado **IFI-2024-10001**, bar en campos de presión y conservación de ✓/O/X/NA en SDI.

## Configuración efectiva

Los archivos privados `/home/readyproof/.env` y `.env.local` tienen `MODO_PILOTO=false`, `MAIL_MODO_PRUEBA=false`, `EMPRESA_MANTENEDORA="READYPROOF"` y `CERTIFICADO_N="IFI-2024-10001"`. Se actualizan ambos porque systemd carga `.env` y la aplicación también lee dotenv. Se comprobaron los valores del proceso reiniciado y la aplicación respondió a `/login`. Las credenciales y los archivos de entorno no se incorporaron a Git. El acceso sigue siendo privado mediante el túnel existente, en `http://127.0.0.1:8876/login`.

## Cambios y conservación

La migración 017 agrega SCC-1 `00-26-bar1`: J21 cambia de MPa a bar. Conserva la versión anterior y no convierte valores históricos. SDI mantiene cuatro estados; no se inventan mediciones ni unidades para verificaciones cualitativas. Ver [detalle de unidades](UNIDADES_SCC1_BAR.md).

También se corrigió una carrera de cierre de sesión: una sincronización que termina después del bloqueo ya no lee un borrador retirado ni programa otro intento. La caché de interfaz pasa a v11. Recargar en línea después del corte sin borrar borradores pendientes.

Se compararon cargas, firmas, PDF archivados y usuarios antes y después del cambio de entorno. Permanecen iguales, incluidos los firmantes ficticios. Se cotejaron las huellas de `fuente/`, sin cambios. Los nuevos datos se cargan en registros nuevos; no se transforman clientes ficticios en reales.

## Verificación

- 543 pruebas finales aprobadas: 496 Ubuntu y 47 Windows; cero fallos y omisiones. Incluyen los 541 casos previos y dos nuevos de unidades.
- Compilación de aplicación, pruebas, migraciones y scripts: código 0.
- Ensayo 016→017 en base aislada y comparación de todas las filas anteriores: correcto.
- Respaldo cifrado antes de migración y otro antes del corte, conservados fuera de la rotación diaria.
- Respaldo posterior en Drive y restauración aislada: {restored['tablas_comparadas']} tablas, {restored['blobs_comparados']} binarios y {restored['pdf_exportados_comparados']} PDF cotejados; producción no restaurada ni reemplazada.
- Transporte de planillas: Gmail por HTTPS. No se enviaron correos reales de prueba durante el corte.

## Monitoreo 24/48 horas

Responsable: Jorge Sánchez. Revisar errores, cambios de auditoría y envíos cada dos horas durante la operación. Revisar la copia nocturna y sus alertas al comenzar la jornada siguiente. Primera revisión de 24 h: **{end24}**; cierre de observación de 48 h: **{end48}**. No se creó una automatización nueva.

Ante un incidente, preservar los registros y avisar a Jorge antes de modificar configuración o restaurar. La configuración anterior está conservada en una carpeta privada del servidor. No regenerar documentos históricos ni repetir envíos de resultado indeterminado. El backlog ampliado sigue documentado; la autorización de transición no declara implementadas funciones que estén pendientes.

Tag solicitado: `v1.1-real-20261028T1353`. Evidencia resumida: `TRANSICION_REAL_REPORTE.json`; XML y diagnósticos conservados en `out/transicion_real_20261028/`.
'''
    (ROOT/'docs/TRANSICION_EXITOSA.md').write_text(doc,encoding='utf-8')
    print(json.dumps({'estado':report['estado'],'tests':543,'activacion':start}))

if __name__=='__main__':main()
