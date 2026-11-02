"""Paginación de copias de Excel oficiales, con ajuste de impresión opcional."""
from contextlib import contextmanager
from datetime import datetime, timezone
from hashlib import sha256
import os
import shutil
import time
import warnings
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from io import BytesIO
from zipfile import ZipFile
from lxml import etree

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from pypdf import PdfReader, PdfWriter
from app.planillas.catalogo_completo import definiciones_restantes
from app.planillas.importacion_excel import leer_origen
from app.planillas.pdf import localizar_libreoffice


def _soffice_vivos():
    if os.name != 'nt':
        return []
    command = r"""$ErrorActionPreference='Stop'; @(Get-CimInstance Win32_Process | Where-Object { $_.Name -in @('soffice.exe','soffice.bin') } | Select-Object ProcessId,ExecutablePath,CommandLine,@{Name='CreadoUTC';Expression={$_.CreationDate.ToUniversalTime().ToString('o')}}) | ConvertTo-Json -Compress"""
    result = subprocess.run(['powershell.exe', '-NoProfile', '-NonInteractive', '-Command', command], capture_output=True, text=True, encoding='utf-8', timeout=15)
    if result.returncode:
        raise RuntimeError('No se pudo consultar LibreOffice; no se cerró ningún proceso sin identificar.')
    rows = json.loads(result.stdout.strip() or '[]')
    return rows if isinstance(rows, list) else [rows]


def _son_propios(rows, preparation):
    executable = preparation.get('ejecutable')
    if not executable:
        return []
    parent = str(Path(executable).resolve().parent).casefold()
    before = set(preparation.get('pids_preexistentes', []))
    return [row for row in rows
            if row.get('ProcessId') not in before
            and Path(row.get('ExecutablePath') or '').name.casefold() in {'soffice.exe', 'soffice.bin'}
            and str(Path(row['ExecutablePath']).resolve().parent).casefold() == parent
            and any(profile.casefold() in (row.get('CommandLine') or '').casefold() for profile in preparation['perfiles'])]


def _cerrar_por_identidad(row):
    command = r"""$ErrorActionPreference='Stop'; $expected=$env:READYPROOF_SOFFICE_PROPIO | ConvertFrom-Json; $owned=Get-Process -Id $expected.ProcessId -ErrorAction SilentlyContinue; if(!$owned){exit 0}; $owned.Handle | Out-Null; $current=Get-CimInstance Win32_Process -Filter ('ProcessId='+$expected.ProcessId); if(!$current){exit 0}; if($current.ExecutablePath -ine $expected.ExecutablePath -or $current.CommandLine -cne $expected.CommandLine -or $current.CreationDate.ToUniversalTime().ToString('o') -cne $expected.CreadoUTC){throw 'Cambió la identidad del proceso: no se cierra.'}; if(!$owned.HasExited){$owned.CloseMainWindow() | Out-Null; if(!$owned.WaitForExit(300)){$owned.Kill(); if(!$owned.WaitForExit(5000)){throw 'No terminó el proceso propio de referencias.'}}}"""
    env = dict(os.environ, READYPROOF_SOFFICE_PROPIO=json.dumps(row))
    result = subprocess.run(['powershell.exe', '-NoProfile', '-NonInteractive', '-Command', command], env=env, capture_output=True, timeout=12)
    if result.returncode:
        raise RuntimeError('No se pudo cerrar el PID propio de referencias '+str(row['ProcessId']))


def _huellas_pdf(work):
    result = {}
    for path in sorted((work/'pdf').glob('*.pdf')):
        reader = PdfReader(path)
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        memory = BytesIO()
        writer.write(memory)
        result[path.name] = {'sha256': sha256(path.read_bytes()).hexdigest(),
                             'sha256_paginas_sin_metadatos': sha256(memory.getvalue()).hexdigest(),
                             'paginas': len(reader.pages), 'bytes': path.stat().st_size}
    return result


def _ejecutar_lote(args, preparation):
    with subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
        preparation['iniciados'].append({'pid': process.pid, 'ejecutable': str(args[0]),
                                         'inicio_utc': datetime.now(timezone.utc).isoformat()})
        try:
            stdout, stderr = process.communicate(timeout=300)
        except BaseException:
            process.kill()
            process.communicate()
            raise
        return subprocess.CompletedProcess(args, process.returncode, stdout, stderr)


@contextmanager
def _referencias_temporales(temporal):
    # Las cuatro primeras limpiezas son estrictas; la quinta tolera residuos solo aquí.
    temporary = TemporaryDirectory(prefix='r-', dir=temporal, ignore_cleanup_errors=True)
    work = Path(temporary.name)
    preparation = {'directorio': str(work), 'perfiles': [], 'iniciados': [],
                   'cierres': [], 'errores_cierre': [], 'intentos_limpieza': [],
                   'ignore_cleanup_errors': True, 'fallback_usado': False}
    try:
        preparation['pids_preexistentes'] = [row['ProcessId'] for row in _soffice_vivos()]
    except Exception as error:
        preparation['pids_preexistentes'] = []
        preparation['errores_cierre'].append(str(error))
    try:
        yield preparation
    finally:
        try:
            preparation['hashes_pdf'] = _huellas_pdf(work)
        except Exception as error:
            preparation['error_huellas_pdf'] = str(error)
        try:
            rows = _son_propios(_soffice_vivos(), preparation)
            preparation['vivos_propios_antes_limpieza'] = rows
            for row in rows:
                try:
                    _cerrar_por_identidad(row)
                    preparation['cierres'].append(row)
                except Exception as error:
                    preparation['errores_cierre'].append(str(error))
        except Exception as error:
            preparation['errores_cierre'].append(str(error))
        # La ruta proviene de TemporaryDirectory y se verifica antes de cualquier borrado.
        assert work.resolve().parent == Path(temporal).resolve() and work.name.startswith('r-')
        for attempt in range(1, 5):
            if not work.exists():
                break
            try:
                shutil.rmtree(work)
                preparation['intentos_limpieza'].append({'intento': attempt, 'resultado': 'limpio'})
                break
            except OSError as error:
                preparation['intentos_limpieza'].append({'intento': attempt, 'error': str(error)})
                time.sleep(.2)
        if work.exists():
            preparation['fallback_usado'] = True
            preparation['intentos_limpieza'].append({'intento': 5, 'resultado': 'cleanup tolerante'})
        temporary.cleanup()
        preparation['residuos'] = [str(path) for path in work.rglob('*')] if work.exists() else []
        preparation['carpeta_residual'] = str(work) if work.exists() else None
        if work.exists():
            warnings.warn('Quedaron temporales de referencias sin borrar: '+str(work), RuntimeWarning)
        audit = Path(temporal)/(work.name+'_limpieza.json')
        audit.write_text(json.dumps(preparation, ensure_ascii=False, indent=2), encoding='utf-8')


def crear_referencias(origen, salida, temporal, *, paginacion_actual=False):
    files=leer_origen(origen);definitions=definiciones_restantes();report={}
    temporal=Path(temporal);temporal.mkdir(parents=True,exist_ok=True)
    with _referencias_temporales(temporal) as preparation:
        work=Path(preparation['directorio']);pdfs=work/'pdf';pdfs.mkdir()
        sources=[]
        for code,definition in definitions.items():
            ref=definition['definicion']['origen_excel'];payload=files[ref['archivo']]
            if sha256(payload).hexdigest()!=ref['sha256']:raise ValueError('El original cambió: '+code)
            if paginacion_actual:
                from app.planillas.impresion import preparar_impresion
                output=BytesIO()
                with ZipFile(BytesIO(payload)) as source, ZipFile(output,'w') as target:
                    sheet=etree.fromstring(source.read('xl/worksheets/sheet1.xml'))
                    workbook=etree.fromstring(source.read('xl/workbook.xml'))
                    preparar_impresion(sheet,workbook,titulos=[title for title,_ in definition['especificacion']['bloques']])
                    replacements={'xl/worksheets/sheet1.xml':etree.tostring(sheet),'xl/workbook.xml':etree.tostring(workbook)}
                    for entry in source.infolist():target.writestr(entry,replacements.get(entry.filename,source.read(entry.filename)))
                payload=output.getvalue()
            path=work/(code.removeprefix('SG-PEM-IFI-')+'.xlsx');path.write_bytes(payload);sources.append((code,path))
        executable=localizar_libreoffice()
        for first in range(0,len(sources),8):
            batch=sources[first:first+8];profile=(work/('p'+str(first))).as_uri()
            preparation['ejecutable']=str(executable)
            preparation['perfiles'].append(profile)
            result=_ejecutar_lote([str(executable),'-env:UserInstallation='+profile,'--headless','--nologo','--nodefault','--norestore',
                '--convert-to','pdf:calc_pdf_Export','--outdir',str(pdfs),*[str(path) for _,path in batch]],preparation)
            if result.returncode:raise RuntimeError('Falló la conversión del lote de referencia.')
            for code,path in batch:
                pdf=pdfs/(path.stem+'.pdf')
                if not pdf.is_file():raise RuntimeError('Falta PDF de referencia: '+code)
                reader=PdfReader(pdf)
                report[code]={'paginas':len(reader.pages),'sha256_excel':definitions[code]['definicion']['origen_excel']['sha256'],
                    'papel':[[float(p.mediabox.width),float(p.mediabox.height)] for p in reader.pages]}
    salida=Path(salida);salida.parent.mkdir(parents=True,exist_ok=True)
    salida.write_text(json.dumps(report,indent=2),encoding='utf-8')
    return report


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--origen',required=True,type=Path);parser.add_argument('--salida',required=True,type=Path)
    parser.add_argument('--temporal',required=True,type=Path);args=parser.parse_args()
    report=crear_referencias(args.origen,args.salida,args.temporal)
    print(json.dumps({'originales_comparados':len(report),'paginas_totales':sum(r['paginas'] for r in report.values())}))
