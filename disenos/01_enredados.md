# Diseño 2026 · Vinculación y Enredados

**DISEÑO; sin datos históricos, implementación o Desktop verificados.** Se selecciona por el riesgo de multiplicidad de una red institucional y la navegación histórica documentada. No se reproduce el diseño visual reservado.

| Objeto | Clave/grano | Campos mínimos | Control |
|---|---|---|---|
| FactActividad | actividad_id | fecha, tipo, estado, participantes_total | ID único, total no negativo |
| PuenteActividadOrganizacion | actividad_id + organizacion_id | rol en actividad | Pareja única y FK |
| DimOrganizacion | organizacion_id | tipo, territorio_id | Catálogo y vigencia |
| DimTerritorio | territorio_id | agrupación de gestión | No geolocalización precisa |
| DimFecha | fecha | año, mes, semana | Contigua y única |

Una actividad con 3 organizaciones sigue siendo 1 actividad. En total, sumar resultados por territorio puede sobrecontar si la actividad cruza territorios. Por eso el total se recalcula como conjunto, no suma filas territoriales. Participantes no son una medida aditiva por organización; si se requieren, se necesita participación individual autorizada o una asignación acordada.

```dax
Actividades vinculadas =
CALCULATE(
    DISTINCTCOUNT(FactActividad[actividad_id]),
    KEEPFILTERS(TREATAS(
        VALUES(PuenteActividadOrganizacion[actividad_id]),
        FactActividad[actividad_id])))
```

M propuesto: normalizar claves con `Text.Trim` y tipo texto; crear catálogos; `Table.NestedJoin` del puente contra maestros; expandir solo claves; comparar filas antes/después; cuarentenar huérfanos. Nunca aplicar `Table.Distinct` indiscriminadamente a observaciones para esconder duplicados.

Pruebas de aceptación propuestas: fixture de 2 actividades y 3 instituciones, una actividad compartida; total 2 aunque la suma por institución sea 3. Filtro territorial debe restringir el puente y el conjunto de actividades. No activar caminos bidireccionales. Validar dos versiones de una organización si cambia de territorio: elegir asignación histórica o vigente y mostrarla al usuario.

Pantallas: inicio por tarea, cobertura y actividad, detalle agregado de vínculo, panel de excepciones. Filtros visibles y reinicio; tooltip de no aditividad. Pasar a implementación solo con contrato de extracción, vigencias y propósito aprobado. No se afirma que estas pruebas se ejecutaron: es especificación para un futuro fixture.
