from datetime import date, datetime, timedelta, time

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Consulta, Disponibilidade, Medico


STATUS_QUE_OCUPAM_HORARIO = {
    "pendente",
    "confirmada",
    "em_andamento",
}


def listar_horarios_disponiveis(
    db: Session,
    medico_id: int,
    data_consulta: date,
) -> list[time]:

    medico = db.get(
        Medico,
        medico_id,
    )

    if medico is None:
        raise LookupError(
            "Médico não encontrado."
        )

    dia_semana = data_consulta.isoweekday()

    consulta_disponibilidades = (
        select(Disponibilidade)
        .where(
            Disponibilidade.medico_id == medico_id,
            Disponibilidade.dia_semana == dia_semana,
        )
        .order_by(
            Disponibilidade.horario_inicio
        )
    )

    disponibilidades = db.scalars(
        consulta_disponibilidades
    ).all()

    horarios_gerados = []

    for disponibilidade in disponibilidades:

        horario_atual = datetime.combine(
            data_consulta,
            disponibilidade.horario_inicio,
        )

        horario_final = datetime.combine(
            data_consulta,
            disponibilidade.horario_fim,
        )

        duracao = timedelta(
            minutes=disponibilidade.duracao_consulta
        )

        while horario_atual + duracao <= horario_final:

            horarios_gerados.append(
                horario_atual.time()
            )

            horario_atual += duracao

    consulta_ocupados = (
        select(Consulta.horario)
        .where(
            Consulta.medico_id == medico_id,
            Consulta.data_consulta == data_consulta,
            Consulta.status.in_(
                STATUS_QUE_OCUPAM_HORARIO
            ),
        )
    )

    horarios_ocupados = set(
        db.scalars(
            consulta_ocupados
        ).all()
    )

    horarios_disponiveis = [
        horario
        for horario in horarios_gerados
        if horario not in horarios_ocupados
    ]

    return horarios_disponiveis