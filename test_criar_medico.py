from app.database.connection import SessionLocal
from app.security.password import verificar_senha
from app.services.medico_service import criar_medico
import traceback


db = SessionLocal()

senha_original = "ClinicPy123!"

try:
    usuario, medico = criar_medico(
        db=db,
        nome_completo="Carlos Henrique Souza",
        email="carlos.henrique@example.com",
        senha=senha_original,
        crm="54321",
        uf_crm="ro",
        telefone_profissional="69988887777",
        codigo_postal="76980000",
        especialidade_ids=[1, 2],
    )

    print("Médico cadastrado com sucesso!")
    print()

    print("DADOS DO USUÁRIO")
    print(f"ID do usuário: {usuario.id}")
    print(f"Nome: {usuario.nome_completo}")
    print(f"E-mail: {usuario.email}")
    print(f"Tipo: {usuario.tipo_usuario}")

    print()

    print("DADOS DO MÉDICO")
    print(f"ID do médico: {medico.id}")
    print(f"Usuário relacionado: {medico.usuario_id}")
    print(f"CRM: {medico.crm}/{medico.uf_crm}")
    print(
        f"Telefone profissional: "
        f"{medico.telefone_profissional}"
    )
    print(f"Código postal: {medico.codigo_postal}")

    print()

    print("ESPECIALIDADES")

    if medico.especialidades:
        for especialidade in medico.especialidades:
            print(
                f"- {especialidade.id}: "
                f"{especialidade.nome}"
            )
    else:
        print("Nenhuma especialidade cadastrada.")

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

except Exception:
    print(f"Erro inesperado:")
    traceback.print_exc()

finally:
    db.close()