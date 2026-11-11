from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.disponibilidade import (
    DisponibilidadeCreate,
    DisponibilidadeResponse,
)
from app.services.disponibilidade_service import (
    criar_disponibilidade,
    listar_disponibilidades_medico,
)


router = APIRouter(
    prefix="/medicos/{medico_id}/disponibilidades",
    tags=["Disponibilidades"],
)


@router.get(
    "/",
    response_model=list[DisponibilidadeResponse],
)
def obter_disponibilidades(
    medico_id: int,
    db: Annotated[Session, Depends(get_db)],
):
    try:
        return listar_disponibilidades_medico(
            db=db,
            medico_id=medico_id,
        )

    except LookupError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(erro),
        ) from erro


@router.post(
    "/",
    response_model=DisponibilidadeResponse,
    status_code=status.HTTP_201_CREATED,
)
def cadastrar_disponibilidade(
    medico_id: int,
    dados: DisponibilidadeCreate,
    db: Annotated[Session, Depends(get_db)],
):
    try:
        return criar_disponibilidade(
            db=db,
            medico_id=medico_id,
            **dados.model_dump(),
        )

    except LookupError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(erro),
        ) from erro

    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(erro),
        ) from erro