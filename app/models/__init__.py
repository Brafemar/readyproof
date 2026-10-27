"""Persistencia de clientes, sistemas, plantillas y cargas de la etapa 2."""
from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Boolean, CheckConstraint, DateTime, ForeignKey, Integer, JSON, LargeBinary, String, Text, Uuid, Enum, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


def ahora():
    return datetime.now(timezone.utc)


def identificador():
    return str(uuid4())


class Base(DeclarativeBase):
    pass


class Cliente(Base):
    __tablename__ = "clientes"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=identificador)
    nombre: Mapped[str] = mapped_column(String(200))
    es_ejemplo: Mapped[bool] = mapped_column(Boolean, default=True)


class Sistema(Base):
    __tablename__ = "sistemas"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=identificador)
    cliente_id: Mapped[str] = mapped_column(ForeignKey("clientes.id"), index=True)
    tipo: Mapped[str] = mapped_column(String(12))
    designacion: Mapped[str] = mapped_column(String(200))


class Planilla(Base):
    __tablename__ = "planillas"
    __table_args__ = (UniqueConstraint("codigo", "version"),)
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=identificador)
    codigo: Mapped[str] = mapped_column(String(60))
    version: Mapped[str] = mapped_column(String(30))
    sistema_tipo: Mapped[str] = mapped_column(String(12))
    huella: Mapped[str] = mapped_column(String(64))
    definicion: Mapped[dict] = mapped_column(JSON)
    manual_id: Mapped[str | None] = mapped_column(ForeignKey("manuales.id"))
    manual: Mapped["Manual | None"] = relationship(back_populates="planillas")


class Carga(Base):
    __tablename__ = "cargas"
    __table_args__ = (CheckConstraint("estado IN ('borrador','finalizada','emitida')"),)
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=identificador)
    sistema_id: Mapped[str] = mapped_column(ForeignKey("sistemas.id"), index=True)
    planilla_id: Mapped[str] = mapped_column(ForeignKey("planillas.id"), index=True)
    creada_por_id: Mapped[str | None] = mapped_column(ForeignKey("usuarios.id"))
    estado: Mapped[str] = mapped_column(String(20), default="borrador")
    datos: Mapped[dict] = mapped_column(JSON)
    revision: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    creada_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=ahora)
    actualizada_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=ahora)
    finalizada_en: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    emitida_en: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    pdf: Mapped[bytes | None] = mapped_column(LargeBinary)
    pdf_sha256: Mapped[str | None] = mapped_column(String(64))
    __mapper_args__ = {"version_id_col": revision}
    envios: Mapped[list["Envio"]] = relationship(back_populates="carga",passive_deletes="all")


class RevisionCarga(Base):
    __tablename__ = "revisiones_carga"
    __table_args__ = (UniqueConstraint("carga_id", "numero"),)
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=identificador)
    carga_id: Mapped[str] = mapped_column(ForeignKey("cargas.id"), index=True)
    numero: Mapped[int] = mapped_column(Integer)
    evento: Mapped[str] = mapped_column(String(40))
    datos: Mapped[dict] = mapped_column(JSON)
    firmas_huellas: Mapped[dict | None] = mapped_column(JSON)
    actor_id: Mapped[str | None] = mapped_column(ForeignKey("usuarios.id"))
    actor: Mapped[str] = mapped_column(String(120), default="[Ejemplo] API local sin autenticación")
    fecha: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=ahora)


class FirmaCarga(Base):
    __tablename__ = "firmas_carga"
    carga_id: Mapped[str] = mapped_column(ForeignKey("cargas.id"), primary_key=True)
    tecnico_png: Mapped[bytes | None] = mapped_column(LargeBinary)
    responsable_png: Mapped[bytes | None] = mapped_column(LargeBinary)


class VersionEsquema(Base):
    __tablename__ = "versiones_esquema"
    numero: Mapped[int] = mapped_column(Integer, primary_key=True)
    aplicada_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=ahora)


class Usuario(Base):
    __tablename__ = "usuarios"
    __table_args__ = (CheckConstraint("rol IN ('admin','tecnico')"),)
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=identificador)
    login: Mapped[str] = mapped_column(String(80), unique=True)
    nombre: Mapped[str] = mapped_column(String(120))
    clave_hash: Mapped[bytes] = mapped_column(LargeBinary)
    rol: Mapped[str] = mapped_column(String(12))
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    creado_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=ahora)


class UsuarioCliente(Base):
    __tablename__ = "usuarios_clientes"
    usuario_id: Mapped[str] = mapped_column(ForeignKey("usuarios.id"), primary_key=True)
    cliente_id: Mapped[str] = mapped_column(ForeignKey("clientes.id"), primary_key=True)


class SesionUsuario(Base):
    __tablename__ = "sesiones_usuario"
    token_hash: Mapped[str] = mapped_column(String(64), primary_key=True)
    usuario_id: Mapped[str] = mapped_column(ForeignKey("usuarios.id"), index=True)
    vence_en: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class RegistroAcceso(Base):
    __tablename__ = "registros_acceso"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=identificador)
    usuario_id: Mapped[str | None] = mapped_column(ForeignKey("usuarios.id"), index=True)
    fecha: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=ahora, index=True)
    evento: Mapped[str] = mapped_column(String(40))
    ruta: Mapped[str] = mapped_column(String(200))
    metodo: Mapped[str] = mapped_column(String(10))
    estado_http: Mapped[int] = mapped_column(Integer)
    cliente_id: Mapped[str | None] = mapped_column(ForeignKey("clientes.id"))
    carga_id: Mapped[str | None] = mapped_column(ForeignKey("cargas.id"))
    planilla_codigo: Mapped[str | None] = mapped_column(String(60))
    destinatario: Mapped[str | None] = mapped_column(String(254))
    login_huella: Mapped[str | None] = mapped_column(String(64), index=True)


class Manual(Base):
    __tablename__ = "manuales"
    __table_args__ = (UniqueConstraint("codigo","version",name="uq_manual_codigo_version"),)
    id: Mapped[str] = mapped_column(Uuid(as_uuid=False),primary_key=True,default=identificador)
    codigo: Mapped[str] = mapped_column(String(60),unique=True)
    titulo: Mapped[str] = mapped_column(String(255))
    sistema_tipo: Mapped[str] = mapped_column(String(12))
    contenido: Mapped[str] = mapped_column(Text)
    campos_obligatorios: Mapped[list] = mapped_column(JSON,default=list)
    version: Mapped[str] = mapped_column(String(30))
    planillas: Mapped[list["Planilla"]] = relationship(back_populates="manual",passive_deletes="all")


class Envio(Base):
    __tablename__ = "envios"
    __table_args__ = (CheckConstraint("intentos_reservados BETWEEN 0 AND 3", name="ck_envio_max_intentos"),)
    usuario_id: Mapped[str | None] = mapped_column(ForeignKey("usuarios.id"))
    asunto: Mapped[str | None] = mapped_column(String(200))
    cuerpo: Mapped[str | None] = mapped_column(Text)
    pdf_copia: Mapped[bytes | None] = mapped_column(LargeBinary)
    pdf_sha256: Mapped[str | None] = mapped_column(String(64))
    mensaje_eml: Mapped[bytes | None] = mapped_column(LargeBinary)
    eml_sha256: Mapped[str | None] = mapped_column(String(64))
    retener_hasta: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    intentos_reservados: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    en_proceso_desde: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    id: Mapped[str] = mapped_column(Uuid(as_uuid=False),primary_key=True,default=identificador)
    carga_id: Mapped[str] = mapped_column(ForeignKey("cargas.id",ondelete="CASCADE"),index=True)
    destinatario: Mapped[str] = mapped_column(String(255))
    enviado_en: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    estado: Mapped[str] = mapped_column(Enum("pendiente","enviado","fallo","descartado",name="estado_envio"),default="pendiente")
    creado_en: Mapped[datetime] = mapped_column(DateTime(timezone=True),default=ahora)
    carga: Mapped["Carga"] = relationship(back_populates="envios")
    intentos: Mapped[list["Intento"]] = relationship(back_populates="envio",passive_deletes="all")
    retenciones: Mapped[list["Retencion"]] = relationship(back_populates="envio",passive_deletes="all")


class Intento(Base):
    __tablename__ = "intentos"
    __table_args__ = (UniqueConstraint("envio_id","numero",name="uq_intento_envio_numero"),CheckConstraint("numero >= 1",name="ck_intento_numero"),CheckConstraint("resultado IN ('ok','timeout','rechazado','bounce')",name="ck_intento_resultado"),)
    id: Mapped[str] = mapped_column(Uuid(as_uuid=False),primary_key=True,default=identificador)
    envio_id: Mapped[str] = mapped_column(ForeignKey("envios.id",ondelete="CASCADE"),index=True)
    numero: Mapped[int] = mapped_column(Integer)
    intentado_en: Mapped[datetime] = mapped_column(DateTime(timezone=True),default=ahora)
    resultado: Mapped[str] = mapped_column(String(60))
    respuesta: Mapped[str | None] = mapped_column(Text)
    envio: Mapped["Envio"] = relationship(back_populates="intentos")


class Retencion(Base):
    __tablename__ = "retenciones"
    __table_args__ = (CheckConstraint("proximos_intentos BETWEEN 0 AND 2",name="ck_retencion_intentos"),CheckConstraint("razon IN ('fallo_temporal','correo_invalido','bloqueado')",name="ck_retencion_razon"),)
    id: Mapped[str] = mapped_column(Uuid(as_uuid=False),primary_key=True,default=identificador)
    envio_id: Mapped[str] = mapped_column(ForeignKey("envios.id",ondelete="CASCADE"),index=True)
    reintentado_en: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    proximos_intentos: Mapped[int] = mapped_column(Integer,default=0)
    razon: Mapped[str] = mapped_column(String(255))
    envio: Mapped["Envio"] = relationship(back_populates="retenciones")
