from datetime import datetime

from sqlalchemy import Enum, String, TIMESTAMP, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Usuario(Base):
    __tablename__ = "usuario"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    nome_completo: Mapped[str] = mapped_column(
        String(80),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(60),
        nullable=False,
        unique=True
    )

    tipo_usuario: Mapped[str] = mapped_column(
    Enum("medico", "paciente"),
    nullable=False
    )

    senha_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    data_cadastro: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP")
    )

    paciente: Mapped["Paciente | None"] = relationship(
        "Paciente",
        back_populates="usuario",
        uselist=False
    )

    medico: Mapped["Medico | None"] = relationship(
        "Medico",
        back_populates="usuario",
        uselist=False
    )

    def __repr__(self):
        return (
            f"Usuario("
            f"id={self.id}, "
            f"nome='{self.nome_completo}', "
            f"email='{self.email}', "
            f"tipo='{self.tipo_usuario}'"
            f")"
        )