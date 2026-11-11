from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.consulta import (
    ConsultaCreate,
    ConsultaResponse,
)
from app.services.consulta_service import criar_consulta


router = APIRouter(
    prefix="/consultas",
    tags=["Consultas"],
)


@router.post(
    "/",
    response_model=ConsultaResponse,
    status_code=status.HTTP_201_CREATED,
)
def cadastrar_consulta(
    dados: ConsultaCreate,
    db: Annotated[
        Session,
        Depends(get_db),
    ],
):
    try:
        return criar_consulta(
            db=db,
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