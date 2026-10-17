import assert from 'node:assert/strict';import fs from 'node:fs';import {consultar} from '../src/modelo_recuperacion.mjs';
const root=new URL('../',import.meta.url);const d=JSON.parse(fs.readFileSync(new URL('datos_recuperacion/modelo.json',root)));const refs=JSON.parse(fs.readFileSync(new URL('datos_recuperacion/controles.json',root)));let values=0;
for(const r of refs){const {personas,hechos,...a}=consultar(d,r.filtros);assert.deepEqual(a,r.resultado);assert.equal(personas.length,a.registrados);assert.equal(hechos.length,a.inscripciones);values+=Object.keys(a).length;}
console.log(`${refs.length} contextos / ${values} resultados contrastados con Python`);
