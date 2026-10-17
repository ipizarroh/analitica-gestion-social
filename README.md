# Analítica para la gestión social · Hogar de Cristo

**Ignacio Pizarro Hurtado · Ingeniero Civil Industrial · Power BI · Excel · ETL y calidad de datos**

Durante 2022–2024 desarrollé dashboards, prototipos y análisis para áreas usuarias; colaboré con BI/TI y mantuve soluciones Excel preexistentes. Estos seis casos explican mi responsabilidad y cómo los abordaría hoy con modelamiento, SQL, Python, Power Query y DAX.

La recuperación histórica permitió examinar **21 PBIX originales y otras once copias en comprimidos: 27 versiones distintas por SHA-256**, además de libros, código R, documentos y capturas. Los originales y su trazabilidad detallada permanecen privados. El código publicado es desarrollo posterior con datos inventados, sin atribuirlo al período laboral.

## Ver el trabajo

[**Recreación de Formación basada en el reporte recuperado**](https://ipizarroh.github.io/analitica-gestion-social/recuperacion/) · [Proyecto Power BI para validar en Desktop](powerbi/recuperacion_formacion/README.md) · [Demos de cohortes y asistencia](https://ipizarroh.github.io/analitica-gestion-social/) · [Auditoría y procedencia](recuperacion_historica.md)

La recreación conserva cinco indicadores, cinco filtros, tres tablas y una distribución por vínculo. Añade resolución de afiliaciones al corte y cuarentena de conflictos. **Es una implementación web independiente de 2026; no una captura histórica ni una validación de Power BI Desktop.**

![Recreación independiente de Formación con datos inventados](imagenes/formacion_fase3_total.jpg)

## Seis casos y mi contribución

| Caso | Trabajo histórico acreditado | Evidencia y evolución actual |
|---|---|---|
| [Vinculación / Enredados](casos/01_vinculacion/README.md) | Requerimientos, extractos recibidos, prototipos y navegación propia | Documentos y capturas; modelo de actividades y relaciones múltiples propuesto |
| [Escuela de Formación](casos/02_formacion/README.md) | Reporterías, prototipos y seguimiento mensual | PBIX, DAX, M y libros; recreación funcional y candidato PBIR/TMSL |
| [Calidad CRM](casos/03_calidad_crm/README.md) | Propuesta remitida a TI; revisión colaborativa del piloto | Documentos de propuesta; reglas versionadas y cuarentena |
| [Educación Inicial](casos/04_educacion_inicial/README.md) | Actualización de libros existentes, muestreo y botones | Fórmulas, pivots y conexiones; demo de jornadas esperadas y cobertura |
| [Trayectorias](casos/05_longitudinal/README.md) | Elaboración colaborativa sobre bases facilitadas por jefatura | Libros, criterios y PBIX; episodios, pares y censura propuestos |
| [Exploración predictiva](casos/06_predictiva/README.md) | Consolidación y exploración RStudio/Power BI supervisada | R recuperado; auditoría de evaluación y propuesta para conteos por programa |

Cada caso incluye **«Cómo lo desarrollé entonces y cómo lo abordaría hoy»**. Se distingue desarrollo, colaboración, mantenimiento y propuesta. Aceptar prototipos no demuestra despliegue; identificar inactivos no acredita bajas; correlación no prueba impacto.

## Evidencia técnica reproducible

- [ETL y contratos](src/recuperacion.py): afiliación vigente, duplicados, huérfanos y conflictos sin asignación arbitraria.
- [Modelo sintético](datos_recuperacion/README.md): universo registrado separado de inscripciones y diccionario de granos.
- [DAX, M y Power BI](powerbi/recuperacion_formacion/): fuentes nuevas, relaciones unidireccionales y quince visuales PBIR.
- [Pruebas](tests/): contratos y conciliación Python/SQL; paridad JavaScript y contextos vacíos.
- [Verificación](VERIFICACION.md): JSON/PBIR validado contra esquemas públicos; ejecución DAX/M, refresh y render Desktop **pendientes**.

```bash
python src/evolucion.py
python src/construir_web.py
python src/recuperacion.py
python src/construir_recuperacion.py
python src/construir_powerbi_recuperacion.py
python -m unittest discover -s tests -v
node tests/test_web.mjs
node tests/test_recuperacion.mjs
```

La reconstrucción y documentación actuales recibieron asistencia de IA. La autoría de mis dashboards laborales, con sus colaboraciones, conserva el protagonismo. [Autoría](AUTORIA_Y_USO.md) · [Fuentes y límites](fuentes_y_limites.md) · [Correcciones](CHANGELOG.md). Portafolio personal sin afiliación ni endoso institucional.
