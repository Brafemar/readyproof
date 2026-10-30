"""Paginación de copias de Excel oficiales, con ajuste de impresión opcional."""
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from io import BytesIO
from zipfile import ZipFile
from lxml import etree

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from pypdf import PdfReader
from app.planillas.catalogo_completo import definiciones_restantes
from app.planillas.importacion_excel import leer_origen
from app.planillas.pdf import localizar_libreoffice


def crear_referencias(origen, salida, temporal, *, paginacion_actual=False):
    files=leer_origen(origen);definitions=definiciones_restantes();report={}
    temporal=Path(temporal);temporal.mkdir(parents=True,exist_ok=True)
    with TemporaryDirectory(prefix='r-',dir=temporal) as directory:
        work=Path(directory);pdfs=work/'pdf';pdfs.mkdir()
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
            result=subprocess.run([str(executable),'-env:UserInstallation='+profile,'--headless','--nologo','--nodefault','--norestore',
                '--convert-to','pdf:calc_pdf_Export','--outdir',str(pdfs),*[str(path) for _,path in batch]],capture_output=True,timeout=300)
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
