"""Formación y muestreo: ejemplos posteriores completamente inventados."""
import csv
import json
import random
from collections import Counter, defaultdict
from html import escape
from pathlib import Path

RAIZ=Path(__file__).resolve().parents[1]


def generar_formacion():
    return [{"inscripcion_id":f"INS-SIM-{i:03}", "persona_id":f"PER-SIM-{i%53:03}",
             "curso":f"Curso {i%4+1}", "estado":["Aprobado","En curso","Sin avance"][i%3],
             "registro_crm":int(i%5!=0)} for i in range(96)]


def indicadores(filas):
    ids=[f['inscripcion_id'] for f in filas]
    if len(set(ids))!=len(ids):raise ValueError('Inscripción duplicada')
    permitidos={'Aprobado','En curso','Sin avance'}
    if any(f['estado'] not in permitidos for f in filas):raise ValueError('Estado desconocido')
    estados=Counter(f['estado'] for f in filas)
    return {'naturaleza':'SINTÉTICO POSTERIOR','inscripciones':len(filas),
            'personas':len({f['persona_id'] for f in filas}), 'estados':dict(sorted(estados.items())),
            'tasa_aprobacion':estados['Aprobado']/len(filas) if filas else None}


def muestrear(poblacion,n_por_programa,semilla=731):
    if n_por_programa<1:raise ValueError('Tamaño debe ser positivo')
    ids=[f['registro_id'] for f in poblacion]
    if len(ids)!=len(set(ids)):raise ValueError('Registro duplicado')
    grupos=defaultdict(list)
    for f in poblacion:grupos[f['programa']].append(f)
    rng=random.Random(semilla);muestra=[]
    for programa in sorted(grupos):
        grupo=sorted(grupos[programa],key=lambda f:f['registro_id'])
        if len(grupo)<n_por_programa:raise ValueError('Programa con población insuficiente')
        muestra.extend(rng.sample(grupo,n_por_programa))
    return sorted(muestra,key=lambda f:(f['programa'],f['registro_id']))


def svg(nombre,titulo,metricas,barras,nota):
    p=['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="660" viewBox="0 0 1200 660" role="img" aria-labelledby="titulo desc">',
       '<title id="titulo">'+escape(titulo)+'</title><desc id="desc">Datos totalmente inventados, demostración posterior.</desc>',
       '<rect width="1200" height="660" fill="#F3F6FA"/>']
    def text(x,y,t,size=18,color='#16324F',bold=False):p.append(f'<text x="{x}" y="{y}" font-family="DejaVu Sans, sans-serif" font-size="{size}" fill="{color}" font-weight="{"bold" if bold else "normal"}">{escape(str(t))}</text>')
    text(40,46,'ANALÍTICA DE GESTIÓN · EJEMPLO NUEVO',16,'#146D78',True);text(40,88,titulo,29,bold=True)
    text(40,119,'DEMOSTRACIÓN SINTÉTICA POSTERIOR · sin registros ni cifras institucionales',16)
    for i,(et,val) in enumerate(metricas):
        x=40+i*378;p.append(f'<rect x="{x}" y="151" width="362" height="110" rx="12" fill="white"/>');text(x+20,184,et,16);text(x+20,230,val,30,bold=True)
    text(40,310,'Distribución de la muestra seleccionada' if nombre == 'muestreo' else 'Estados de las inscripciones inventadas',21,bold=True);maximo=max(barras.values(),default=1)
    for i,(et,n) in enumerate(barras.items()):
        y=350+i*62;w=650*n/maximo;text(40,y+24,et,18);p.append(f'<rect x="250" y="{y}" width="{w:.1f}" height="32" rx="4" fill="#3157A4"/>');text(920,y+24,n,18)
    text(40,612,nota,16);p.append('</svg>');out=RAIZ/'imagenes';out.mkdir(exist_ok=True);(out/f'{nombre}.svg').write_text('\n'.join(p)+'\n')


def guardar(nombre,filas,campos):
    out=RAIZ/'datos_sinteticos';out.mkdir(exist_ok=True)
    with (out/nombre).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=campos);w.writeheader();w.writerows(filas)


def main():
    f=generar_formacion();s=indicadores(f);guardar('formacion.csv',f,['inscripcion_id','persona_id','curso','estado','registro_crm'])
    p=[{'programa':f'Programa {i%3+1}','registro_id':f'REG-SIM-{i:03}'} for i in range(36)]
    m=muestrear(p,4);guardar('poblacion.csv',p,['programa','registro_id']);guardar('muestra.csv',m,['programa','registro_id'])
    resumen={'formacion':s,'muestreo':{'naturaleza':'SINTÉTICO POSTERIOR','semilla':731,'poblacion':len(p),'muestra':len(m),'por_programa':dict(Counter(x['programa'] for x in m))}}
    (RAIZ/'datos_sinteticos/resumen.json').write_text(json.dumps(resumen,ensure_ascii=False,indent=2)+'\n')
    svg('formacion','Formación · inscripciones y personas',[('Personas ficticias',s['personas']),('Inscripciones',s['inscripciones']),('Aprobación por inscripción',f"{s['tasa_aprobacion']:.1%}")],s['estados'],'Fuente: generador incluido. La tasa es descriptiva y no mide impacto causal.')
    svg('muestreo','Selección reproducible por programa',[('Población artificial',len(p)),('Registros seleccionados',len(m)),('Semilla del ejemplo',731)],resumen['muestreo']['por_programa'],'Muestra sin reemplazo. Tamaño ilustrativo; no es un diseño estadístico institucional.')
    print('Formación y muestra sintéticas regeneradas.')

if __name__=='__main__':main()
