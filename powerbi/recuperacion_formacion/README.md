# Formación · candidato Power BI de 2026

**Borrador con datos inventados. JSON/PBIR validado estáticamente; Desktop, DAX, M, refresh y render nativo pendientes.** No es el PBIX laboral ni una exportación ya probada en Desktop.

Abrir `Formacion.pbip` o `Formacion.Report/definition.pbir` en Desktop compatible con PBIP/PBIR. Guardar una copia y registrar versión. M contiene tablas artificiales autocontenidas: no necesita Drive, CRM ni cuenta institucional.

`Formacion.SemanticModel/model.bim` define tres tablas, dos relaciones unidireccionales y once medidas nuevas. El informe define una página y quince visuales: aviso, cinco tarjetas, cinco slicers, tres tablas/matriz y barras. El generador reproduce los archivos desde `datos_recuperacion/modelo.json`.

```bash
python src/recuperacion.py
python src/construir_powerbi_recuperacion.py
```

## Protocolo nativo pendiente

1. Abrir y guardar sin errores; registrar compilación, advertencias y conversiones.
2. Refrescar las tres tablas M: 96 personas, 4 cursos y 120 inscripciones.
3. Comprobar tarjetas 96, 77, 19, 80, 16 y filtros contra `datos_recuperacion/controles.json`, incluidos vacío y «Sin resolver».
4. Revisar propagación de filtros y que KEEPFILTERS respete el filtro opuesto; una persona no se multiplica por sus cursos.
5. Comprobar matriz, tablas, barras, teclado y aviso sintético. La matriz de texto debe mostrar BLANK sin inscripción; aceptar solo tras probar el visual nativo.
6. Ejecutar DAX equivalente a los controles Python/SQL y conservar resultados, capturas y Performance Analyzer. Cerrar y reabrir.

Estos pasos no se ejecutaron en el entorno actual. Validar esquemas no prueba M/DAX, roles de visuales, relaciones en ejecución ni compatibilidad de una versión de Desktop.

Referencias primarias: [PBIR](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-report), [modelo semántico](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-dataset). Los esquemas Microsoft constan en `$schema` de cada JSON.
