from datetime import date

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import Paciente
from app.services.usuario_service import _adicionar_usuario

def criar_paciente(
        db: Session,
        nome_completo: str,
        email: str,
        senha: str,
        cpf: str,
        data_nascimento: date,
        telefone: str,
        codigo_postal: str | None = None,
) -> tuple:

    cpf = "".join(
        caractere
        for caractere in cpf
        if caractere.isdigit()
    )

    telefone = telefone.strip()

    if codigo_postal:
        codigo_postal = codigo_postal.strip()

    if len(cpf) != 11:
        raise ValueError(
            "O CPF deve possuir 11 dígitos."
        )

    if not telefone:
        raise ValueError(
            "O telefone é obrigatório."
        )

    try:
        usuario = _adicionar_usuario(
            db=db,
            nome_completo=nome_completo,
            email=email,
            senha=senha,
            tipo_usuario="paciente",
        )

        paciente = Paciente(
            usuario_id=usuario.id,
            cpf = cpf,
            data_nascimento=data_nascimento,
            telefone=telefone,
            codigo_postal=codigo_postal,
        )

        db.add(paciente)

        db.commit()

        db.refresh(usuario)
        db.refresh(paciente)

        return usuario, paciente

    except IntegrityError as erro:
        db.rollback()

        raise ValueError(
            "Não foi possível cadastrar o paciente."
            "Verifique se o e-mail ou CPF já está cadastrado"
        ) from erro

    except Exception:
        db.rollback()
        raise