from datetime import datetime, timezone
import pytz

BR_TZ = pytz.timezone("America/Sao_Paulo")


def to_brazil_time(dt: datetime | None):
    if dt is None:
        return None

    # garante que está em UTC
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)

    return dt.astimezone(BR_TZ)