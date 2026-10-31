"""Fotos de campo y anotaciones de cargas (frente C, subfase C1)."""
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, Float, ForeignKey, Integer, LargeBinary, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from . import Base, ahora, identificador

MAX_FOTOS_POR_CARGA = 20
MAX_TEXTO_ANOTACION = 140


class FotoCarga(Base):
    __tablename__ = "fotos_carga"
    __table_args__ = (
        UniqueConstraint("carga_id", "orden", name="uq_foto_carga_orden"),
        CheckConstraint("orden >= 1", name="ck_foto_orden"),
        CheckConstraint("ancho > 0 AND alto > 0", name="ck_foto_dimensiones"),
        CheckConstraint("char_length(sha256) = 64", name="ck_foto_sha256"),
    )
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=identificador)
    carga_id: Mapped[str] = mapped_column(ForeignKey("cargas.id"), index=True, nullable=False)
    orden: Mapped[int] = mapped_column(Integer, nullable=False)
    imagen: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    ancho: Mapped[int] = mapped_column(Integer, nullable=False)
    alto: Mapped[int] = mapped_column(Integer, nullable=False)
    sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    creado_por_id: Mapped[str | None] = mapped_column(ForeignKey("usuarios.id"), nullable=True)
    creada_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=ahora, nullable=False)


class FotoAnotacion(Base):
    __tablename__ = "fotos_anotacion"
    __table_args__ = (
        UniqueConstraint("foto_id", "numero", name="uq_anotacion_foto_numero"),
        CheckConstraint("numero >= 1", name="ck_anotacion_numero"),
        CheckConstraint("x BETWEEN 0 AND 1 AND y BETWEEN 0 AND 1", name="ck_anotacion_posicion"),
        CheckConstraint("codigo IN ('✓', 'O', 'X', 'NA')", name="ck_anotacion_codigo"),
        CheckConstraint(f"char_length(texto) <= {MAX_TEXTO_ANOTACION} AND (codigo IN ('✓', 'NA') OR char_length(texto) >= 1)", name="ck_anotacion_texto"),
    )
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=identificador)
    foto_id: Mapped[str] = mapped_column(ForeignKey("fotos_carga.id"), index=True, nullable=False)
    numero: Mapped[int] = mapped_column(Integer, nullable=False)
    x: Mapped[float] = mapped_column(Float, nullable=False)
    y: Mapped[float] = mapped_column(Float, nullable=False)
    codigo: Mapped[str] = mapped_column(String(2), nullable=False)
    texto: Mapped[str] = mapped_column(String(MAX_TEXTO_ANOTACION), nullable=False)
    creada_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=ahora, nullable=False)
