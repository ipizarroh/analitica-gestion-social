# Datos completamente sintéticos · recreación 2026

Generador: `python src/recuperacion.py`. Reutiliza el generador artificial de la fase 2 y añade personas sin cursos y afiliaciones inventadas. No lee fuentes privadas ni calibra distribuciones con datos institucionales.

| Tabla | Grano y clave | Campos funcionales |
|---|---|---|
| RegistroSintetico | Persona registrada; PersonaID único | TipoVinculo artificial |
| VinculosSinteticos | Afiliación persona–fecha; puede contener conflicto | Programa, Zona, Territorio, Desde |
| DimPersona | Persona registrada al 30-06-2026 | EnCRM, ConCurso, AsignacionResuelta y afiliación |
| DimCurso | Curso artificial; CursoID | Curso y Fin |
| FactInscripcion | Inscripción única al corte; InscripcionID | PersonaID, CursoID, Estado, Cerrado |
| Cuarentena | Afiliación simultánea contradictoria | Motivo, clave y atributos inventados |

Indicadores binarios 0/1 y fechas ISO. Relaciones propuestas: DimPersona 1→N FactInscripcion y DimCurso 1→N FactInscripcion, en una dirección. Estos datos artificiales no requieren RLS; una implementación real exigiría roles y pruebas de acceso.

El ETL elimina una repetición idéntica y conserva dos afiliaciones contradictorias de una persona en cuarentena. Una afiliación anterior no reemplaza la vigente y una futura no altera el corte. La persona conflictiva conserva EnCRM=1 y continúa en el universo con Programa/Zona/Territorio «Sin resolver». «Sin CRM» es distinto.

Controles: 96 registradas = 77 con CRM + 19 sin CRM = 80 con cursos + 16 sin cursos; 120 inscripciones. Las 83 aprobadas cuentan **todos** los cursos, incluidos abiertos: no son la tasa de aprobación de cohortes maduras de la otra demo. No mezclar indicadores.

La exportación CSV contiene solo la vista artificial seleccionada. No hay correspondencia entre estos IDs y personas reales.
