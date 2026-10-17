// New 2026 computation over synthetic records only. Native DAX is tested separately in Desktop.
export function consultar(d, filtros={}) {
  const people=d.DimPersona.filter(p=>Object.entries(filtros).every(([k,v])=>v===''||v===null||String(p[k])===String(v)));
  const ids=new Set(people.map(p=>p.PersonaID));
  const facts=d.FactInscripcion.filter(f=>ids.has(f.PersonaID));
  const count=k=>people.reduce((n,p)=>n+Number(p[k]),0);
  const grouped={};for(const p of people)grouped[p.TipoVinculo]=(grouped[p.TipoVinculo]||0)+1;
  return {registrados:people.length,en_crm:count('EnCRM'),sin_crm:people.length-count('EnCRM'),con_curso:count('ConCurso'),sin_curso:people.length-count('ConCurso'),inscripciones:facts.length,aprobadas:facts.filter(x=>x.Estado==='Aprobado').length,por_vinculo:Object.fromEntries(Object.entries(grouped).sort()),personas:people,hechos:facts};
}
