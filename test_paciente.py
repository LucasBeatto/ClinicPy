from sqlalchemy import select

from app.database.connection import SessionLocal
from app.models.usuario import Usuario
from app.models.paciente import Paciente


db = SessionLocal()

try:
    consulta = select(Paciente)

    pacientes = db.scalars(consulta).all()

    if not pacientes:
        print("Nenhum paciente cadastrado.")

    else:
        print("Pacientes encontrados:\n")

        for paciente in pacientes:
            print(f"Paciente ID: {paciente.id}")
            print(f"CPF: {paciente.cpf}")
            print(f"Nome: {paciente.usuario.nome_completo}")
            print(f"E-mail: {paciente.usuario.email}")
            print("-" * 40)

except Exception as erro:
    print("Erro ao consultar pacientes:")
    print(erro)

finally:
    db.close()