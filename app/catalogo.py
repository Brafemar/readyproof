"""Registro local de la única planilla aprobada y datos de prueba."""
from hashlib import sha256
from sqlalchemy import select
from .models import Cliente, Sistema, Planilla
from .planillas.definiciones.saa1 import HERRAMIENTAS, MODELO
from .planillas.validacion import esquema_saa1


def huella_saa1():
    digest = sha256()
    for path in (HERRAMIENTAS / "planillas_data3.py", HERRAMIENTAS / "build_planilla.py", MODELO):
        digest.update(path.read_bytes())
    return digest.hexdigest()


def registrar_ejemplos(session):
    planilla = session.scalar(select(Planilla).where(Planilla.codigo == "SG-PEM-IFI-SAA-1", Planilla.version == "00-26"))
    if planilla is None:
        planilla = Planilla(codigo="SG-PEM-IFI-SAA-1", version="00-26", sistema_tipo="SAA", huella=huella_saa1(), definicion=esquema_saa1())
        session.add(planilla)
    elif planilla.huella != huella_saa1():
        raise RuntimeError("La plantilla cambió; registrar una nueva versión antes de usarla.")
    cliente = session.scalar(select(Cliente).where(Cliente.nombre == "[Ejemplo] Planta de prueba"))
    if cliente is None:
        cliente = Cliente(nombre="[Ejemplo] Planta de prueba", es_ejemplo=True)
        session.add(cliente)
        session.flush()
    sistema = session.scalar(select(Sistema).where(Sistema.cliente_id == cliente.id, Sistema.tipo == "SAA"))
    if sistema is None:
        sistema = Sistema(cliente_id=cliente.id, tipo="SAA", designacion="[Ejemplo] Abastecimiento de agua")
        session.add(sistema)
    session.commit()
    return cliente, sistema, planilla
