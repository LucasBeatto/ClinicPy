from sqlalchemy import select

from app.database.connection import SessionLocal

from app.models.usuario import Usuario
from app.models.paciente import Paciente
from app.models.medico import Medico
from app.models.especialidade import Especialidade
from app.models.disponibilidade import Disponibilidade
from app.models.consulta import Consulta
from app.models.documento import Documento


db = SessionLocal()

try:
    consulta_sql = select(Documento)

    documentos = db.scalars(consulta_sql).all()

    if not documentos:
        print("Nenhum documento cadastrado.")

    else:
        print("Documentos encontrados:\n")

        for documento in documentos:
            print(f"Documento ID: {documento.id}")
            print(f"Tipo: {documento.tipo}")
            print(f"Arquivo: {documento.caminho_arquivo}")
            print(f"Data de envio: {documento.data_envio}")

            print(
                f"Consulta ID: "
                f"{documento.consulta.id}"
            )

            print(
                f"Paciente: "
                f"{documento.consulta.paciente.usuario.nome_completo}"
            )

            print(
                f"Médico: "
                f"{documento.consulta.medico.usuario.nome_completo}"
            )

            print(
                f"Especialidade: "
                f"{documento.consulta.especialidade.nome}"
            )

            print("-" * 50)

except Exception as erro:
    print("Erro ao consultar documentos:")
    print(erro)

finally:
    db.close()