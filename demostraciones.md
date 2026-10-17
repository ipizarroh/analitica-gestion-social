# Demostraciones y evolución 2026

Las dos demos principales son Formación con snapshots y Educación Inicial con universo esperado. Son recreaciones técnicas posteriores con datos completamente inventados. No son dashboards históricos ni Power BI Desktop ejecutado.

```bash
python src/evolucion.py
python -m unittest discover -s tests -v
```

Abrir `demo/index.html` localmente permite explorar los datos sin instalar un servidor ni enviar información. `src/construir_web.py` regenera la interfaz al cambiar datos. Los CSV detallados están en `datos_evolucion/`. Los tests incluyen SQL independiente para Formación y controles de integridad, fechas y denominadores para Educación.

[Diseño Formación](disenos/02_formacion.md) · [Diseño Educación](disenos/03_educacion.md) · [Enredados, diseño sin implementación](disenos/01_enredados.md) · [M/DAX preparados](powerbi/evolucion/).

La demo anterior (`src/demostracion.py`, `datos_sinteticos/`) se conserva por historial y utilidad del muestreo. Sus SVG no representan los dashboards profesionales y ya no encabezan el portafolio. No usar ambas generaciones como un mismo dataset.

Para Power BI: importar con los M preparados, crear las dimensiones/relaciones descritas y medidas, configurar corte único y conciliar contra `datos_evolucion/controles.json`. Registrar versión, capturas, refresh y reapertura. Hasta entonces: **VALIDACIÓN DESKTOP PENDIENTE**.
