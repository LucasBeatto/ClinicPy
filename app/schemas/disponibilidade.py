from datetime import time

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    model_validator,
)


class DisponibilidadeCreate(BaseModel):
    dia_semana: int = Field(
        ge=1,
        le=7,
    )

    horario_inicio: time
    horario_fim: time

    duracao_consulta: int = Field(
        gt=0,
    )

    @model_validator(mode="after")
    def validar_horarios(self):
        if self.horario_inicio >= self.horario_fim:
            raise ValueError(
                "O horário inicial deve ser menor que o horário final."
            )

        return self


class DisponibilidadeResponse(BaseModel):
    id: int
    medico_id: int
    dia_semana: int
    horario_inicio: time
    horario_fim: time
    duracao_consulta: int

    model_config = ConfigDict(
        from_attributes=True
    )