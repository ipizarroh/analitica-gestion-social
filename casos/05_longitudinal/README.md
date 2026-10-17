# Trayectorias sociales: cohortes, episodios y mediciones

Construí vistas de ingresos, egresos y seguimiento sobre bases facilitadas por jefatura, con modificaciones colaborativas. No me atribuyo la construcción inicial de toda la base ni una evaluación causal de los programas.

**Evidencia histórica:** H07 y HC3-E05. A los resultados visuales del informe se suman libros con fórmulas y modelos, PBIX con árboles de descomposición y segmentaciones, documentos de criterios de filtrado y notas de reuniones de 2024. Acreditan trabajo y evolución de preguntas; su disponibilidad no prueba la autoría individual de todos los componentes ni cierre productivo.

## Cómo lo desarrollé entonces y cómo lo abordaría hoy

### Problema, solución y colaboración histórica

Se buscaba observar cómo cambiaban cohortes y condiciones a lo largo del tiempo, considerando ingreso, egreso, permanencia y mediciones sucesivas. Utilicé Excel y vistas analíticas con el equipo. El material de 2024 amplía la evidencia hacia comparación de mediciones y selección de población; las reuniones contienen decisiones y preguntas todavía abiertas.

La fortaleza fue revisar temporalidad y hacer visibles trayectorias en vez de limitarse a un total transversal. La limitación comprobada es que algunos criterios excluyen personas sin medición inicial o con una sola medición: los cambios entre pares describen una población seleccionada y no a todos los participantes. También se documentan decisiones sobre observaciones por año; no se sustituyen por una regla inventada sin aprobación de negocio.

El análisis de envejecimiento es una línea relacionada pero distinta: tiene notas propias de limpieza y preguntas sobre permanencia y deterioro. PADAM constituye otro flujo de medición, con manual y panel preexistentes; no se absorbe automáticamente dentro de este caso ni se atribuye su creación completa. Véase [material complementario](../../recuperacion_historica.md#material-complementario-y-atribución).

### Arquitectura y KPI actuales propuestos

Separaría **FactEpisodio** (persona–programa–fecha de ingreso), **FactObservacion** (episodio–fecha–instrumento) y dimensiones de programa, instrumento, fecha y persona restringida. Un reingreso generaría otro episodio. La versión del instrumento y las reglas de homologación serían explícitas.

| Pregunta / KPI | Condición necesaria |
|---|---|
| Seguimiento a una ventana | Elegibles que alcanzaron la ventana al corte; observados y no observados visibles |
| Cambio entre mediciones | Pares comparables, intervalo y número de pares; no rellenar faltantes con cero |
| Permanencia | Distinguir egreso observado de episodio vigente censurado |
| Sesgo de seguimiento | Comparar cobertura de pares entre cohortes y programas, sin conclusiones causales |

El ETL conservaría las exclusiones con motivo, normalizaría fechas, validaría secuencias y registraría instrumento/versión. No aplicaría el último estado disponible a todas las cohortes pasadas. Los faltantes y pérdidas de seguimiento se mostrarían como cobertura, no como ausencia de cambio.

### Calidad, seguridad y pruebas de aceptación

Exigiría unicidad de episodios/observaciones, ingreso <= egreso, temporalidad coherente, reingresos conservados y total de personas reconciliado con episodios sin sumarlos como equivalentes. Reproduciría cada exclusión desde RAW y compararía cálculos contra SQL independiente. Los árboles de descomposición sirven para explorar, sin demostrar impacto.

Los resultados originales y variables sociales permanecen privados. El beneficio esperado es comparar poblaciones y ventanas de forma defendible; la cobertura incompleta y los cambios de instrumentos seguirían limitando interpretaciones. **Estado: evidencia técnica recuperada y revisión retrospectiva; arquitectura propuesta, sin nueva implementación longitudinal ni validación Desktop.**
