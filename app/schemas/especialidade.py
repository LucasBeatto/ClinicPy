from pydantic import BaseModel, ConfigDict


class EspecialidadeResponse(BaseModel):
    id: int
    nome: str

    model_config = ConfigDict(
        from_attributes=True
    )