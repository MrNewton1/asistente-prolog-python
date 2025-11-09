:- set_prolog_flag(encoding, utf8).
:- encoding(utf8).

% --- NLU mínimo por palabras clave, sensible a español ---

% Normalización: pasar a minúsculas
lower_str(S, L) :- string_lower(S, L).

% Reglas de intención
intent(Text, greet) :-
    lower_str(Text, L),
    ( sub_string(L, _,_,_, "hola")
    ; sub_string(L, _,_,_, "buenas")
    ; sub_string(L, _,_,_, "qué tal")
    ).

intent(Text, bye) :-
    lower_str(Text, L),
    ( sub_string(L, _,_,_, "adios")
    ; sub_string(L, _,_,_, "adiós")
    ; sub_string(L, _,_,_, "bye")
    ; sub_string(L, _,_,_, "hasta luego")
    ).

intent(Text, help) :-
    lower_str(Text, L),
    ( sub_string(L, _,_,_, "ayuda")
    ; sub_string(L, _,_,_, "help")
    ; sub_string(L, _,_,_, "qué puedes hacer")
    ).

intent(Text, time_now) :-
    lower_str(Text, L),
    ( sub_string(L, _,_,_, "hora")
    ; sub_string(L, _,_,_, "qué hora es")
    ; sub_string(L, _,_,_, "dime la hora")
    ).

intent(Text, date_today) :-
    lower_str(Text, L),
    ( sub_string(L, _,_,_, "fecha")
    ; sub_string(L, _,_,_, "qué día es")
    ; sub_string(L, _,_,_, "dime la fecha")
    ).

% Respuestas estáticas para algunas intenciones
reply(greet, "Hola, ¿en qué puedo ayudarte?").
reply(bye,   "¡Hasta luego!").
reply(help,  "Puedo saludar, despedirme, y decirte la hora/fecha. Prueba: 'qué hora es', 'qué día es'").

% Predicado principal de NLU:
% nlu(+Texto, -Intent, -ReplyOrEmpty)
nlu(Text, Intent, Reply) :-
    (   intent(Text, Intent),
        ( reply(Intent, Reply) -> true ; Reply = "" )
    )
    -> true
    ;  (Intent = unknown, Reply = "No entendí. Escribe 'ayuda' para ver ejemplos.").
