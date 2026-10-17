# Recuperación histórica · fase 3

Los materiales se revisaron en privado bajo autorización de análisis con IA, sin licencia general de publicación. Originales, rutas, identidades, resultados internos, capturas y código recuperado quedan fuera de GitHub.

## Matriz pública de evidencia

| Referencia | Fuente privada y correspondencia con informe histórico | Hallazgo | Límite |
|---|---|---|---|
| HC3-E01 / H01–H02 | Informes y capturas; pp. 7–23 | Prototipos, botones y marcadores | No se recuperaron todos los marcadores ejecutables; despliegue no demostrado |
| HC3-E02 / H03–H04 | PBIX mensuales, libros y medidas; pp. 24–28, 40–43 | DAX, M, tres tablas y cinco indicadores | Componentes reutilizados; no atribuir cada línea por su presencia |
| HC3-E03 / H05 | Propuestas y notas del piloto; pp. 28–32 | Categorización y colaboración TI | Propuesta/revisión no equivale a implementación |
| HC3-E04 / H06 | Libros de asistencia y consolidado; pp. 39–46 | Fórmulas, pivots, conexiones y mantenimiento | Soluciones preexistentes; recálculo Excel pendiente |
| HC3-E05 / H07 | Libros, PBIX y notas 2024; pp. 46–50 | Seguimiento y criterios de comparación | Bases colaborativas, selección de pares y cierre parcial |
| HC3-E06 / H08 | R con cabecera nominal, informe y PBIX; pp. 32–37 | Imputación, Boruta, split y Poisson | Errores estáticos de evaluación; pronóstico no validado |

Los IDs se resuelven a archivos, SHA-256, miembros de comprimidos y localizadores en la entrega privada. El contenido original no es auditable desde este repositorio por confidencialidad; las demostraciones nuevas sí son reproducibles aquí.

Se revisaron 32 copias PBIX, 27 distintas por bytes, con 53 páginas y 384 contenedores visuales **contando versiones repetidas y grupos**. No representan 31 dashboards únicos ni contribuciones individuales. Expresiones y relaciones se recuperaron por lectura local, sin ejecutarlas ni refrescar los modelos.

## Correcciones y decisiones

1. La fase 2 no disponía de estos PBIX, bases ni scripts. La fase 3 actualiza su disponibilidad preservando el historial Git.
2. Un texto de medidas tiene un mes incoherente; una versión PBIX lo tiene correcto. Se conserva la diferencia sin generalizar el error.
3. El R mezcla conjuntos al calcular métricas y contiene objetos no definidos en el archivo. Imputación y selección previas al split requieren rediseño. El objetivo es conteo por programa; se retiró la propuesta genérica de clasificación individual de la fase 2.
4. Se contrastan informes personales y artefactos. Usuarios de modificación y fechas de importación no certifican autoría laboral.
5. No se publican código institucional ni capturas recuperadas. La recreación usa narrativa propia, diseño abstracto y código nuevo con datos artificiales.

## Recuperación visual

| Elemento histórico de Formación | Recreación independiente | Cambio explícito |
|---|---|---|
| Cinco tarjetas de conciliación | Cinco tarjetas sobre personas inventadas | Universo y denominadores explícitos |
| Zona, territorio, programa, CRM y cursos | Mismos cinco conceptos de filtro | Categorías artificiales y conflictos visibles |
| Información, cursos y resumen por persona | Tres tablas conectadas | Sin identificación ni contactos reales |
| Distribución por vínculo | Barras y cambio de agrupación | Agrupación adicional de 2026 |
| Libros locales y lógica reutilizada | ETL y candidato PBIR/TMSL reproducibles | Código nuevo sin rutas institucionales |

La comparación con imágenes originales se conserva en privado. El visor público conserva preguntas y organización funcional; no reproduce exactamente el aspecto ni acredita funcionamiento nativo del PBIX histórico.

## Material complementario y atribución

- **Envejecimiento:** notas de limpieza, permanencia y gestión; línea distinta de las cohortes, pendiente de matriz específica.
- **PADAM / garantías:** panel, libro y manual con flujo propio. La evidencia no acredita autoría integral de la solución preexistente; se conserva separado, sin presentarlo como caso completo de creación propia.
- **Ecomapas territoriales:** los documentos los vinculan expresamente con Enredados; no se duplican como séptimo caso.
- **Material académico y de terceros:** excluido como prueba de desarrollo laboral personal. Su presencia en la carpeta no acredita autoría.

## Validaciones pendientes

Abrir originales y candidato en Desktop, refrescar copias privadas, probar navegación y ejecutar DAX/M. Recalcular libros en Excel y revisar pivots. Los bloqueos de descarga y formatos se detallan por archivo en la entrega privada. No se midió rendimiento del motor nativo ni impacto operativo institucional.
