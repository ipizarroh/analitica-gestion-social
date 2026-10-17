"""New synthetic PBIR/TMSL candidate. Static generation is not Desktop validation."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'powerbi/recuperacion_formacion'
BASE='https://developer.microsoft.com/json-schemas/fabric/item/'
def save(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def schema(path):return BASE+path+'/schema.json'
def mstr(x):return '"'+str(x).replace('"','""').replace('\n','#(lf)')+'"'
def build():
 d=json.loads((ROOT/'datos_recuperacion/modelo.json').read_text());tables=[]
 measures={
 'Personas registradas':('COALESCE(COUNTROWS(DimPersona), 0)','Personas del universo registrado, incluso sin inscripción.'),
 'Con CRM':('CALCULATE([Personas registradas], KEEPFILTERS(DimPersona[EnCRM] = 1))','Bandera al corte; no se utiliza información futura.'),
 'Sin CRM':('CALCULATE([Personas registradas], KEEPFILTERS(DimPersona[EnCRM] = 0))','No registrado en la fuente sintética CRM.'),
 'Con cursos':('CALCULATE([Personas registradas], KEEPFILTERS(DimPersona[ConCurso] = 1))','Personas, no inscripciones.'),
 'Sin cursos':('CALCULATE([Personas registradas], KEEPFILTERS(DimPersona[ConCurso] = 0))','Incluye registradas sin inscripción.'),
 'Inscripciones':('COALESCE(COUNTROWS(FactInscripcion), 0)','Grano inscripción única en un corte fijo.'),
 'Aprobadas':('CALCULATE([Inscripciones], KEEPFILTERS(FactInscripcion[Estado] = "Aprobado"))','Cuenta inscripciones aprobadas; incluye cursos aún abiertos.'),
 'En curso':('CALCULATE([Inscripciones], KEEPFILTERS(FactInscripcion[Estado] = "En curso"))','Inscripciones en curso al corte.'),
 'Sin avance':('CALCULATE([Inscripciones], KEEPFILTERS(FactInscripcion[Estado] = "Sin avance"))','Inscripciones sin avance al corte.'),
 'Estado visible':('SELECTEDVALUE(FactInscripcion[Estado])','Texto solo cuando hay un estado único; no inscripción queda BLANK.'),
 'Cobertura CRM':('DIVIDE([Con CRM], [Personas registradas])','Mismo universo registrado bajo los filtros.')}
 for name in ['DimPersona','DimCurso','FactInscripcion']:
  rows=d[name];cols=[];types=[]
  for k,v in rows[0].items():
   typ='int64' if isinstance(v,int) else 'string';cols.append({'name':k,'dataType':typ,'sourceColumn':k,'summarizeBy':'none'});types.append(mstr(k)+' = '+('Int64.Type' if typ=='int64' else 'type text'))
  m='#table(type table ['+', '.join(types)+'], {\n'+',\n'.join('    {'+', '.join(str(x) if isinstance(x,int) else mstr(x) for x in row.values())+'}' for row in rows)+'\n})'
  table={'name':name,'columns':cols,'partitions':[{'name':name,'mode':'import','source':{'type':'m','expression':m.splitlines()}}]}
  if name=='DimPersona':table['measures']=[{'name':n,'expression':e,'description':desc,'formatString':'0.0%' if n=='Cobertura CRM' else '#,0'} for n,(e,desc) in measures.items() if n!='Estado visible']
  if name=='FactInscripcion':table['measures']=[{'name':'Estado visible','expression':measures['Estado visible'][0],'description':measures['Estado visible'][1]}]
  tables.append(table)
  p=OUT/(name+'.pq');p.parent.mkdir(parents=True,exist_ok=True);p.write_text('// New synthetic table, 2026. No institutional source.\n'+m+'\n')
 model={'name':'FormacionSintetica2026','compatibilityLevel':1600,'model':{'culture':'es-CL','defaultPowerBIDataSourceVersion':'powerBI_V3','sourceQueryCulture':'es-CL','tables':tables,'relationships':[{'name':'Persona_Inscripcion','fromTable':'FactInscripcion','fromColumn':'PersonaID','fromCardinality':'many','toTable':'DimPersona','toColumn':'PersonaID','toCardinality':'one','crossFilteringBehavior':'oneDirection'},{'name':'Curso_Inscripcion','fromTable':'FactInscripcion','fromColumn':'CursoID','fromCardinality':'many','toTable':'DimCurso','toColumn':'CursoID','toCardinality':'one','crossFilteringBehavior':'oneDirection'}],'annotations':[{'name':'__PBI_TimeIntelligenceEnabled','value':'0'}]}}
 save(OUT/'Formacion.SemanticModel/model.bim',model);save(OUT/'Formacion.SemanticModel/definition.pbism',{'$schema':schema('semanticModel/definitionProperties/1.0.0'),'version':'1.0','settings':{}})
 report=OUT/'Formacion.Report';definition=report/'definition';save(report/'definition.pbir',{'$schema':schema('report/definitionProperties/2.0.0'),'version':'4.0','datasetReference':{'byPath':{'path':'../Formacion.SemanticModel'}}})
 save(OUT/'Formacion.pbip',{'version':'1.0','artifacts':[{'report':{'path':'Formacion.Report'}}],'settings':{'enableAutoRecovery':True}})
 save(definition/'version.json',{'$schema':schema('report/definition/versionMetadata/1.0.0'),'version':'4.0.0'})
 save(definition/'report.json',{'$schema':schema('report/definition/report/3.1.0'),'themeCollection':{},'annotations':[{'name':'Procedencia','value':'Recreación independiente 2026, todos los datos inventados; validación Desktop pendiente.'}]})
 save(definition/'pages/pages.json',{'$schema':schema('report/definition/pagesMetadata/1.0.0'),'pageOrder':['FormacionSintetica'],'activePageName':'FormacionSintetica'})
 page=definition/'pages/FormacionSintetica';save(page/'page.json',{'$schema':schema('report/definition/page/2.0.0'),'name':'FormacionSintetica','displayName':'Formación SINTÉTICA · Desktop pendiente','displayOption':'FitToPage','width':1440,'height':900})
 def col(table,prop):return {'field':{'Column':{'Expression':{'SourceRef':{'Entity':table}},'Property':prop}},'queryRef':table+'.'+prop,'nativeQueryRef':prop}
 def meas(prop):
  table='FactInscripcion' if prop=='Estado visible' else 'DimPersona'
  return {'field':{'Measure':{'Expression':{'SourceRef':{'Entity':table}},'Property':prop}},'queryRef':table+'.'+prop,'nativeQueryRef':prop}
 order=iter(range(1000))
 def add(name,kind,pos,roles=None,objects=None):
  v={'visualType':kind,'drillFilterOtherVisuals':True}
  if roles:v['query']={'queryState':{k:{'projections':arr} for k,arr in roles.items()}}
  if objects:v['objects']=objects
  save(page/'visuals'/name/'visual.json',{'$schema':schema('report/definition/visualContainer/2.3.0'),'name':name,'position':dict(zip(['x','y','width','height'],pos),z=0,tabOrder=next(order)),'visual':v})
 add('disclosure','textbox',[12,8,1416,48],objects={'general':[{'properties':{'paragraphs':[{'textRuns':[{'value':'RECREACIÓN INDEPENDIENTE 2026 · DATOS INVENTADOS · POWER BI DESKTOP PENDIENTE','textStyle':{'fontSize':'14pt','fontFamily':'Segoe UI'}}]}]}}]})
 for i,n in enumerate(['Personas registradas','Con CRM','Sin CRM','Con cursos','Sin cursos']):add('card'+str(i),'card',[12+i*284,64,272,95],{'Values':[meas(n)]})
 for i,n in enumerate(['Zona','Territorio','Programa','EnCRM','ConCurso']):add('slicer'+str(i),'slicer',[12+i*284,172,272,85],{'Values':[col('DimPersona',n)]})
 add('registro','tableEx',[12,270,800,285],{'Values':[col('DimPersona',n) for n in ['PersonaID','EnCRM','ConCurso','Programa','TipoVinculo']]})
 add('vinculos','clusteredBarChart',[828,270,600,285],{'Category':[col('DimPersona','TipoVinculo')],'Y':[meas('Personas registradas')]})
 add('matriz','pivotTable',[12,570,800,315],{'Rows':[col('DimPersona','PersonaID')],'Columns':[col('DimCurso','Curso')],'Values':[meas('Estado visible')]})
 add('resumen','tableEx',[828,570,600,315],{'Values':[col('DimPersona','PersonaID')]+[meas(n) for n in ['Inscripciones','Aprobadas','En curso','Sin avance']]})
 (OUT/'medidas.dax').write_text('// Código nuevo 2026; no código histórico. Validación nativa pendiente.\n'+ '\n\n'.join(n+' = '+e for n,(e,desc) in measures.items())+'\n')
if __name__=='__main__':build()
