"""Registro local de la única planilla aprobada y datos de prueba."""
from hashlib import sha256
from sqlalchemy import select
from .models import Cliente, Sistema, Planilla, Manual
from .planillas.definiciones.saa1 import HERRAMIENTAS, MODELO
from .planillas.validacion import esquema_saa1

VERSION_PILOTO = "00-26-rp2"


def huella_saa1():
    digest = sha256()
    for path in (HERRAMIENTAS / "planillas_data3.py", HERRAMIENTAS / "build_planilla.py", MODELO):
        digest.update(path.read_bytes())
    return digest.hexdigest()


def registrar_ejemplos(session):
    manual=session.scalar(select(Manual).where(Manual.codigo=="SG-PEM-IFI-SAA-EJEMPLO"))
    if manual is None:
        manual=Manual(codigo="SG-PEM-IFI-SAA-EJEMPLO",titulo="[Ejemplo] Sistema de Abastecimiento de Agua",sistema_tipo="SAA",contenido="[Ejemplo] Contenido de prueba. Procedimiento y campos obligatorios pendientes de confirmación técnica.",campos_obligatorios=[],version="v1")
        session.add(manual)
    planilla = session.scalar(select(Planilla).where(Planilla.codigo == "SG-PEM-IFI-SAA-1", Planilla.version == VERSION_PILOTO))
    if planilla is None:
        planilla = Planilla(codigo="SG-PEM-IFI-SAA-1", version=VERSION_PILOTO, sistema_tipo="SAA", huella=huella_saa1(), definicion=esquema_saa1())
        session.add(planilla)
    elif planilla.huella != huella_saa1():
        raise RuntimeError("La plantilla cambió; registrar una nueva versión antes de usarla.")
    if planilla.manual_id is None:
        planilla.manual=manual
    cliente = session.scalar(select(Cliente).where(Cliente.nombre == "[Ejemplo] Planta de prueba"))
    if cliente is None:
        cliente = Cliente(nombre="[Ejemplo] Planta de prueba", es_ejemplo=True)
        session.add(cliente)
        session.flush()
    sistema = session.scalar(select(Sistema).where(Sistema.cliente_id == cliente.id, Sistema.tipo == "SAA"))
    if sistema is None:
        sistema = Sistema(cliente_id=cliente.id, tipo="SAA", designacion="[Ejemplo] Abastecimiento de agua")
        session.add(sistema)
    from .planillas.multisistema import DESIGNACIONES
    session.flush()
    for family,name in DESIGNACIONES.items():
        if session.scalar(select(Sistema).where(Sistema.cliente_id==cliente.id,Sistema.tipo==family)) is None:
            session.add(Sistema(cliente_id=cliente.id,tipo=family,designacion=name))
    session.flush()
    from .planillas.catalogo_completo import completar_sistemas_ejemplo
    completar_sistemas_ejemplo(session.connection())
    session.commit()
    return cliente, sistema, planilla
