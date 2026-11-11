from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from app.models import Especialidade, Medico
from app.services.usuario_service import _adicionar_usuario


def criar_medico(
    db: Session,
    nome_completo: str,
    email: str,
    senha: str,
    crm: str,
    uf_crm: str,
    telefone_profissional: str,
    codigo_postal: str | None = None,
    especialidade_ids: list[int] | None = None,
) -> tuple:

    crm = crm.strip()
    uf_crm = uf_crm.strip().upper()
    telefone_profissional = telefone_profissional.strip()

    if codigo_postal:
        codigo_postal = codigo_postal.strip()

    if not crm:
        raise ValueError("O CRM é obrigatório.")

    if len(uf_crm) != 2:
        raise ValueError(
            "A UF do CRM deve possuir 2 caracteres."
        )

    if not telefone_profissional:
        raise ValueError(
            "O telefone profissional é obrigatório."
        )

    if not especialidade_ids:
        raise ValueError(
            "O médico deve possuir pelo menos uma especialidade."
        )

    try:
        consulta = select(Especialidade).where(
            Especialidade.id.in_(especialidade_ids)
        )

        especialidades = db.scalars(consulta).all()

        if len(especialidades) != len(set(especialidade_ids)):
            raise ValueError(
                "Uma ou mais especialidades informadas não existem."
            )

        usuario = _adicionar_usuario(
            db=db,
            nome_completo=nome_completo,
            email=email,
            senha=senha,
            tipo_usuario="medico",
        )

        medico = Medico(
            usuario_id=usuario.id,
            crm=crm,
            uf_crm=uf_crm,
            telefone_profissional=telefone_profissional,
            codigo_postal=codigo_postal,
        )

        db.add(medico)
        db.flush()

        medico.especialidades.extend(especialidades)

        db.commit()

        db.refresh(usuario)
        db.refresh(medico)

        return usuario, medico

    except IntegrityError as erro:
        db.rollback()

        raise ValueError(
            "Não foi possível cadastrar o médico. "
            "Verifique se o e-mail ou CRM/UF já está cadastrado."
        ) from erro

    except ValueError:
        db.rollback()
        raise

    except Exception:
        db.rollback()
        raise


def listar_medicos(
    db: Session,
    especialidade_id: int | None = None,
) -> list[Medico]:

    consulta = (
        select(Medico)
        .options(
            selectinload(Medico.usuario),
            selectinload(Medico.especialidades),
        )
        .order_by(Medico.id)
    )

    if especialidade_id is not None:
        consulta = consulta.where(
            Medico.especialidades.any(
                Especialidade.id == especialidade_id
            )
        )

    medicos = db.scalars(consulta).all()

    return list(medicos)