"""Franja de identificación complementaria al pie, sin modificar filas del kit."""
from datetime import date
import textwrap
from .firmantes import nombre_tecnico_segun_modo

from pypdf.generic import ArrayObject,DecodedStreamObject,DictionaryObject,NameObject

FUENTE=7
INTERLINEADO=8.5
BASE=44


def lineas_firmantes(datos,ancho):
    tecnico=datos['tecnico'];responsable=datos['responsable']
    fecha=date.fromisoformat(datos['fecha']).strftime('%d/%m/%Y')
    nombre=nombre_tecnico_segun_modo(tecnico.get('nombre'))
    # El login conserva la identidad autenticada si el nombre usa otra escritura.
    try:nombre.encode('cp1252')
    except UnicodeEncodeError:nombre=tecnico.get('login') or ''
    columnas=[['TÉCNICO DE READYPROOF',f"Usuario: {tecnico.get('login') or 'Sin firma registrada'}",f'Nombre: {nombre}', 'Empresa: '+datos.get('empresa_mantenedora','readyproof'),f'Fecha del servicio: {fecha}'],
              ['RESPONSABLE DE LA INSTALACIÓN',f"Nombre: {responsable.get('nombre_firmante') or 'Sin completar'}",f"DNI: {responsable.get('dni_firmante') or 'Sin completar'}",f"Cargo: {responsable.get('cargo_firmante') or 'No informado'}",f"Empresa: {datos['empresa']}",f'Fecha del servicio: {fecha}']]
    # El glifo más ancho de Helvetica WinAnsi ocupa 1,015 em.
    limite=max(1,int(ancho/(FUENTE*1.02)))
    return [[part for linea in columna for part in textwrap.wrap(linea,width=limite,break_long_words=True,break_on_hyphens=False)] for columna in columnas]


def preparar_identificacion(datos,width,height):
    columnas=lineas_firmantes(datos,(width-100)/2)
    top=BASE+max(map(len,columnas))*INTERLINEADO
    # Reserva el texto bajo el área impresa; misma escala en todas las páginas.
    escala=min(.95,(height-8-top-10)/(height-8-20))
    if escala<.70:raise RuntimeError('La identificación excede el espacio reservado del PDF.')
    return columnas,top,escala


def pegar_identificacion(writer,page,font_ref,columnas,top):
    resources=DictionaryObject(dict(page['/Resources'].get_object()))
    fonts=DictionaryObject(dict(resources.get('/Font',DictionaryObject()).get_object()))
    fonts[NameObject('/RPFirmantes')]=font_ref;resources[NameObject('/Font')]=fonts;page[NameObject('/Resources')]=resources
    width=float(page.mediabox.width);commands=[f'q 0.2 g 0.5 w 40 {top+4:.3f} m {width-40:.3f} {top+4:.3f} l S']
    for index,column in enumerate(columnas):
        x=40+index*((width-60)/2)
        for offset,line in enumerate(column):
            commands.append(f'BT /RPFirmantes {FUENTE} Tf 1 0 0 1 {x:.3f} {top-INTERLINEADO*(offset+1):.3f} Tm <{line.encode("cp1252").hex()}> Tj ET')
    commands.append('Q\n');stream=DecodedStreamObject();stream.set_data('\n'.join(commands).encode('ascii'))
    original=page.get('/Contents');resolved=original.get_object() if original is not None else None
    contents=ArrayObject(list(resolved) if isinstance(resolved,ArrayObject) else [original] if original is not None else [])
    contents.append(writer._add_object(stream));page[NameObject('/Contents')]=contents
