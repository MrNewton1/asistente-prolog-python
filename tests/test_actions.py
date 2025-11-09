import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from actions import handle_intent

def test_action_time():
    out = handle_intent("time_now", "")
    assert "Son las " in out

def test_action_date():
    out = handle_intent("date_today", "")
    assert "Hoy es " in out
