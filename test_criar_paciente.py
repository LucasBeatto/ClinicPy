from datetime import date

from app.database.connection import SessionLocal
from app.security.password import verificar_senha
from app.services.paciente_service import criar_paciente


db = SessionLocal()

senha_original = "ClinicPy123!"

try:
    usuario, paciente = criar_paciente(
        db=db,
        nome_completo="Mariana Ferreira",
        email="mariana.ferreira@example.com",
        senha=senha_original,
        cpf="12345678901",
        data_nascimento=date(1995, 5, 20),
        telefone="69999999999",
        codigo_postal="76980000",
    )

    print("Paciente cadastrado com sucesso!")
    print()

    print("DADOS DO USUÁRIO")
    print(f"ID do usuário: {usuario.id}")
    print(f"Nome: {usuario.nome_completo}")
    print(f"E-mail: {usuario.email}")
    print(f"Tipo: {usuario.tipo_usuario}")

    print()

    print("DADOS DO PACIENTE")
    print(f"ID do paciente: {paciente.id}")
    print(f"Usuário relacionado: {paciente.usuario_id}")
    print(f"CPF: {paciente.cpf}")
    print(f"Nascimento: {paciente.data_nascimento}")
    print(f"Telefone: {paciente.telefone}")
    print(f"Código postal: {paciente.codigo_postal}")

    print()

    print(
        "Senha armazenada como hash:",
        usuario.senha_hash != senha_original
    )

    print(
        "Senha validada:",
        verificar_senha(
            senha_original,
            usuario.senha_hash
        )
    )

except ValueError as erro:
    print(f"Erro de validação: {erro}")

except Exception as erro:
    print(f"Erro inesperado: {erro}")

finally:
    db.close()