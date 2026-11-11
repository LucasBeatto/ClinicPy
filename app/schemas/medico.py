from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
)

from app.schemas.especialidade import EspecialidadeResponse
from app.schemas.usuario import UsuarioResponse

class MedicoCreate(BaseModel):
    nome_completo: str = Field(
        min_length=3,
        max_length=80
    )

    email: EmailStr

    senha: str = Field(
        min_length=8,
        max_length=128
    )

    crm: str = Field(
        min_length=1,
        max_length=10
    )

    uf_crm: str = Field(
        min_length=2,
        max_length=2
    )

    telefone_profissional: str = Field(
        min_length=8,
        max_length=20
    )

    codigo_postal: str | None = Field(
        min_length=1
    )

    especialidade_ids: list[int] = Field(
        min_length=1
    )


class MedicoDadosResponse(BaseModel):
    id: int
    usuario_id: int
    crm: str
    uf_crm: str
    telefone_profissional: str
    codigo_postal: str | None
    especialidades: list[EspecialidadeResponse]

    model_config = ConfigDict(
        from_attributes=True
    )


class MedicoResponse(BaseModel):
    usuario: UsuarioResponse
    medico: MedicoDadosResponse

class MedicoListaResponse(BaseModel):
    id: int
    crm: str
    uf_crm: str
    telefone_profissional: str
    codigo_postal: str | None

    usuario: UsuarioResponse

    especialidades: list[EspecialidadeResponse]

    model_config = ConfigDict(
        from_attributes=True
    )