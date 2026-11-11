from datetime import date, time

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from app.models import (
    Consulta,
    Especialidade,
    Medico,
    Paciente,
)
from app.models.associations import medico_especialidade
from app.services.horario_service import listar_horarios_disponiveis

TRANSICOES_PERMITIDAS = {
    "pendente": {
        "confirmada",
        "recusada",
        "cancelada",
    },

    "confirmada": {
        "em_andamento",
        "cancelada",
    },

    "em_andamento": {
        "finalizada",
    },

    "recusada": set(),
    "cancelada": set(),
    "finalizada": set(),
}


def criar_consulta(
    db: Session,
    paciente_id: int,
    medico_id: int,
    especialidade_id: int,
    data_consulta: date,
    horario: time,
) -> Consulta:

    if data_consulta < date.today():
        raise ValueError(
            "Não é possível agendar uma consulta em uma data passada."
        )

    try:
        # Bloqueia momentaneamente este médico durante
        # a validação do agendamento.
        consulta_medico = (
            select(Medico)
            .where(
                Medico.id == medico_id
            )
            .with_for_update()
        )

        medico = db.scalar(
            consulta_medico
        )

        if medico is None:
            raise LookupError(
                "Médico não encontrado."
            )

        paciente = db.get(
            Paciente,
            paciente_id,
        )

        if paciente is None:
            raise LookupError(
                "Paciente não encontrado."
            )

        especialidade = db.get(
            Especialidade,
            especialidade_id,
        )

        if especialidade is None:
            raise LookupError(
                "Especialidade não encontrada."
            )

        consulta_vinculo = (
            select(
                medico_especialidade.c.medico_id
            )
            .where(
                medico_especialidade.c.medico_id == medico_id,
                medico_especialidade.c.especialidade_id
                == especialidade_id,
            )
        )

        vinculo = db.scalar(
            consulta_vinculo
        )

        if vinculo is None:
            raise ValueError(
                "O médico não atende a especialidade escolhida."
            )

        horarios_disponiveis = listar_horarios_disponiveis(
            db=db,
            medico_id=medico_id,
            data_consulta=data_consulta,
        )

        if horario not in horarios_disponiveis:
            raise ValueError(
                "O horário escolhido não está disponível "
                "para esse médico nessa data."
            )

        consulta = Consulta(
            paciente_id=paciente_id,
            medico_id=medico_id,
            especialidade_id=especialidade_id,
            data_consulta=data_consulta,
            horario=horario,
            status="pendente",
        )

        db.add(consulta)

        db.commit()

        db.refresh(consulta)

        return consulta

    except IntegrityError as erro:
        db.rollback()

        raise ValueError(
            "Não foi possível agendar a consulta."
        ) from erro

    except (LookupError, ValueError):
        db.rollback()
        raise

    except Exception:
        db.rollback()
        raise


def listar_consultas_medico(
    db: Session,
    medico_id: int,
    status_consulta: str | None = None,
) -> list[Consulta]:

    medico = db.get(
        Medico,
        medico_id,
    )

    if medico is None:
        raise LookupError(
            "Médico não encontrado."
        )

    consulta = (
        select(Consulta)
        .where(
            Consulta.medico_id == medico_id
        )
        .options(
            selectinload(
                Consulta.paciente
            ).selectinload(
                Paciente.usuario
            ),
            selectinload(
                Consulta.especialidade
            ),
        )
        .order_by(
            Consulta.data_consulta,
            Consulta.horario,
        )
    )

    if status_consulta is not None:
        consulta = consulta.where(
            Consulta.status == status_consulta
        )

    consultas = db.scalars(
        consulta
    ).all()

    return list(consultas)

def alterar_status_consulta_medico(
    db: Session,
    medico_id: int,
    consulta_id: int,
    novo_status: str,
) -> Consulta:

    consulta_banco = (
        select(Consulta)
        .where(
            Consulta.id == consulta_id
        )
        .with_for_update()
    )

    consulta = db.scalar(
        consulta_banco
    )

    if consulta is None:
        db.rollback()

        raise LookupError(
            "Consulta não encontrada."
        )

    if consulta.medico_id != medico_id:
        db.rollback()

        raise PermissionError(
            "Esta consulta não pertence ao médico informado."
        )

    status_atual = consulta.status

    if novo_status == status_atual:
        db.rollback()

        raise ValueError(
            f"A consulta já está com status '{status_atual}'."
        )

    proximos_status = TRANSICOES_PERMITIDAS.get(
        status_atual,
        set(),
    )

    if novo_status not in proximos_status:

        db.rollback()

        if not proximos_status:
            raise ValueError(
                f"A consulta está '{status_atual}' "
                "e não permite mais alteração de status."
            )

        permitidos = ", ".join(
            sorted(proximos_status)
        )

        raise ValueError(
            f"Não é permitido alterar a consulta de "
            f"'{status_atual}' para '{novo_status}'. "
            f"Transições permitidas: {permitidos}."
        )

    try:
        consulta.status = novo_status

        db.commit()

        db.refresh(consulta)

        return consulta

    except Exception:
        db.rollback()
        raise

def listar_consultas_paciente(
    db: Session,
    paciente_id: int,
    status_consulta: str | None = None,
) -> list[Consulta]:

    paciente = db.get(
        Paciente,
        paciente_id,
    )

    if paciente is None:
        raise LookupError(
            "Paciente não encontrado."
        )

    consulta = (
        select(Consulta)
        .where(
            Consulta.paciente_id == paciente_id
        )
        .options(
            selectinload(
                Consulta.medico
            ).selectinload(
                Medico.usuario
            ),
            selectinload(
                Consulta.especialidade
            ),
        )
        .order_by(
            Consulta.data_consulta,
            Consulta.horario,
        )
    )

    if status_consulta is not None:
        consulta = consulta.where(
            Consulta.status == status_consulta
        )

    consultas = db.scalars(
        consulta
    ).all()

    return list(consultas)


def obter_consulta_paciente(
    db: Session,
    paciente_id: int,
    consulta_id: int,
) -> Consulta:

    paciente = db.get(
        Paciente,
        paciente_id,
    )

    if paciente is None:
        raise LookupError(
            "Paciente não encontrado."
        )

    consulta_banco = (
        select(Consulta)
        .where(
            Consulta.id == consulta_id,
            Consulta.paciente_id == paciente_id,
        )
        .options(
            selectinload(
                Consulta.medico
            ).selectinload(
                Medico.usuario
            ),
            selectinload(
                Consulta.especialidade
            ),
        )
    )

    consulta = db.scalar(
        consulta_banco
    )

    if consulta is None:
        raise LookupError(
            "Consulta não encontrada para este paciente."
        )

    return consulta