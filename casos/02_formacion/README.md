# Escuela de Formación: reportería y conciliación

Desarrollé reportes Excel y Power BI para relacionar registros de la plataforma formativa con el CRM, explorar estados y apoyar el seguimiento. Preparé prototipos y cortes mensuales con retroalimentación de las áreas usuarias. La identificación de cuentas sin actividad para revisión no demuestra que fueran dadas de baja ni que se obtuviera un ahorro.

**Evidencia histórica:** H03–H04 y HC3-E02. Ahora se recuperaron PBIX mensuales, libros de soporte, expresiones DAX y consultas M, además de capturas de dos versiones del tablero. Ya no corresponde afirmar que todo el código original está ausente. La existencia de una expresión en un modelo no prueba su autoría individual: la atribución del trabajo se contrasta con los informes personales y la colaboración documentada.

## Cómo lo desarrollé entonces y cómo lo abordaría hoy

### Problema y solución histórica

El equipo necesitaba distinguir personas registradas, presencia en CRM, inscripción y estados de cursos. Los reportes recuperados contienen cinco tarjetas, cinco segmentaciones, tres tablas y un gráfico por vínculo. Power Query importa libros locales, promueve encabezados y transforma tipos; las fórmulas recuperadas incluyen filtros, recuentos, búsquedas por persona y cálculos mensuales. Reutilizar estructuras entre cortes facilitó la reportería.

La fortaleza fue entregar una consulta operativa por persona, curso y territorio. Las limitaciones concretas son dependencias de rutas locales y versiones mensuales, relaciones bidireccionales en un modelo recuperado y búsquedas que eligen un máximo cuando puede haber más de una afiliación. Esto exige comprobar multiplicidad; no implica que todas las filas históricas estuvieran mal.

La auditoría halló un mes incoherente en un archivo de medidas, mientras el PBIX de julio contiene el mes correcto. No se traslada el error del borrador al binario. Las comparaciones de meses y campañas no prueban causalidad, y una aprobación no se interpreta como efecto de una comunicación.

### Reconstrucción actual verificada y modelo propuesto

[**Abrir recreación independiente**](../../recuperacion/index.html) · [ETL nueva](../../src/recuperacion.py) · [datos artificiales](../../datos_recuperacion/) · [candidato Power BI](../../powerbi/recuperacion_formacion/README.md).

La recreación conserva las cinco preguntas, cinco filtros, tres vistas y distribución por vínculo. Utiliza 96 personas inventadas y 120 inscripciones artificiales en un corte fijo. Los campos identificables, nombres de cursos internos, imágenes y marcas fueron sustituidos. No se copió el código histórico al repositorio público.

El modelo nuevo contiene **DimPersona** (persona registrada, incluidas las que no inscriben cursos), **DimCurso** y **FactInscripcion** (inscripción única al corte). Resuelve la afiliación vigente por fecha; elimina una repetición idéntica y deja un conflicto simultáneo en cuarentena. La persona permanece en el universo. Para varios cortes, la [demo previa](../../disenos/02_formacion.md) conserva el hecho inscripción–corte; no se mezclan los granos.

| KPI actual | Regla |
|---|---|
| Personas registradas / con CRM / sin CRM | Universo de personas al corte; las dos últimas concilian con el total |
| Con cursos / sin cursos | Presencia de inscripción; no número de inscripciones |
| Aprobadas | Inscripciones aprobadas, incluidas las de cursos abiertos en esta vista |
| Aprobación de cursos cerrados | Solo en la demo de cohortes: aprobadas elegibles / inscripciones elegibles |

### Validación, seguridad y beneficio esperado

Se probaron duplicados, huérfanos, independencia del orden de entrada, afiliaciones futuras, conflictos y conciliación independiente SQL/Python/JavaScript. La selección vacía devuelve cero personas y ninguna fila. Las tablas y CSV de la recreación contienen solo identificadores artificiales.

El proyecto PBIR/TMSL incluye relaciones unidireccionales, M autocontenido y medidas nuevas. **Su JSON fue validado contra esquemas públicos de Microsoft; abrir, refrescar y ejecutar DAX/M en Desktop sigue pendiente.** La vista web no valida el motor de Power BI. El beneficio esperado es reducir divergencias entre cortes y explicitar denominadores; no es un resultado laboral histórico medido.
