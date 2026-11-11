from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

class UsuarioResponse(BaseModel):
    id: int
    nome_completo: str
    email: EmailStr
    tipo_usuario: str
    data_cadastro: datetime

    model_config = ConfigDict(
        from_attributes=True
    )

class UsuarioResumoResponse(BaseModel):
    id: int
    nome_completo: str

    model_config = ConfigDict(
        from_attributes=True
    )