from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Especialidade

def listar_especialidades(
        db: Session,
) -> list[Especialidade]:

    consulta = (
        select(Especialidade)
        .order_by(Especialidade.nome)
    )

    especialidades = db.scalars(consulta).all()

    return list(especialidades)