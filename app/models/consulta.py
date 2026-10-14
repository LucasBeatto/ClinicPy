from datetime import date, datetime, time

from sqlalchemy import (
    Date,
    Enum,
    ForeignKey,
    ForeignKeyConstraint,
    Integer,
    TIMESTAMP,
    Time,
    text,
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

class Consulta(Base):
    __tablename__ = "consulta"

    __table_args__ = (
        ForeignKeyConstraint(
            ["medico_id", "especialidade_id"],
            [
                "medico_especialidade.medico_id",
                "medico_especialidade.especialidade_id",
            ],
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    paciente_id: Mapped[int] = mapped_column(
        ForeignKey("paciente.id"),
        nullable=False
    )

    medico_id: Mapped[int] = mapped_column(
        ForeignKey("medico.id"),
        nullable=False
    )

    especialidade_id: Mapped[int] = mapped_column(
        ForeignKey("especialidade.id"),
        nullable=False
    )

    data_consulta: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    horario: Mapped[time] = mapped_column(
        Time,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        Enum(
            "pendente",
            "confirmada",
            "cancelada",
            "em_andamento",
            "finalizada",
        ),
        nullable=False,
        server_default="pendente"
    )

    data_solicitacao: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP")
    )

    paciente: Mapped["Paciente"] = relationship(
        "Paciente",
        back_populates="consultas"
    )

    medico: Mapped["Medico"] = relationship(
        "Medico",
        back_populates="consultas"
    )

    especialidade: Mapped["Especialidade"] = relationship(
        "Especialidade",
        back_populates="consultas"
    )

    documentos: Mapped[list["Documento"]] = relationship(
        "Documento",
        back_populates="consulta"
    )

    def __repr__(self):
        return (
            f"Consulta("
            f"id={self.id}, "
            f"paciente_id={self.paciente_id}, "
            f"medico_id={self.medico_id}, "
            f"especialidade_id={self.especialidade_id}, "
            f"data={self.data_consulta}, "
            f"horario={self.horario}, "
            f"status='{self.status}'"
            f")"
        )