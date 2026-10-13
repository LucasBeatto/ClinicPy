from datetime import time

from sqlalchemy import CheckConstraint, ForeignKey, Integer, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Disponibilidade(Base):
    __tablename__ = "disponibilidade"

    __table_args__ = (
        CheckConstraint(
            "horario_inicio < horario_fim"
        ),
        CheckConstraint(
            "duracao_consulta > 0"
        ),
        CheckConstraint(
            "dia_semana BETWEEN 1 AND 7"
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    medico_id: Mapped[int] = mapped_column(
        ForeignKey("medico.id"),
        nullable=False
    )

    dia_semana: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    horario_inicio: Mapped[time] = mapped_column(
        Time,
        nullable=False
    )

    horario_fim: Mapped[time] = mapped_column(
        Time,
        nullable=False
    )

    duracao_consulta: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    medico: Mapped["Medico"] = relationship(
        "Medico",
        back_populates="disponibilidades"
    )

    def __repr__(self):
        return (
            f"Disponibilidade("
            f"id={self.id}, "
            f"medico_id={self.medico_id}, "
            f"dia_semana={self.dia_semana}, "
            f"inicio={self.horario_inicio}, "
            f"fim={self.horario_fim}, "
            f"duracao={self.duracao_consulta}"
            f")"
        )