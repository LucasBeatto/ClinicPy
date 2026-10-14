from app.database.connection import SessionLocal
from app.security.password import verificar_senha
from app.services.usuario_service import criar_usuario
from app.models import Usuario


db = SessionLocal()

senha_original = "ClinicPy123!"

try:
    usuario = criar_usuario(
        db=db,
        nome_completo="Fernando Ribeiro",
        email="fernando.ribeiro@example.com",
        senha=senha_original,
        tipo_usuario="paciente",
    )

    print("Usuário cadastrado com sucesso!")
    print(f"ID: {usuario.id}")
    print(f"Nome: {usuario.nome_completo}")
    print(f"E-mail: {usuario.email}")
    print(f"Tipo: {usuario.tipo_usuario}")

    print(
        "Senha armazenada como hash:",
        usuario.senha_hash != senha_original
    )

    print(
        "Senha validada corretamente:",
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