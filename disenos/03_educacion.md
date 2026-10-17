# Diseño y demo 2026 · Educación Inicial

**ETL/medidas Python y navegador probados; Power Query/DAX y Desktop pendientes.** Se selecciona por la experiencia documentada de mantenimiento de reportes y porque el universo esperado es central para interpretar asistencia. No se replica política de incentivos ni información de niños reales.

Fuentes artificiales: 4 programas abstractos, 24 matrículas ficticias, calendario de junio con fines de semana fuera y un cierre inventado, observaciones presente/ausente. No hay nombres, edad, domicilio ni documentación de identidad.

ETL: expandir matrícula vigente por cada día abierto; formar clave participante–fecha; unir observaciones por izquierda; sin coincidencia se etiqueta `Sin registro`. Rechazar observación sin jornada esperada. No imputar falta de registro como ausencia. La capacidad de programa es atributo ilustrativo y no denominador de asistencia.

Modelo estrella: DimPrograma(programa_id), DimFecha(fecha), DimParticipante(participante_id) → FactJornada(participante_id, programa_id, fecha, estado). Una dirección, tres FK. La matrícula es staging para construir expectativas, no un hecho conectado por muchos-a-muchos.

| KPI | Numerador | Denominador | Vacío |
|---|---|---|---|
| Cobertura | Presente + Ausente | Jornadas esperadas | BLANK/None |
| Asistencia observada | Presente | Presente + Ausente | BLANK/None |
| Asistencia sobre esperadas | Presente | Jornadas esperadas | BLANK/None |

El ejemplo tiene 336 jornadas esperadas: 265 presentes + 49 ausentes + 22 sin registro. Cobertura 314/336, asistencia observada 265/314; su producto concilia con 265/336. Son magnitudes inventadas, sin significado institucional.

Pruebas: duplicado participante–fecha bloqueado; observación huérfana bloqueada; cierre del 10 de junio sin denominador; suma por programa concilia total; estados exhaustivos. La demo anterior de muestreo sigue separada: una selección de apoyo no equivale a representatividad estadística.

UX: primero pendientes y cobertura, luego asistencia, tabla con bases y fecha de corte. Evitar ranking por asistencia si la cobertura es distinta. Seguridad real requeriría minimización, permisos, supresión de grupos pequeños y reglas de exportación; no se implementa RLS ficticio. Calendarista y responsable de programa aprueban correcciones; cada carga debe conciliar universo y observaciones.

Aceptación Desktop futura: cargar CSV, verificar 336/314/265, seleccionar programa y fecha, comprobar que días cerrados devuelven ausencia de base; comparar con `datos_evolucion/controles.json`. [M/DAX preparados](../powerbi/evolucion/), aún sin ejecución nativa.
