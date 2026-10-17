"""Independent 2026 reconstruction grounded in a privately recovered training report.
No institutional input is read. Historical source code is never copied or executed.
"""
from pathlib import Path
from collections import Counter, defaultdict
import csv,json
from evolucion import generar,formacion_etl
ROOT=Path(__file__).resolve().parents[1]
CUT='2026-06-30'

def sources():
    old=generar()
    people=[{'PersonaID':f'PERSONA_SIM_{i:03}','TipoVinculo':['Voluntariado','Práctica'][i%2]} for i in range(1,97)]
    links=[]
    for i,p in enumerate(people,1):
        if i%5:
            links.append({'PersonaID':p['PersonaID'],'Programa':f'Programa ficticio {i%4+1}','Zona':f'Zona ficticia {i%2+1}','Territorio':f'Territorio ficticio {i%4+1}','Desde':'2026-03-01'})
    links.append(dict(links[0])) # identical repeated source row, safe deduplication
    links.append({**links[0],'Programa':'Programa en conflicto'}) # same effective date, quarantine
    links.append({**links[1],'Programa':'Programa antiguo','Desde':'2025-01-01'})
    return people,links,old

def etl(people,links,old,cut=CUT):
    if len({p['PersonaID'] for p in people})!=len(people):raise ValueError('Duplicate registered person')
    ids={p['PersonaID'] for p in people};seen=set();by=defaultdict(list);duplicates=0
    for a in links:
        if a['PersonaID'] not in ids:raise ValueError('Orphan CRM association')
        key=tuple(sorted(a.items()))
        if key in seen:duplicates+=1;continue
        seen.add(key)
        if a['Desde']<=cut:by[a['PersonaID']].append(a)
    facts=[{'InscripcionID':a['inscripcion_id'],'PersonaID':a['persona_id'],'CursoID':a['curso_id'],'Estado':a['estado'],'Cerrado':int(a['curso_cerrado_al_corte'])} for a in formacion_etl(old) if a['corte']==cut]
    if any(f['PersonaID'] not in ids for f in facts):raise ValueError('Orphan enrollment')
    enrolled={f['PersonaID'] for f in facts};dim=[];quarantine=[]
    for p in people:
        choices=by[p['PersonaID']];latest=max((a['Desde'] for a in choices),default=None)
        current=[a for a in choices if a['Desde']==latest]
        if len(current)>1:
            quarantine.extend({**a,'Motivo':'Concurrent associations require a business decision'} for a in current)
        resolved=current[0] if len(current)==1 else None
        dim.append({**p,'Programa':resolved['Programa'] if resolved else 'Sin resolver' if choices else 'Sin CRM','Zona':resolved['Zona'] if resolved else 'Sin resolver' if choices else 'Sin CRM','Territorio':resolved['Territorio'] if resolved else 'Sin resolver' if choices else 'Sin CRM','EnCRM':int(bool(choices)),'ConCurso':int(p['PersonaID'] in enrolled),'AsignacionResuelta':int(resolved is not None)})
    courses=[{'CursoID':c['curso_id'],'Curso':c['curso'],'Fin':c['fin']} for c in old['cursos']]
    return {'DimPersona':dim,'DimCurso':courses,'FactInscripcion':facts,'Cuarentena':quarantine,'Corte':cut,'Controles':{'duplicados_identicos_retirados':duplicates,'personas_asignacion_ambigua':len({a['PersonaID'] for a in quarantine}),'registros_personas':len(dim),'inscripciones':len(facts)}}

def query(d,filters=None):
    filters=filters or {}
    keys={'Zona','Territorio','Programa','EnCRM','ConCurso','TipoVinculo'}
    if set(filters)-keys:raise ValueError('Unknown filter')
    rows=[p for p in d['DimPersona'] if all(str(p[k])==str(v) for k,v in filters.items() if v is not None and v!='')]
    ids={p['PersonaID'] for p in rows};f=[x for x in d['FactInscripcion'] if x['PersonaID'] in ids]
    return {'registrados':len(rows),'en_crm':sum(x['EnCRM'] for x in rows),'sin_crm':sum(1-x['EnCRM'] for x in rows),'con_curso':sum(x['ConCurso'] for x in rows),'sin_curso':sum(1-x['ConCurso'] for x in rows),'inscripciones':len(f),'aprobadas':sum(x['Estado']=='Aprobado' for x in f),'por_vinculo':dict(sorted(Counter(x['TipoVinculo'] for x in rows).items()))}

def build():
    people,links,old=sources();d=etl(people,links,old);p=ROOT/'datos_recuperacion';p.mkdir(exist_ok=True)
    for name,rows in [('RegistroSintetico',people),('VinculosSinteticos',links)]+[(k,v) for k,v in d.items() if isinstance(v,list)]:
        with (p/(name+'.csv')).open('w',newline='') as w:
            c=csv.DictWriter(w,fieldnames=list(rows[0]),lineterminator='\n');c.writeheader();c.writerows(rows)
    d['Naturaleza']='Recreación independiente de 2026; datos completamente inventados; no Power BI Desktop'
    (p/'modelo.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
    cases=[{}, {'EnCRM':0},{'ConCurso':0},{'Zona':'Zona ficticia 1'},{'Programa':'Sin resolver'},{'Zona':'SIN_COINCIDENCIAS'},{'EnCRM':1,'ConCurso':0}]
    (p/'controles.json').write_text(json.dumps([{'filtros':f,'resultado':query(d,f)} for f in cases],ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'model':d['Controles'],'totals':query(d)},ensure_ascii=False))
    return d

if __name__=='__main__':build()
