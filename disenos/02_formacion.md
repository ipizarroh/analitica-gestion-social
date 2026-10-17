# Diseño y demo 2026 · Escuela de Formación

**Python/SQL probados; Power Query/DAX y Desktop pendientes.** Se selecciona porque separa identidad, inscripción y seguimiento y permite demostrar control temporal sin datos institucionales.

RAW artificial: personas (80), cursos (4), inscripciones (120), snapshots por corte. STAGING valida clave de inscripción, FK, estado y `corte >= fecha_inscripcion`. CURATED `FactSeguimiento`: una inscripción–corte; se agregan persona, curso y `curso_cerrado_al_corte = fin_curso <= corte`. La tabla de inscripciones es staging; no se añade una segunda ruta de filtros al modelo.

| Tabla estrella | Clave | Relación hacia hecho |
|---|---|---|
| DimPersona | persona_id | 1:* unidireccional |
| DimCurso | curso_id | 1:* unidireccional |
| DimCorte | corte | 1:* unidireccional; selección única |
| FactSeguimiento | inscripcion_id + corte | Hecho, no persona |

No se suman snapshots entre cortes. Los IDs de inscripción se repiten legítimamente en meses diferentes. `Personas` usa DISTINCTCOUNT de la clave en hecho; no sumar personas por curso. `Cobertura CRM demo` considera el catálogo ficticio de personas y no acredita identidad real.

Indicadores: inscritos al corte, personas únicas, estados, inscripciones en cursos cerrados, aprobadas entre cerradas y su razón; curso inmaduro devuelve BLANK/None. Son definiciones nuevas, no fórmulas laborales recuperadas. El estado de abril solo usa abril; no se toma el último estado de junio para reescribir historia.

`src/evolucion.py` crea datos y ejecuta ETL/medidas Python; `tests/test_evolucion.py` los concilia mediante joins SQL separados, prueba no fuga futura, no aditividad de personas y bloqueo de duplicados. Los CSV de `datos_evolucion` son los valores esperados para la validación M/DAX nativa. [Implementación M/DAX](../powerbi/evolucion/).

Contrato de actualización propuesto: misma clave/corte no se anexa dos veces; una corrección a un corte cerrado genera versión documentada. Publicar solo agregados; separar contactos y acciones sobre cuentas. RLS y refresh programado requieren diseño institucional y prueba, no se atribuyen a esta demo.

UX: corte obligatorio, curso opcional, numerador y base visibles, distribución de estados y tabla conciliada. La vista web usa estos mismos datos; su evidencia no demuestra ejecución DAX. Aceptación Desktop futura: cambiar corte a abril, verificar 109 inscripciones/74 personas y 9 aprobadas entre 30 de cursos cerrados; junio 120/80 y 61/90. Seleccionar Curso 4 en abril debe devolver sin base para aprobación.
