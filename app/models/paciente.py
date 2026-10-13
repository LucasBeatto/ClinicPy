from datetime import date

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

class Paciente(Base):
    __tablename__ = "paciente"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuario.id"),
        nullable=False,
        autoincrement=True
    )

    cpf: Mapped[str] = mapped_column(
        String(11),
        nullable=False,
        unique=True
    )

    data_nascimento: Mapped[date] = mapped_column(
        nullable=False
    )

    telefone: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    codigo_postal: Mapped[str | None] = mapped_column(
        String(10),
        nullable=False
    )

    usuario: Mapped["Usuario"] = relationship(
        "Usuario",
        back_populates="paciente"
    )

    def __repr__(self):
        return (
            f"Paciente("
            f"id={self.id}, "
            f"usuario_id={self.usuario_id}, "
            f"cpf='{self.cpf}'"
            f")"
        )