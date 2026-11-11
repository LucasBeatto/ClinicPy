from datetime import date, datetime, time

from pydantic import BaseModel, ConfigDict, Field

from typing import Literal

from app.schemas.especialidade import EspecialidadeResponse
from app.schemas.usuario import UsuarioResumoResponse

ConsultaStatus = Literal[
    "pendente",
    "confirmada",
    "recusada",
    "cancelada",
    "em_andamento",
    "finalizada",
]

NovoStatusConsulta = Literal[
    "confirmada",
    "recusada",
    "cancelada",
    "em_andamento",
    "finalizada",
]

class ConsultaStatusUpdate(BaseModel):
    status: NovoStatusConsulta

class ConsultaCreate(BaseModel):
    paciente_id: int = Field(
        gt=0,
        description="ID do paciente.",
    )

    medico_id: int = Field(
        gt=0,
        description="ID do médico.",
    )

    especialidade_id: int = Field(
        gt=0,
        description="ID da especialidade escolhida.",
    )

    data_consulta: date = Field(
        description=(
            "Data da consulta no formato AAAA-MM-DD. "
            "Exemplo: 2026-11-16."
        ),
        examples=["2026-11-16"],
    )

    horario: time = Field(
        description=(
            "Horário escolhido. "
            "Exemplo: 08:30:00."
        ),
        examples=["08:30:00"],
    )


class ConsultaResponse(BaseModel):
    id: int
    paciente_id: int
    medico_id: int
    especialidade_id: int
    data_consulta: date
    horario: time
    status: str
    data_solicitacao: datetime

    model_config = ConfigDict(
        from_attributes=True
    )

class PacienteConsultaResponse(BaseModel):
    id: int
    usuario: UsuarioResumoResponse

    model_config = ConfigDict(
        from_attributes=True
    )

class ConsultaMedicoResponse(BaseModel):
    id: int

    paciente: PacienteConsultaResponse
    especialidade: EspecialidadeResponse

    data_consulta: date
    horario: time

    status: ConsultaStatus

    data_solicitacao: datetime

    model_config = ConfigDict(
        from_attributes=True
    )

class MedicoConsultaPacienteResponse(BaseModel):
    id: int
    crm: str
    uf_crm: str
    usuario: UsuarioResumoResponse

    model_config = ConfigDict(
        from_attributes=True
    )


class ConsultaPacienteResponse(BaseModel):
    id: int

    medico: MedicoConsultaPacienteResponse
    especialidade: EspecialidadeResponse

    data_consulta: date
    horario: time
    status: ConsultaStatus
    data_solicitacao: datetime

    model_config = ConfigDict(
        from_attributes=True
    )




