:- set_prolog_flag(encoding, utf8).
:- encoding(utf8).

% --- kb.pl: base mínima de conocimiento del asistente ---

% Respuestas predefinidas por intención
reply(greet, "Hola, ¿en qué puedo ayudarte?").
reply(bye,   "¡Hasta luego!").
reply(help,  "Puedo saludar, despedirme y decir 'ayuda' en este demo.").

% Un clasificador ultra-simple por palabras clave (placeholder para NLU posterior)
% Nota: muy básico a propósito; luego lo sustituiremos por reglas mejores o ML.
intent(Text, greet) :- sub_string(Text, _, _, _, "hola"); sub_string(Text, _, _, _, "buenas").
intent(Text, bye)   :- sub_string(Text, _, _, _, "adios"); sub_string(Text, _, _, _, "adiós"); sub_string(Text, _, _, _, "bye").
intent(Text, help)  :- sub_string(Text, _, _, _, "ayuda"); sub_string(Text, _, _, _, "help").

% Predicado principal: dado un texto, encuentra intención y respuesta
respond(Text, Resp) :-
    (   intent(Text, Intent) -> reply(Intent, Resp)
    ;   Resp = "No entendí. Escribe 'ayuda' para ver qué sé hacer en este demo."
    ).
