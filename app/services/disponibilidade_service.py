from datetime import time

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import Disponibilidade, Medico


def criar_disponibilidade(
    db: Session,
    medico_id: int,
    dia_semana: int,
    horario_inicio: time,
    horario_fim: time,
    duracao_consulta: int,
) -> Disponibilidade:

    medico = db.get(
        Medico,
        medico_id,
    )

    if medico is None:
        raise LookupError(
            "Médico não encontrado."
        )

    minutos_inicio = (
        horario_inicio.hour * 60
        + horario_inicio.minute
    )

    minutos_fim = (
        horario_fim.hour * 60
        + horario_fim.minute
    )

    duracao_periodo = (
        minutos_fim - minutos_inicio
    )

    if duracao_consulta > duracao_periodo:
        raise ValueError(
            "A duração da consulta não pode ser "
            "maior que o período de atendimento."
        )

    consulta_conflito = (
        select(Disponibilidade)
        .where(
            Disponibilidade.medico_id == medico_id,
            Disponibilidade.dia_semana == dia_semana,
            Disponibilidade.horario_inicio < horario_fim,
            Disponibilidade.horario_fim > horario_inicio,
        )
    )

    conflito = db.scalar(
        consulta_conflito
    )

    if conflito is not None:
        raise ValueError(
            "Já existe uma disponibilidade do médico "
            "que coincide com esse horário."
        )

    disponibilidade = Disponibilidade(
        medico_id=medico_id,
        dia_semana=dia_semana,
        horario_inicio=horario_inicio,
        horario_fim=horario_fim,
        duracao_consulta=duracao_consulta,
    )

    try:
        db.add(disponibilidade)

        db.commit()

        db.refresh(disponibilidade)

        return disponibilidade

    except IntegrityError as erro:
        db.rollback()

        raise ValueError(
            "Não foi possível cadastrar a disponibilidade."
        ) from erro

    except Exception:
        db.rollback()
        raise


def listar_disponibilidades_medico(
    db: Session,
    medico_id: int,
) -> list[Disponibilidade]:

    medico = db.get(
        Medico,
        medico_id,
    )

    if medico is None:
        raise LookupError(
            "Médico não encontrado."
        )

    consulta = (
        select(Disponibilidade)
        .where(
            Disponibilidade.medico_id == medico_id
        )
        .order_by(
            Disponibilidade.dia_semana,
            Disponibilidade.horario_inicio,
        )
    )

    disponibilidades = db.scalars(
        consulta
    ).all()

    return list(disponibilidades)