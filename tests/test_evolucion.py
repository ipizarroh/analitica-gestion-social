import unittest,sys,copy,json,sqlite3
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from evolucion import generar,formacion_etl,formacion,asistencia_etl,educacion,CORTES

class Evolucion(unittest.TestCase):
    def setUp(self):self.d=generar()
    def test_reproducibilidad(self):
        self.assertEqual(self.d,generar());self.assertNotEqual(self.d,generar(1))
        self.assertEqual(json.loads((Path(__file__).resolve().parents[1]/'datos_evolucion/fuentes.json').read_text()),self.d)
    def test_granos_y_fk(self):
        f=formacion_etl(self.d);self.assertEqual(len(f),len({(x['inscripcion_id'],x['corte']) for x in f}))
        self.assertTrue({x['persona_id'] for x in f}<={x['persona_id'] for x in self.d['personas']})
        self.assertTrue({x['curso_id'] for x in f}<={x['curso_id'] for x in self.d['cursos']})
        a=asistencia_etl(self.d);self.assertEqual(len(a),336);self.assertEqual(len(a),len({(x['participante_id'],x['fecha']) for x in a}))
    def test_sql_independiente_formacion(self):
        db=sqlite3.connect(':memory:');db.execute('create table s(id text,corte text,estado text)');db.execute('create table i(id text,persona text,curso text,fecha text)');db.execute('create table c(id text,fin text)')
        db.executemany('insert into s values(:inscripcion_id,:corte,:estado)',self.d['seguimiento']);db.executemany('insert into i values(:inscripcion_id,:persona_id,:curso_id,:fecha_inscripcion)',self.d['inscripciones']);db.executemany('insert into c values(:curso_id,:fin)',self.d['cursos'])
        for corte in CORTES:
            for curso in [None,'CURSO_SIM_1','CURSO_SIM_4']:
                g=formacion(self.d,corte,curso);where='s.corte=?';params=[corte]
                if curso:where+=' and i.curso=?';params.append(curso)
                n,p,closed,passed=db.execute('select count(*),count(distinct i.persona),sum(case when c.fin<=s.corte then 1 else 0 end),sum(case when c.fin<=s.corte and s.estado="Aprobado" then 1 else 0 end) from s join i on s.id=i.id join c on i.curso=c.id where '+where,params).fetchone()
                self.assertEqual((g['inscripciones'],g['personas'],g['inscripciones_curso_cerrado'],g['aprobadas_curso_cerrado']),(n,p,closed,passed))
        db.close()
    def test_no_fuga_futura(self):
        antes=formacion(self.d,'2026-04-30');d=copy.deepcopy(self.d)
        for s in d['seguimiento']:
            if s['corte']>'2026-04-30':s['estado']='Aprobado'
        self.assertEqual(antes,formacion(d,'2026-04-30'))
        with self.assertRaises(ValueError):formacion(d,'2026-07-31')
    def test_no_suma_personas_entre_cursos(self):
        g=formacion(self.d,CORTES[-1]);suma=sum(formacion(self.d,CORTES[-1],c['curso_id'])['personas'] for c in self.d['cursos']);self.assertGreater(suma,g['personas'])
        self.assertIsNone(formacion(self.d,CORTES[0],'CURSO_SIM_4')['aprobacion_curso_cerrado'])
    def test_asistencia_ausencia_no_es_falta_registro(self):
        g=educacion(self.d);self.assertGreater(g['sin_registro'],0);self.assertEqual(g['jornadas_esperadas'],g['presentes']+g['ausentes']+g['sin_registro'])
        self.assertAlmostEqual(g['asistencia_sobre_esperadas'],g['cobertura']*g['asistencia_observada'])
        self.assertEqual(sum(educacion(self.d,p['programa_id'])['jornadas_esperadas'] for p in self.d['programas']),g['jornadas_esperadas'])
        self.assertIsNone(educacion(self.d,fecha='2026-06-10')['cobertura'])
    def test_bloqueo_duplicados_y_fuera_universo(self):
        d=copy.deepcopy(self.d);d['seguimiento'].append(d['seguimiento'][0]);self.assertRaises(ValueError,formacion_etl,d)
        d=copy.deepcopy(self.d);d['asistencia'].append({'participante_id':'NO_EXISTE','fecha':'2026-06-01','estado':'Presente'});self.assertRaises(ValueError,asistencia_etl,d)
        d=copy.deepcopy(self.d);d['matricula'].append(d['matricula'][0]);self.assertRaises(ValueError,asistencia_etl,d)

if __name__=='__main__':unittest.main()
