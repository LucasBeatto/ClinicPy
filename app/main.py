from fastapi import FastAPI

from app.routes.disponibilidade import router as disponibilidade_router
from app.routes.especialidade import router as especialidade_router
from app.routes.medico import router as medico_router
from app.routes.paciente import router as paciente_router
from app.routes.horario import router as horario_router
from app.routes.consulta import router as consulta_router


app = FastAPI(
    title="ClinicPy API",
    description=(
        "API para gerenciamento de pacientes, médicos, "
        "consultas, agendas e documentos médicos."
    ),
    version="0.1.0",
)


app.include_router(paciente_router)
app.include_router(medico_router)
app.include_router(especialidade_router)
app.include_router(disponibilidade_router)
app.include_router(horario_router)
app.include_router(consulta_router)


@app.get("/")
def raiz():
    return {
        "mensagem": "ClinicPy API funcionando."
    }