from sqlalchemy import select

from app.database.connection import SessionLocal

from app.models.usuario import Usuario
from app.models.paciente import Paciente
from app.models.medico import Medico
from app.models.especialidade import Especialidade
from app.models.disponibilidade import Disponibilidade
from app.models.consulta import Consulta


db = SessionLocal()

try:
    consulta_sql = select(Consulta)

    consultas = db.scalars(consulta_sql).all()

    if not consultas:
        print("Nenhuma consulta cadastrada.")

    else:
        print("Consultas encontradas:\n")

        for consulta in consultas:
            print(f"Consulta ID: {consulta.id}")

            print(
                f"Paciente: "
                f"{consulta.paciente.usuario.nome_completo}"
            )

            print(
                f"Médico: "
                f"{consulta.medico.usuario.nome_completo}"
            )

            print(
                f"Especialidade: "
                f"{consulta.especialidade.nome}"
            )

            print(
                f"Data: "
                f"{consulta.data_consulta}"
            )

            print(
                f"Horário: "
                f"{consulta.horario}"
            )

            print(
                f"Status: "
                f"{consulta.status}"
            )

            print("-" * 50)

except Exception as erro:
    print("Erro ao consultar consultas:")
    print(erro)

finally:
    db.close()
