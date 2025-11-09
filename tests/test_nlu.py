import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from bridge import NLUBridge

def test_greet():
    nlu = NLUBridge(kb_path=os.path.join(os.path.dirname(__file__), "..", "prolog", "nlu.pl"))
    r = nlu.parse("hola")
    assert r["intent"] == "greet"
    assert "Hola" in r["reply"]

def test_time_intent():
    nlu = NLUBridge(kb_path=os.path.join(os.path.dirname(__file__), "..", "prolog", "nlu.pl"))
    r = nlu.parse("qué hora es?")
    assert r["intent"] == "time_now"
