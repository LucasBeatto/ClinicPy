from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.associations import medico_especialidade


class Especialidade(Base):
    __tablename__ = "especialidade"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    nome: Mapped[str] = mapped_column(
        String(80),
        nullable=False,
        unique=True
    )

    medicos: Mapped[list["Medico"]] = relationship(
        "Medico",
        secondary=medico_especialidade,
        back_populates="especialidades"
    )

    consultas: Mapped[list["Consulta"]] = relationship(
        "Consulta",
        back_populates="especialidade"
    )

    def __repr__(self):
        return (
            f"Especialidade("
            f"id={self.id}, "
            f"nome='{self.nome}'"
            f")"
        )