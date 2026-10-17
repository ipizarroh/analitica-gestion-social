# Analítica para la gestión social · Hogar de Cristo

**Ignacio Pizarro Hurtado · Power BI · Excel · ETL · calidad de información**

Desarrollé análisis, prototipos y dashboards para las áreas usuarias, colaboré con BI/TI y actualicé reportes preexistentes. Estos seis casos documentan mi contribución real y explican cómo abordaría hoy sus decisiones de datos y gestión. La evidencia detallada cubre principalmente junio de 2022–febrero de 2024; el vínculo continuó hasta junio de 2024 según el resumen documental. La evolución de 2026 es posterior.

![Formación: recreación técnica posterior verificada](imagenes/formacion_2026_verificada.jpg)

*Visor web con datos inventados: recreación técnica posterior (2026), no captura histórica ni Power BI Desktop.*

## Recorrido por los seis casos

| Caso | Mi contribución acreditada | Evolución 2026 |
|---|---|---|
| [Vinculación / Enredados](casos/01_vinculacion/README.md) | Requerimientos, preparación de extractos recibidos, prototipos, botones y marcadores | [Diseño profundo](disenos/01_enredados.md), control de multiplicidad |
| [Escuela de Formación](casos/02_formacion/README.md) | Reporterías y prototipos; identificación de inactividad para revisión | [Diseño y demo](disenos/02_formacion.md), snapshots y cohortes maduras |
| [Calidad CRM](casos/03_calidad_crm/README.md) | Análisis y propuesta enviada a TI; revisión colaborativa de piloto | Reglas versionadas, cuarentena y responsabilidad |
| [Educación Inicial](casos/04_educacion_inicial/README.md) | Actualización de libros previos, apoyo al muestreo y navegación propia | [Diseño y demo](disenos/03_educacion.md), universo esperado y cobertura |
| [Trayectorias longitudinales](casos/05_longitudinal/README.md) | Elaboración colaborativa sobre bases facilitadas por jefatura | Episodios, ventanas, censura y comparabilidad |
| [Exploración predictiva](casos/06_predictiva/README.md) | Cruces y exploración documentados con RStudio/Power BI | Etiqueta, fuga temporal y evaluación como propuesta; sin modelo validado |

Cada caso incluye **«¿Cómo lo abordaría hoy? Evolución técnica y profesional (2026)»**, con decisiones, datos faltantes, riesgos y aceptación. No se atribuye despliegue a la aceptación de un prototipo, bajas a la identificación de inactivos ni impacto causal a comparaciones temporales.

## Evidencia técnica actual

[**Explorar las dos demos**](https://ipizarroh.github.io/analitica-gestion-social/) · [HTML autocontenido](demo/index.html) · [DAX/M](powerbi/evolucion/) · [Datos y controles](datos_evolucion/) · [Reproducción](demostraciones.md)

Formación separa personas de inscripciones y calcula estados al corte sin usar información futura. Educación Inicial construye las jornadas esperadas y distingue ausencia de falta de registro. Las pruebas comprueban granos, FK, fechas, denominadores y conciliación; el visor permite filtrar y revisar las filas.

```bash
python src/evolucion.py
python src/construir_web.py
python -m unittest discover -s tests -v
node tests/test_web.mjs
```

Las demos Python/JavaScript son nuevas y reproducibles con datos completamente inventados. **DAX/M y Desktop: validación nativa pendiente.** No existen PBIX ni bases históricos de HC entre las fuentes recibidas. Los diseños profundos explican el modelo y sus criterios, sin presentarlos como código laboral recuperado.

[Metodología](metodologia.md) · [Fuentes y límites](fuentes_y_limites.md) · [Autoría](AUTORIA_Y_USO.md) · [Verificación](VERIFICACION.md). Portafolio personal sin afiliación o endoso institucional.
