import datetime as dt


def iso_dt_to_display(iso_date: str) -> str:
    """Convert ISO date to display date."""
    if iso_date:
        return dt.datetime.fromisoformat(iso_date).strftime("%d %b %Y")
    return ""
