from datetime import date, time

from pydantic import BaseModel


class HorariosDisponiveisResponse(BaseModel):
    medico_id: int
    data: date
    horarios: list[time]