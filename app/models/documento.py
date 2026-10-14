from datetime import datetime

from sqlalchemy import Enum, ForeignKey, String, TIMESTAMP, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

class Documento(Base):
    __tablename__ = "documento"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    consulta_id: Mapped[int] = mapped_column(
        ForeignKey("consulta.id"),
        nullable=False
    )

    tipo: Mapped[str] = mapped_column(
        Enum(
            "receita",
            "atestado",
            "pedido_exame",
            "laudo",
            "outro",
        ),
        nullable=False
    )

    caminho_arquivo: Mapped[str] = mapped_column(
        String(260),
        nullable=False
    )

    data_envio: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP")
    )

    consulta: Mapped["Consulta"] = relationship(
        "Consulta",
        back_populates="documentos"
    )

    def __repr__(self):
        return (
            f"Documento("
            f"id={self.id}, "
            f"consulta_id={self.consulta_id}, "
            f"tipo={self.tipo}, "
            f"caminho_arquivo='{self.arquivo}'"
            f")"
        )