"""Marcas de agua aprobadas, reutilizando los logos del encabezado."""
from pypdf import PdfReader,PdfWriter
from pypdf.generic import ArrayObject,DecodedStreamObject,DictionaryObject,FloatObject,NameObject
from .encabezado_pdf import logos_del_excel

OPACIDAD=0.055
ESTADO="/ReadyproofMarcaAgua"


def incorporar_marca_agua(excel,origen,destino):
    logos,_=logos_del_excel(excel)
    names={anchor:NameObject(f"/RPLogo{i}") for i,(anchor,_,_,_) in enumerate(logos)}
    if not {"LH","RH"}<=names.keys():
        raise RuntimeError("Se requieren los logos de readyproof e ISO para la marca de agua.")
    reader=PdfReader(origen);writer=PdfWriter();writer.clone_document_from_reader(reader)
    state=DictionaryObject({NameObject("/Type"):NameObject("/ExtGState"),NameObject("/ca"):FloatObject(OPACIDAD),NameObject("/CA"):FloatObject(OPACIDAD),NameObject("/BM"):NameObject("/Multiply")})
    state_ref=writer._add_object(state)
    for page in writer.pages:
        resources=DictionaryObject(dict(page["/Resources"].get_object()))
        page[NameObject("/Resources")]=resources
        objects=resources["/XObject"].get_object()
        if any(name not in objects or objects[name].get_object().get("/Subtype")!="/Image" for name in (names["LH"],names["RH"])):
            raise RuntimeError("Los recursos de logo del encabezado no están disponibles.")
        states=DictionaryObject(dict(resources.get("/ExtGState",DictionaryObject()).get_object()))
        if ESTADO in states:raise RuntimeError("El PDF ya tiene las marcas de agua.")
        states[NameObject(ESTADO)]=state_ref;resources[NameObject("/ExtGState")]=states
        brand,iso=(objects[names[a]].get_object() for a in ("LH","RH"))
        width,height=float(page.mediabox.width),float(page.mediabox.height)
        bw=width*.38;bh=bw*float(brand["/Height"])/float(brand["/Width"])
        iw=height*.17;ih=iw*float(iso["/Height"])/float(iso["/Width"])
        gap=width*.035;left=(width-bw-gap-iw)/2;center_y=height*.5
        commands=f"q {ESTADO} gs {bw:.5f} 0 0 {bh:.5f} {left:.5f} {center_y-bh/2:.5f} cm {names['LH']} Do Q\n"
        commands+=f"q {ESTADO} gs {iw:.5f} 0 0 {ih:.5f} {left+bw+gap:.5f} {center_y-ih/2:.5f} cm {names['RH']} Do Q\n"
        stream=DecodedStreamObject();stream.set_data(commands.encode("ascii"))
        original=page.get("/Contents");resolved=original.get_object() if original is not None else None
        contents=ArrayObject(list(resolved) if isinstance(resolved,ArrayObject) else [original] if original is not None else [])
        contents.append(writer._add_object(stream));page[NameObject("/Contents")]=contents
    writer.add_metadata({"/ReadyproofMarcaAgua":"readyproof + ISO; opacidad 0.055"})
    with open(destino,"xb") as output:writer.write(output)
