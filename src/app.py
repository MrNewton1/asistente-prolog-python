from bridge import NLUBridge
from actions import handle_intent

def main():
    nlu = NLUBridge()

    print("Asistente (paso 2) listo. Escribe algo y Enter. Ctrl+C para salir.")
    while True:
        try:
            user = input("> ").strip()
            if not user:
                continue
            result = nlu.parse(user)
            intent = result["intent"]
            reply  = result["reply"]  # puede venir vacío

            out = handle_intent(intent, reply)
            print(out)
        except (EOFError, KeyboardInterrupt):
            print("\nSaliendo. ¡Hasta luego!")
            break

if __name__ == "__main__":
    main()
