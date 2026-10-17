"""Reproducible independent viewer. Historical screenshots are never embedded."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
def build():
    d=json.loads((ROOT/'datos_recuperacion/modelo.json').read_text())
    js=(ROOT/'src/modelo_recuperacion.mjs').read_text().replace('export function','function')
    template=(ROOT/'src/recuperacion_plantilla.html').read_text()
    html=template.replace('/*MODEL*/',js).replace('/*DATA*/',json.dumps(d,ensure_ascii=False).replace('</','<\\/'))
    p=ROOT/'recuperacion';p.mkdir(exist_ok=True);(p/'index.html').write_text(html)
if __name__=='__main__':build()
