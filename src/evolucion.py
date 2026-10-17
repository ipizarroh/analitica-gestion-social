"""Dos recreaciones 2026 con datos inventados. Ningún insumo institucional."""
from pathlib import Path
from datetime import date,timedelta
from collections import Counter
import json,random,csv
RAIZ=Path(__file__).resolve().parents[1]
CORTES=['2026-04-30','2026-05-31','2026-06-30']


def generar(seed=20261016):
    r=random.Random(seed)
    personas=[{'persona_id':f'PERSONA_SIM_{i:03}','registro_crm_demo':i%5!=0} for i in range(1,81)]
    cursos=[{'curso_id':f'CURSO_SIM_{i}','curso':f'Curso ficticio {i}','fin':['2026-04-20','2026-05-20','2026-06-20','2026-07-20'][i-1]} for i in range(1,5)]
    inscripciones=[];seguimiento=[]
    for i in range(1,121):
        persona=personas[(i-1)%80]['persona_id'];curso=cursos[(i-1)//30]
        fecha=date(2026,3,1)+timedelta(days=r.randrange(70))
        ins={'inscripcion_id':f'INS_SIM_{i:03}','persona_id':persona,'curso_id':curso['curso_id'],'fecha_inscripcion':fecha.isoformat()};inscripciones.append(ins)
        umbral=r.randrange(15,100);abandona=r.random()<.15
        for corte in CORTES:
            dias=(date.fromisoformat(corte)-fecha).days
            if dias<0:continue
            estado='Sin avance' if dias<12 or abandona else 'Aprobado' if dias>=umbral else 'En curso'
            seguimiento.append({'inscripcion_id':ins['inscripcion_id'],'corte':corte,'estado':estado})
    programas=[{'programa_id':f'PROGRAMA_SIM_{i}','capacidad_demo':8} for i in range(1,5)]
    matricula=[{'participante_id':f'PARTICIPANTE_SIM_{i:03}','programa_id':programas[(i-1)//6]['programa_id'],'desde':'2026-06-01','hasta':'2026-06-30'} for i in range(1,25)]
    calendario=[];asistencia=[]
    for i in range(19):
        d=date(2026,6,1)+timedelta(days=i)
        if d.weekday()>4:continue
        abierto=d.day!=10 # cierre ficticio, no calendario institucional
        calendario.append({'fecha':d.isoformat(),'abierto_demo':abierto})
        if not abierto:continue
        for m in matricula:
            estado=r.choices(['Presente','Ausente',None],[76,16,8])[0]
            if estado is not None:asistencia.append({'participante_id':m['participante_id'],'fecha':d.isoformat(),'estado':estado})
    return {'naturaleza':'Recreación técnica posterior (2026), no captura histórica','seed':seed,'personas':personas,'cursos':cursos,'inscripciones':inscripciones,'seguimiento':seguimiento,'programas':programas,'matricula':matricula,'calendario':calendario,'asistencia':asistencia}


def formacion_etl(d):
    ins={x['inscripcion_id']:x for x in d['inscripciones']};cur={x['curso_id']:x for x in d['cursos']};out=[];keys=set()
    if len(ins)!=len(d['inscripciones']):raise ValueError('ID inscripción duplicado')
    for s in d['seguimiento']:
        k=(s['inscripcion_id'],s['corte'])
        if k in keys:raise ValueError('Snapshot duplicado')
        keys.add(k)
        if s['inscripcion_id'] not in ins:raise ValueError('Snapshot huérfano')
        i=ins[s['inscripcion_id']]
        if s['corte']<i['fecha_inscripcion']:raise ValueError('Snapshot anterior a inscripción')
        if s['estado'] not in ['Aprobado','En curso','Sin avance']:raise ValueError('Estado desconocido')
        out.append({**i,**s,'curso_cerrado_al_corte':cur[i['curso_id']]['fin']<=s['corte']})
    return out


def formacion(d,corte,curso=None):
    if corte not in CORTES:raise ValueError('Corte no disponible; no se extrapola')
    filas=[x for x in formacion_etl(d) if x['corte']==corte and (curso is None or x['curso_id']==curso)]
    cerradas=[x for x in filas if x['curso_cerrado_al_corte']];aprobadas=sum(x['estado']=='Aprobado' for x in cerradas)
    ids={x['persona_id'] for x in filas};crm={x['persona_id'] for x in d['personas'] if x['registro_crm_demo']}
    return {'inscripciones':len(filas),'personas':len(ids),'estados':dict(sorted(Counter(x['estado'] for x in filas).items())),'inscripciones_curso_cerrado':len(cerradas),'aprobadas_curso_cerrado':aprobadas,'aprobacion_curso_cerrado':aprobadas/len(cerradas) if cerradas else None,'personas_con_crm_demo':len(ids&crm),'cobertura_crm_demo':len(ids&crm)/len(ids) if ids else None}


def asistencia_etl(d):
    observadas={};out=[];esperadas=set()
    for a in d['asistencia']:
        key=(a['participante_id'],a['fecha'])
        if key in observadas:raise ValueError('Asistencia duplicada')
        if a['estado'] not in ['Presente','Ausente']:raise ValueError('Estado desconocido')
        observadas[key]=a['estado']
    for m in d['matricula']:
        for c in d['calendario']:
            if c['abierto_demo'] and m['desde']<=c['fecha']<=m['hasta']:
                key=(m['participante_id'],c['fecha'])
                if key in esperadas:raise ValueError('Matrícula solapada')
                esperadas.add(key)
                out.append({'participante_id':m['participante_id'],'programa_id':m['programa_id'],'fecha':c['fecha'],'estado':observadas.pop(key,None) or 'Sin registro'})
    if observadas:raise ValueError('Observación fuera de matrícula o día cerrado')
    return out


def educacion(d,programa=None,fecha=None):
    f=[x for x in asistencia_etl(d) if (not programa or x['programa_id']==programa) and (not fecha or x['fecha']==fecha)]
    estados=Counter(x['estado'] for x in f);esperados=len(f);recibidos=esperados-estados['Sin registro']
    return {'jornadas_esperadas':esperados,'registros_recibidos':recibidos,'presentes':estados['Presente'],'ausentes':estados['Ausente'],'sin_registro':estados['Sin registro'],'cobertura':recibidos/esperados if esperados else None,'asistencia_observada':estados['Presente']/recibidos if recibidos else None,'asistencia_sobre_esperadas':estados['Presente']/esperados if esperados else None}


def main():
    d=generar();p=RAIZ/'datos_evolucion';p.mkdir(exist_ok=True)
    (p/'fuentes.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
    for nombre,filas in {**{k:v for k,v in d.items() if isinstance(v,list)},'FactSeguimiento':formacion_etl(d),'FactJornada':asistencia_etl(d)}.items():
        with (p/f'{nombre}.csv').open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(filas[0]),lineterminator='\n');w.writeheader();w.writerows(filas)
    (p/'curados_web.json').write_text(json.dumps({'FactSeguimiento':formacion_etl(d),'FactJornada':asistencia_etl(d)},ensure_ascii=False,indent=2)+'\n')
    controles={'formacion':{c:formacion(d,c) for c in CORTES},'educacion':educacion(d)}
    (p/'controles.json').write_text(json.dumps(controles,ensure_ascii=False,indent=2)+'\n');print(json.dumps(controles,ensure_ascii=False))

if __name__=='__main__':main()
