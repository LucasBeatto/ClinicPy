from sqlalchemy import select

from app.database.connection import SessionLocal
from app.models.usuario import Usuario


db = SessionLocal()

try:
    consulta = select(Usuario)

    usuarios = db.scalars(consulta).all()

    if not usuarios:
        print("Nenhum usuário cadastrado.")

    else:
        print("Usuários encontrados:\n")

        for usuario in usuarios:
            print(usuario)

except Exception as erro:
    print("Erro ao consultar usuários:")
    print(erro)

finally:
    db.close()