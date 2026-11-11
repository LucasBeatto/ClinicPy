from datetime import date

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
)

from app.schemas.usuario import UsuarioResponse

class PacienteCreate(BaseModel):
    nome_completo: str = Field(
        min_length=3,
        max_length=80
    )

    email: EmailStr

    senha: str = Field(
        min_length=8,
        max_length=124
    )

    cpf: str = Field(
        min_length=11,
        max_length=14
    )

    data_nascimento: date

    telefone: str = Field(
        min_length=8,
        max_length=20
    )

    codigo_postal: str = Field(
        default=None,
        max_length=10
    )


class PacienteDadosResponse(BaseModel):
    id: int
    usuario_id: int
    cpf: str
    data_nascimento: date
    telefone: str
    codigo_postal: str | None

    model_config = ConfigDict(
        from_attributes=True
    )


class PacienteResponse(BaseModel):
    usuario: UsuarioResponse
    paciente: PacienteDadosResponse