"""Persistencia de clientes, sistemas, plantillas y cargas de la etapa 2."""
from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Boolean, CheckConstraint, DateTime, ForeignKey, Integer, JSON, LargeBinary, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


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


class Carga(Base):
    __tablename__ = "cargas"
    __table_args__ = (CheckConstraint("estado IN ('borrador','finalizada','emitida')"),)
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=identificador)
    sistema_id: Mapped[str] = mapped_column(ForeignKey("sistemas.id"), index=True)
    planilla_id: Mapped[str] = mapped_column(ForeignKey("planillas.id"), index=True)
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


class RevisionCarga(Base):
    __tablename__ = "revisiones_carga"
    __table_args__ = (UniqueConstraint("carga_id", "numero"),)
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=identificador)
    carga_id: Mapped[str] = mapped_column(ForeignKey("cargas.id"), index=True)
    numero: Mapped[int] = mapped_column(Integer)
    evento: Mapped[str] = mapped_column(String(40))
    datos: Mapped[dict] = mapped_column(JSON)
    actor: Mapped[str] = mapped_column(String(120), default="[Ejemplo] API local sin autenticación")
    fecha: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=ahora)


class VersionEsquema(Base):
    __tablename__ = "versiones_esquema"
    numero: Mapped[int] = mapped_column(Integer, primary_key=True)
    aplicada_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=ahora)
