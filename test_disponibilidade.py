from sqlalchemy import select

from app.database.connection import SessionLocal

from app.models.usuario import Usuario
from app.models.paciente import Paciente
from app.models.medico import Medico
from app.models.especialidade import Especialidade
from app.models.disponibilidade import Disponibilidade


db = SessionLocal()

try:
    consulta = select(Disponibilidade)

    disponibilidades = db.scalars(consulta).all()

    if not disponibilidades:
        print("Nenhuma disponibilidade cadastrada.")

    else:
        print("Disponibilidades encontradas:\n")

        for disponibilidade in disponibilidades:
            print(
                f"Médico: "
                f"{disponibilidade.medico.usuario.nome_completo}"
            )

            print(
                f"Dia da semana: "
                f"{disponibilidade.dia_semana}"
            )

            print(
                f"Horário: "
                f"{disponibilidade.horario_inicio} "
                f"até {disponibilidade.horario_fim}"
            )

            print(
                f"Duração das consultas: "
                f"{disponibilidade.duracao_consulta} minutos"
            )

            print("-" * 50)

except Exception as erro:
    print("Erro ao consultar disponibilidades:")
    print(erro)

finally:
    db.close()