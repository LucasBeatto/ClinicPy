from sqlalchemy import text
from app.database.connection import engine

try:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    print("Conexão com o banco realizada com sucesso!")

except Exception as erro:
    print("Erro ao conectar com o banco:")
    print(erro)