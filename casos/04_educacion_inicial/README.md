# Educación Inicial: asistencia, actualización y apoyo al muestreo

Actualicé reportes Excel ya construidos, preparé y cargué bases, actualicé tablas dinámicas y apoyé la revisión mediante selección de participantes. Recibí capacitación de un colega para el consolidado. El informe me atribuye botones de navegación, sin atribuirme el diseño íntegro de sus cálculos o del sistema de incentivos.

**Evidencia histórica:** H06 y HC3-E04. Se recuperaron libros de asistencia y revisión, estructuras de hojas, tablas dinámicas, fórmulas y conexiones. Las imágenes originales muestran segmentadores, cobertura del registro, matrícula, asistencia y vistas trimestrales. La presencia de Power Pivot o macros en un libro no acredita que yo los haya programado.

## Cómo lo desarrollé entonces y cómo lo abordaría hoy

### Problema y trabajo histórico

El equipo requería reportes actualizados de asistencia y un consolidado para apoyar revisiones. Mi contribución consistió en mantener el flujo periódico de preparación, carga y actualización sobre soluciones preexistentes, comprender sus vistas y facilitar navegación. No decidí pagos ni elegibilidad mediante el portafolio.

La fortaleza fue sostener una operación recurrente y aprender el procedimiento con el referente del área. Las fuentes recuperadas permiten inspeccionar fórmulas y cachés de tablas dinámicas; aún no permiten certificar su recálculo nativo. El lector de modelos no pudo decodificar algunos contenedores Power Pivot por su formato de compresión. Eso limita la auditoría del extractor y no demuestra que Excel esté dañado.

La selección aleatoria está documentada, pero no se recuperó una semilla que permita reproducir exactamente la muestra histórica. No se infiere que fuera incorrecta ni representativa de un diseño formal que no está acreditado.

### Arquitectura y reglas actuales

Modelaría **FactJornadaEsperada** a grano participante–día abierto con matrícula vigente, relacionada con fecha, programa y participante restringido. Una unión izquierda incorporaría asistencia observada; `Sin registro` seguiría siendo distinto de `Ausente`. Capacidad física, matrícula y jornadas no serían denominadores intercambiables.

| KPI propuesto / implementado en demo | Denominador |
|---|---|
| Cobertura de registro | Jornadas recibidas / jornadas esperadas |
| Asistencia observada | Presentes / jornadas recibidas |
| Asistencia sobre esperadas | Presentes / jornadas esperadas |
| Completitud por programa y corte | Mismo calendario y matrícula vigente |

La [demo posterior](../../disenos/03_educacion.md) implementa ese universo con 24 participantes inventados, un cierre artificial y 336 jornadas esperadas. El calendario es una decisión sintética de la demo; no representa una política institucional. El muestreo posterior usa semilla fija, orden estable y selección sin reemplazo; no reconstruye la muestra laboral original.

### Pruebas, seguridad y aceptación

Se probaron matrícula solapada, observación fuera del universo, duplicados, faltantes y paridad del cálculo web. Para una liberación real exigiría conciliar días de funcionamiento, capacidad, matrícula y justificaciones con responsables de negocio, recalcular el libro en Excel y comparar celdas/pivots clave antes y después de actualizar. Las fórmulas leídas no equivalen a ese recálculo.

Los datos de menores, contactos, fichas y listados se mantienen privados. No se publica ni una captura censurada por defecto. El beneficio esperado es separar calidad del registro de asistencia y hacer auditable la selección; mejorar asistencia o equidad de incentivos requeriría otro diseño de evaluación. **Estado: mantenimiento histórico confirmado; demo sintética verificada en Python/SQL/JavaScript; Excel y Power BI nativos pendientes.**
