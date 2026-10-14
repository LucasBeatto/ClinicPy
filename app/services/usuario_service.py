from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import Usuario
from app.security.password import gerar_hash_senha


TIPOS_USUARIO_VALIDOS = {
    "medico",
    "paciente",
}


def _adicionar_usuario(
    db: Session,
    nome_completo: str,
    email: str,
    senha: str,
    tipo_usuario: str,
) -> Usuario:

    nome_completo = nome_completo.strip()
    email = email.strip().lower()
    tipo_usuario = tipo_usuario.strip().lower()

    if not nome_completo:
        raise ValueError("O nome completo é obrigatório.")

    if not email:
        raise ValueError("O e-mail é obrigatório.")

    if len(senha) < 8:
        raise ValueError(
            "A senha deve possuir pelo menos 8 caracteres."
        )

    if tipo_usuario not in TIPOS_USUARIO_VALIDOS:
        raise ValueError(
            "O tipo de usuário deve ser 'medico' ou 'paciente'."
        )

    usuario = Usuario(
        nome_completo=nome_completo,
        email=email,
        senha_hash=gerar_hash_senha(senha),
        tipo_usuario=tipo_usuario,
    )

    db.add(usuario)

    # Envia o INSERT para o banco sem confirmar a transação.
    # Assim conseguimos obter usuario.id e continuar trabalhando.
    db.flush()

    return usuario


def criar_usuario(
    db: Session,
    nome_completo: str,
    email: str,
    senha: str,
    tipo_usuario: str,
) -> Usuario:

    try:
        usuario = _adicionar_usuario(
            db=db,
            nome_completo=nome_completo,
            email=email,
            senha=senha,
            tipo_usuario=tipo_usuario,
        )

        db.commit()
        db.refresh(usuario)

        return usuario

    except IntegrityError as erro:
        db.rollback()

        raise ValueError(
            "Não foi possível cadastrar o usuário. "
            "Verifique se o e-mail já está cadastrado."
        ) from erro

    except Exception:
        db.rollback()
        raise