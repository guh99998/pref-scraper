from collections.abc import Iterable
from datetime import date, datetime


class DataInvalidaError(ValueError):
    """Data de vencimento fora do formato dd/mm/aaaa."""


def _parse(texto: str) -> date:
    try:
        return datetime.strptime(texto.strip(), "%d/%m/%Y").date()
    except ValueError as e:
        raise DataInvalidaError(f"Data de vencimento inválida: {texto!r} (esperado dd/mm/aaaa)") from e


def ha_debito_vencido(datas: Iterable[str], hoje: date) -> bool:
    """True se alguma data é anterior a `hoje`. Avalia todas e rejeita datas inválidas."""
    vencimentos = [_parse(d) for d in datas]
    return any(v < hoje for v in vencimentos)
