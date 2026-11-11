from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.especialidade import EspecialidadeResponse
from app.services.especialidade_service import listar_especialidades

router = APIRouter(
    prefix="/especialidades",
    tags=["Especialidades"],
)

# Entrega as especialidades cadastradas
@router.get(
    "/",
    response_model=list[EspecialidadeResponse],
)
def obter_especialidades(
    db: Annotated[Session, Depends(get_db)],
):
    return listar_especialidades(db)