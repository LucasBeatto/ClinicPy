from sqlalchemy import Column, ForeignKey, Integer, Table

from app.database.base import Base


medico_especialidade = Table(
    "medico_especialidade",
    Base.metadata,

    Column(
        "medico_id",
        Integer,
        ForeignKey("medico.id"),
        primary_key=True,
        nullable=False,
    ),

    Column(
        "especialidade_id",
        Integer,
        ForeignKey("especialidade.id"),
        primary_key=True,
        nullable=False,
    ),
)