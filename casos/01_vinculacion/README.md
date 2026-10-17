# Vinculación institucional y Enredados

Desarrollé los prototipos de vinculación y organicé su navegación mediante botones y marcadores. Los informes recuperados describen el levantamiento de necesidades, las extracciones solicitadas al CRM, la preparación de datos, las reuniones de retroalimentación y la entrega al referente BI para la integración prevista. No tenía acceso directo autónomo al CRM en esta etapa.

**Evidencia histórica:** H01–H02 y HC3-E01. Se recuperaron documentos editables y capturas embebidas del menú territorial, detalle general, instituciones educativas y Acción Solidaria. Un PBIX de promociones confirma una vista de actividad, pero no permite atribuirle todas las páginas del informe Enredados ni recuperar sus marcadores completos. La aceptación de los prototipos está documentada; despliegue, actualización automática e impacto en convocatoria siguen sin acreditarse.

## Cómo lo desarrollé entonces y cómo lo abordaría hoy

### Problema, solución y responsabilidad histórica

Las áreas necesitaban comprender con quiénes se vinculaban y explorar información territorial sin recorrer informes aislados. Convertí requerimientos en prototipos de Power BI, preparé extractos recibidos y reuní las áreas en un menú guiado. La colaboración con BI comprendía modelamiento e integración posterior; no me atribuyo el conjunto de la plataforma institucional.

La fortaleza fue conectar preguntas de usuarios con una navegación concreta. Las capturas muestran filtros territoriales, tarjetas, tablas y botones. La limitación comprobada de la recuperación es que esas imágenes no contienen el comportamiento ejecutable de todos los botones; tampoco existe evidencia de uso productivo sostenido. La posible duplicación por relaciones múltiples se mantiene como riesgo a probar, sin declararla un defecto histórico demostrado.

### Arquitectura y mejoras actuales

Mantendría el menú por decisiones, con rutas hacia instituciones educativas, acciones solidarias y detalle. Definiría **FactActividad** (una fila por actividad), **DimOrganizacion**, **DimFecha** y **PuenteActividadOrganizacion** (una pareja única). La participación se guardaría en un hecho separado con su propio grano: sumar participantes por organización no equivale a personas únicas.

El ETL conservaría los extractos originales, tiparía fechas y claves, resolvería categorías mediante correspondencias versionadas y bloquearía relaciones sin clave. Usaría SQL o Power Query según la infraestructura disponible, sin introducir una plataforma innecesaria. Las dimensiones filtrarían hacia los hechos; las relaciones múltiples tendrían una regla explícita de asignación o una medida de actividad distinta.

| Decisión / KPI propuesto | Definición y prueba necesaria |
|---|---|
| Actividad territorial | Actividades distintas por fecha y territorio; conciliar contra IDs RAW |
| Alcance de la red | Organizaciones distintas con actividad; no sumar subtotales como si fueran disjuntos |
| Vínculos sin actividad reciente | Ventana acordada sobre vínculos vigentes; probar límites de fecha |
| Participación | Separar asistencias declaradas de personas únicas; no deducir causalidad |

### Calidad, seguridad y aceptación

Probaría que duplicar una pareja en el puente sea rechazado, que una actividad con dos organizaciones siga contando una vez en el total y que filtros/navegación conserven el contexto previsto. Identidades, contactos y localizaciones sensibles quedarían restringidos; el portafolio usaría registros inventados. No divulgaría las capturas ni el catálogo institucional.

El beneficio esperado es una lectura coherente entre páginas y menos trabajo manual; requiere validar definiciones con usuarios y medir tiempos antes/después para demostrarlo. **Estado actual: recuperación documental y visual confirmada; arquitectura propuesta.** La recreación funcional priorizada en esta fase es Formación, cuya fuente técnica es más completa. No se fabrica un Enredados nativo completo a partir de imágenes.
