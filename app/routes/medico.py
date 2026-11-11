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
from app.schemas.medico import (
    MedicoCreate,
    MedicoListaResponse,
    MedicoResponse,
)
from app.services.medico_service import (
    criar_medico,
    listar_medicos,
)

from app.schemas.consulta import (
    ConsultaMedicoResponse,
    ConsultaResponse,
    ConsultaStatus,
    ConsultaStatusUpdate,
)

from app.services.consulta_service import (
    alterar_status_consulta_medico,
    listar_consultas_medico,
)


router = APIRouter(
    prefix="/medicos",
    tags=["Médicos"],
)


@router.get(
    "/",
    response_model=list[MedicoListaResponse],
)
def obter_medicos(
    db: Annotated[Session, Depends(get_db)],
    especialidade_id: int | None = None,
):
    return listar_medicos(
        db = db,
        especialidade_id=especialidade_id,
    )


@router.post(
    "/",
    response_model=MedicoResponse,
    status_code=status.HTTP_201_CREATED,
)
def cadastrar_medico(
    dados: MedicoCreate,
    db: Annotated[Session, Depends(get_db)],
):
    try:
        usuario, medico = criar_medico(
            db=db,
            **dados.model_dump()
        )

        return {
            "usuario": usuario,
            "medico": medico,
        }

    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(erro),
        ) from erro

@router.get(
    "/{medico_id}/consultas/",
    response_model=list[ConsultaMedicoResponse],
)
def obter_consultas_medico(
    medico_id: int,
    db: Annotated[
        Session,
        Depends(get_db),
    ],
    status_consulta: ConsultaStatus | None = Query(
        default=None,
        alias="status",
        description=(
            "Filtra as consultas pelo status. "
            "Exemplo: pendente."
        ),
    ),
):
    try:
        return listar_consultas_medico(
            db=db,
            medico_id=medico_id,
            status_consulta=status_consulta,
        )

    except LookupError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(erro),
        ) from erro

@router.patch(
    "/{medico_id}/consultas/{consulta_id}/status",
    response_model=ConsultaResponse,
)
def alterar_status_consulta(
    medico_id: int,
    consulta_id: int,
    dados: ConsultaStatusUpdate,
    db: Annotated[
        Session,
        Depends(get_db),
    ],
):
    try:
        return alterar_status_consulta_medico(
            db=db,
            medico_id=medico_id,
            consulta_id=consulta_id,
            novo_status=dados.status,
        )

    except LookupError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(erro),
        ) from erro

    except PermissionError as erro:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(erro),
        ) from erro

    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(erro),
        ) from erro