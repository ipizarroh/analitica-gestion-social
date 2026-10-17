# Calidad y gobierno de información del CRM

Analicé categorías de instituciones, preparé una propuesta de recategorización y participé en la revisión del piloto de autorregistro diseñado por TI. El alcance acreditado es análisis, propuesta y colaboración, sin atribuirme la implementación completa del sistema ni una mejora productiva cuantificada.

**Evidencia histórica:** H05 y HC3-E03. Se recuperaron documentos específicos de propuesta, análisis de categorías y avances del autorregistro, además del informe de trabajo. El contenido permite fortalecer la descripción del razonamiento y de los intercambios con TI; no prueba que la propuesta haya sido aplicada en producción.

## Cómo lo desarrollé entonces y cómo lo abordaría hoy

### Problema, responsabilidad y solución histórica

La diversidad de categorías y el uso de grupos poco específicos dificultaban analizar la vinculación. Exploré frecuencias y actividad en Power BI, discutí alternativas de agrupación y remití una propuesta. En el piloto revisé el diseño recibido de TI con el equipo; las reglas institucionales y los detalles del formulario permanecen privados.

La fortaleza fue tratar la clasificación como una decisión de gestión y no como simple formato. La limitación comprobada de la evidencia es que no hay una bitácora de despliegue, versiones aprobadas ni mediciones antes/después que permitan demostrar beneficios operativos. Los nuevos archivos no convierten una propuesta en implementación.

### Arquitectura y mejora actual

Definiría un catálogo de categorías con propietario, versión y vigencia; una correspondencia entre valor de origen y categoría aprobada; y **FactEvaluacionCalidad** con grano registro–regla–corte. Separaría el registro de institución de los resultados de cada regla. Los valores originales se conservarían en zona restringida y las propuestas de normalización serían reversibles.

El ETL verificaría claves y cobertura de la correspondencia, detectaría solapamientos de vigencia y conservaría desconocidos en cuarentena. Una categoría «otros» puede ser legítima: no se redistribuiría automáticamente para mejorar una tasa. La aprobación del catálogo correspondería al dueño del proceso; TI operaría el despliegue y su reversión.

| KPI propuesto | Criterio de cálculo / aceptación |
|---|---|
| Cobertura de clasificación | Registros con regla válida / registros evaluados al mismo corte |
| Incumplimiento por regla | Registros distintos que fallan / registros elegibles; no contar filas de reglas como personas |
| Excepciones pendientes | Casos abiertos, antigüedad y responsable, sin nombres públicos |
| Reincidencia | Mismo defecto en cortes posteriores, controlando cambios del universo |

### Pruebas, seguridad y límites

Probaría entradas desconocidas, categorías legítimas sin actividad, versiones solapadas, reversión y conservación de claves. La conciliación exigida sería recibido = aceptado + cuarentena, sin eliminar errores silenciosamente. La vista de alertas no ejecutaría modificaciones en CRM; las acciones requerirían responsable y bitácora.

La recreación de Formación implementa un control posterior de afiliaciones ambiguas como demostración acotada de cuarentena. **No implementa ni simula el autorregistro institucional.** El resto de este caso es diseño propuesto. Su beneficio esperado es trazabilidad y consistencia; medir reducción de reprocesos exige registros de operación reales y autorización específica. Los documentos y capturas recuperados no se publican.
