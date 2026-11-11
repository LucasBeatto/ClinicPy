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
from app.schemas.paciente import (
    PacienteCreate,
    PacienteResponse
)
from app.schemas.consulta import (
    ConsultaPacienteResponse,
    ConsultaStatus,
)
from app.services.paciente_service import criar_paciente
from app.services.consulta_service import (
    listar_consultas_paciente,
    obter_consulta_paciente,
)

router = APIRouter(
    prefix="/pacientes",
    tags=["Pacientes"]
)

@router.post(
    "/",
    response_model=PacienteResponse,
    status_code=status.HTTP_201_CREATED,
)
def cadastrar_paciente(
    dados: PacienteCreate,
    db: Annotated[Session, Depends(get_db)],
):
    try:
        usuario, paciente = criar_paciente(
            db=db,
            **dados.model_dump()
        )

        return {
            "usuario": usuario,
            "paciente": paciente,
        }

    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(erro),
        )from erro


@router.get(
    "/{paciente_id}/consultas/",
    response_model=list[ConsultaPacienteResponse],
)
def obter_consultas_paciente(
    paciente_id: int,
    db: Annotated[
        Session,
        Depends(get_db),
    ],
    status_consulta: ConsultaStatus | None = Query(
        default=None,
        alias="status",
        description="Filtra as consultas pelo status.",
    ),
):
    try:
        return listar_consultas_paciente(
            db=db,
            paciente_id=paciente_id,
            status_consulta=status_consulta,
        )

    except LookupError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(erro),
        ) from erro


@router.get(
    "/{paciente_id}/consultas/{consulta_id}",
    response_model=ConsultaPacienteResponse,
)
def obter_detalhes_consulta_paciente(
    paciente_id: int,
    consulta_id: int,
    db: Annotated[
        Session,
        Depends(get_db),
    ],
):
    try:
        return obter_consulta_paciente(
            db=db,
            paciente_id=paciente_id,
            consulta_id=consulta_id,
        )

    except LookupError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(erro),
        ) from erro