from datetime import date
from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status,
)
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.horario import HorariosDisponiveisResponse
from app.services.horario_service import listar_horarios_disponiveis


router = APIRouter(
    prefix="/medicos/{medico_id}/horarios-disponiveis",
    tags=["Horários"],
)


@router.get(
    "/",
    response_model=HorariosDisponiveisResponse,
)
def obter_horarios_disponiveis(
    medico_id: int,
    data: Annotated[
    date,
    Query(
        description=(
            "Data desejada no formato AAAA-MM-DD. "
            "Exemplo: 2026-11-16."
        ),
        examples=["2026-11-16"],
    ),
],
    db: Annotated[Session, Depends(get_db)],
):
    try:
        horarios = listar_horarios_disponiveis(
            db=db,
            medico_id=medico_id,
            data_consulta=data,
        )

        return {
            "medico_id": medico_id,
            "data": data,
            "horarios": horarios,
        }

    except LookupError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(erro),
        ) from erro