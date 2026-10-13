from sqlalchemy import select

from app.database.connection import SessionLocal

# Importando todos os models envolvidos para registrá-los no ORM.
from app.models.usuario import Usuario
from app.models.paciente import Paciente
from app.models.medico import Medico
from app.models.especialidade import Especialidade

db = SessionLocal()

try:
    consulta = select(Medico)

    medicos = db.scalars(consulta).all()

    if not medicos:
        print("Nenhum médico cadastrado")
    else:
        print("Médicos encontrados:\n")

        for medico in medicos:
            print(f"Médico ID: {medico.id}")
            print(f"Nome: {medico.usuario.nome_completo}")
            print(f"E-mail: {medico.usuario.email}")
            print(f"CRM: {medico.crm}/{medico.uf_crm}")
            print(f"Telefone: {medico.telefone_profissional}")

            print("Especialidades:")

            if medico.especialidades:
                for especialidade in medico.especialidades:
                    print(f"- {especialidade.nome}")
            else:
                print("- Nenhuma especialidade cadastrada")

            print("-"*50)

except Exception as erro:
    print("Erro ao consultar médicos:")
    print(erro)

finally:
    db.close()