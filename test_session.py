from sqlalchemy import text

from app.database.connection import SessionLocal

db = SessionLocal()

try:
    resultado = db.execute(text("SELECT DATABASE()"))
    banco = resultado.scalar()

    print("Sessão criada com sucesso!")
    print(f"Banco conectado: {banco}")

except Exception as erro:
    print("Erro ao usar a sessão:")
    print(erro)

finally:
    db.close()