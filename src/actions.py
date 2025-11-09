from datetime import datetime
from zoneinfo import ZoneInfo

MX_TZ = ZoneInfo("America/Mexico_City")

def action_time_now():
    now = datetime.now(MX_TZ)
    # Ej: "Son las 14:35 (CDMX)."
    return f"Son las {now:%H:%M} (CDMX)."

def action_date_today():
    now = datetime.now(MX_TZ)
    # Ej: "Hoy es sábado, 01 de noviembre de 2025."
    meses = ["enero","febrero","marzo","abril","mayo","junio",
             "julio","agosto","septiembre","octubre","noviembre","diciembre"]
    dias = ["lunes","martes","miércoles","jueves","viernes","sábado","domingo"]
    return f"Hoy es {dias[now.weekday()]}, {now:%d} de {meses[now.month-1]} de {now:%Y}."

ACTIONS = {
    "time_now": action_time_now,
    "date_today": action_date_today,
}

def handle_intent(intent: str, fallback_reply: str):
    """
    Si Prolog ya trae reply (no vacío), lo usamos.
    Si no, buscamos una acción dinámica por intent.
    """
    if fallback_reply:
        return fallback_reply
    fn = ACTIONS.get(intent)
    if fn:
        return fn()
    return "Por ahora no tengo una acción para esa intención."
