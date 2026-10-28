"""Identificación de emisión en el pie reservado, sin modificar la planilla del kit."""
from io import BytesIO

from pypdf import PdfReader, PdfWriter
from pypdf.generic import ArrayObject, DecodedStreamObject, DictionaryObject, NameObject

from .leyenda_iram import PIE_PT


def incorporar_registro(payload, numero, revision):
    reader = PdfReader(BytesIO(payload))
    if reader.metadata and reader.metadata.get('/ReadyproofRegistro'):
        raise RuntimeError('El PDF ya contiene un número de registro.')
    writer = PdfWriter()
    writer.clone_document_from_reader(reader)
    font = writer._add_object(DictionaryObject({NameObject('/Type'): NameObject('/Font'),
        NameObject('/Subtype'): NameObject('/Type1'), NameObject('/BaseFont'): NameObject('/Helvetica'),
        NameObject('/Encoding'): NameObject('/WinAnsiEncoding')}))
    label = f'Registro {numero} | Revisión {revision}'
    for page in writer.pages:
        resources = DictionaryObject(dict(page['/Resources'].get_object()))
        fonts = DictionaryObject(dict(resources.get('/Font', DictionaryObject()).get_object()))
        fonts[NameObject('/RPRegistro')] = font
        resources[NameObject('/Font')] = fonts
        page[NameObject('/Resources')] = resources
        stream = DecodedStreamObject()
        stream.set_data(f'q 0.5 g BT /RPRegistro 7 Tf 1 0 0 1 {PIE_PT:.6f} {PIE_PT:.6f} Tm <{label.encode("cp1252").hex()}> Tj ET Q\n'.encode('ascii'))
        original = page.get('/Contents')
        resolved = original.get_object() if original is not None else None
        contents = ArrayObject(list(resolved) if isinstance(resolved, ArrayObject) else [original] if original is not None else [])
        contents.append(writer._add_object(stream))
        page[NameObject('/Contents')] = contents
    writer.add_metadata({'/ReadyproofRegistro': str(numero), '/ReadyproofRevision': str(revision)})
    result = BytesIO()
    writer.write(result)
    return result.getvalue()


def incorporar_modo(payload, modo):
    if modo not in ('PILOTO','REAL'):raise ValueError('Modo de PDF inválido.')
    reader=PdfReader(BytesIO(payload))
    if reader.metadata and reader.metadata.get('/ReadyproofModo'):
        raise RuntimeError('El PDF ya identifica su modo de emisión.')
    writer=PdfWriter();writer.clone_document_from_reader(reader)
    font=writer._add_object(DictionaryObject({NameObject('/Type'):NameObject('/Font'),
        NameObject('/Subtype'):NameObject('/Type1'),NameObject('/BaseFont'):NameObject('/Helvetica')}))
    for page in writer.pages:
        resources=DictionaryObject(dict(page.get('/Resources',DictionaryObject()).get_object()))
        fonts=DictionaryObject(dict(resources.get('/Font',DictionaryObject()).get_object()))
        fonts[NameObject('/RPModo')]=font;resources[NameObject('/Font')]=fonts;page[NameObject('/Resources')]=resources
        label=('Modo '+modo).encode('ascii').hex();x=float(page.mediabox.width)-80
        stream=DecodedStreamObject();stream.set_data(f'q 0.5 g BT /RPModo 7 Tf 1 0 0 1 {x:.3f} {PIE_PT:.6f} Tm <{label}> Tj ET Q\n'.encode('ascii'))
        original=page.get('/Contents');resolved=original.get_object() if original is not None else None
        contents=ArrayObject(list(resolved) if isinstance(resolved,ArrayObject) else [original] if original is not None else [])
        contents.append(writer._add_object(stream));page[NameObject('/Contents')]=contents
    writer.add_metadata({'/ReadyproofModo':modo});result=BytesIO();writer.write(result)
    return result.getvalue()
