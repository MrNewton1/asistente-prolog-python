from pyswip import Prolog

def _normalize(v):
    if isinstance(v, (bytes, bytearray)):
        return v.decode("utf-8", errors="replace")
    return v

class NLUBridge:
    def __init__(self, kb_path="prolog/nlu.pl"):
        self.prolog = Prolog()
        self.prolog.consult(kb_path)

    def parse(self, text: str):
        # escapar comillas simples para Prolog
        qtext = text.replace("'", "\\'")
        results = list(self.prolog.query(f"nlu('{qtext}', Intent, Reply)."))
        if not results:
            return {"intent": "unknown", "reply": "No entendí. Escribe 'ayuda' para ver ejemplos."}
        r = results[0]
        intent = _normalize(r["Intent"])
        reply = _normalize(r["Reply"])
        return {"intent": intent, "reply": reply}

