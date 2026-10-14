from sqlalchemy import CHAR, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.associations import medico_especialidade


class Medico(Base):
    __tablename__ = "medico"

    __table_args__ = (
        UniqueConstraint("crm", "uf_crm"),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuario.id"),
        nullable=False,
        unique=True
    )

    crm: Mapped[str] = mapped_column(
        String(10),
        nullable=False
    )

    uf_crm: Mapped[str] = mapped_column(
        CHAR(2),
        nullable=False
    )

    telefone_profissional: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    codigo_postal: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True
    )

    usuario: Mapped["Usuario"] = relationship(
        "Usuario",
        back_populates="medico"
    )

    especialidades: Mapped[list["Especialidade"]] = relationship(
        "Especialidade",
        secondary=medico_especialidade,
        back_populates="medicos"
    )

    disponibilidades: Mapped[list["Disponibilidade"]] = relationship(
        "Disponibilidade",
        back_populates="medico"
    )

    consultas: Mapped[list["Consulta"]] = relationship(
        "Consulta",
        back_populates="medico"
    )

    def __repr__(self):
        return (
            f"Medico("
            f"id={self.id}, "
            f"crm='{self.crm}', "
            f"uf='{self.uf_crm}'"
            f")"
        )