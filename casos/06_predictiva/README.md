# Exploración predictiva y medición de programas

Desarrollé consolidación y exploración de información de programas con RStudio y Power BI, con supervisión y retroalimentación. Los documentos de análisis me identifican como analista y un script recuperado contiene mi nombre en su cabecera. Esta evidencia fortalece la participación acreditada, sin convertir automáticamente el modelo en una predicción validada.

**Evidencia histórica:** H08 y HC3-E06. Se recuperaron código R, documentos metodológicos, PBIX, consultas M, medidas y estructuras de datos. La referencia anterior a «ausencia de código original» queda corregida. También se corrige la evolución genérica de la fase 2: el objetivo documentado era el **conteo de practicantes y acuerdos de voluntariado por programa**, no una clasificación individual de inactividad a 60 días.

## Cómo lo desarrollé entonces y cómo lo abordaría hoy

### Problema, herramientas y fortalezas históricas

Se buscaba explorar factores relacionados con el involucramiento y formular estimaciones para programas. Consolidé variables organizativas y operativas, exploré faltantes y correlaciones y preparé vistas de Power BI con jerarquías y segmentaciones. El código recuperado incluye imputación por medias, selección Boruta, partición aleatoria y regresión Poisson. Eso concreta parte del relato histórico; no confirma árboles o redes neuronales operativos para este proyecto por el solo hecho de aparecer en materiales académicos próximos.

La fortaleza fue unir fuentes y traducir preguntas de gestión en exploración y consulta. La presencia de material universitario o de terceros dentro de la carpeta no se utiliza como autoría laboral propia.

### Limitaciones técnicas comprobadas en la revisión estática

El archivo R calcula algunas métricas mezclando predicciones del conjunto completo con observaciones de prueba, y usa objetos que no están definidos dentro de ese archivo. Imputa y selecciona variables antes de separar entrenamiento/prueba. Estos hallazgos impiden aceptar sus métricas como evaluación reproducible fuera de muestra sin recuperar el contexto de sesión y corregir el flujo.

Además, el objetivo narrado de estimar un año posterior no queda demostrado por una respuesta construida con conteos del mismo período de los predictores. Un R² no es un porcentaje de precisión ni garantiza generalización. Las correlaciones y comparaciones entre programas no prueban efectos causales. Los documentos se conservan íntegros en privado; aquí se corrige su interpretación sin publicar valores internos.

### Arquitectura, KPI y evaluación que propondría hoy

Definiría **FactProgramaPeriodo** con grano programa–año y una etiqueta de conteo en el horizonte siguiente; **DimPrograma** preservaría cambios organizativos y **FactEvaluacionModelo** registraría versión, corte, fold y métricas agregadas. No mezclaría practicantes individuales con acuerdos grupales ni beneficiarios atendidos.

Primero verificaría que existen varios períodos y fechas de disponibilidad. Si solo hay un corte transversal, entregaría análisis descriptivo o validación entre programas, sin llamarla capacidad de pronosticar el año siguiente. Una línea base simple precedería a Poisson; contrastaría dispersión, exposición y exceso de ceros antes de aumentar complejidad.

| Requisito / KPI | Prueba de aceptación |
|---|---|
| Horizonte y disponibilidad | Features conocidas al corte, etiqueta posterior observada |
| MAE y desviación Poisson | Vectores con mismos IDs y longitudes; respuesta de conteo no negativa |
| Comparación con baseline | Misma población y holdout intacto; no ajustar decisiones con test |
| Cobertura y estabilidad | Reportar faltantes, programas nuevos y error por grupos comparables |

Imputación y selección se ajustarían solo en entrenamiento dentro de cada partición. Las uniones no multiplicarían programas; el diccionario distinguiría conteos, capacidades y porcentajes. Las predicciones serían apoyo agregado a revisión humana, sin decisiones automáticas sobre prestaciones.

### Implementación actual y límites

**Se recuperó y auditó código auténtico; no se ejecutó el R histórico ni se publicaron sus predicciones.** La nueva implementación funcional elegida es Formación, por su mayor completitud y menor riesgo. Este caso queda con diagnóstico y diseño de evaluación, sin inventar un modelo posterior para aparentar rendimiento. Se requieren datos temporales coherentes, dependencias de R, respuesta futura y un experimento reproducible antes de acreditar precisión o beneficio operativo.
