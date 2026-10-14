from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import Especialidade, Medico
from app.services.usuario_service import _adicionar_usuario

def criar_medico(
        db:Session,
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
        raise ValueError("A UF do CRM deve possuir 2 caracteres.")

    if not telefone_profissional:
        raise ValueError(
            "O telefone profissional é obrigatório."
        )

    try:
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

        # Precisamos do ID do médico antes de continuar
        db.flush()

        if especialidade_ids:
            consulta = select(Especialidade).where(
                Especialidade.id.in_(especialidade_ids)
            )

            especialidades = db.scalars(consulta).all()

            if len(especialidades) != len(set(especialidade_ids)):
                raise ValueError(
                    "Uma ou mais especialidades não existem."
                )

            medico.especialidades.extend(especialidades)

        db.commit()

        db.refresh(usuario)
        db.refresh(medico)

        return usuario, medico

    except Exception:
        db.rollback()
        raise