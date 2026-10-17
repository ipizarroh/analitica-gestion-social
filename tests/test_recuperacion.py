"""Adversarial contracts and independently expressed SQL reconciliation."""
import unittest,sys,json,sqlite3,copy,random
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from recuperacion import sources,etl,query,CUT

class Reconstruction(unittest.TestCase):
    def setUp(self):self.people,self.links,self.old=sources();self.d=etl(self.people,self.links,self.old)
    def test_universe_not_enrollment_denominator(self):
        a=query(self.d);self.assertEqual((a['registrados'],a['en_crm'],a['sin_crm'],a['con_curso'],a['sin_curso'],a['inscripciones']),(96,77,19,80,16,120))
    def test_conflict_retained_without_arbitrary_assignment(self):
        self.assertEqual(self.d['Controles']['duplicados_identicos_retirados'],1)
        self.assertEqual(len(self.d['Cuarentena']),2)
        p=self.d['DimPersona'][0];self.assertEqual((p['Programa'],p['EnCRM'],p['AsignacionResuelta']),('Sin resolver',1,0))
    def test_source_order_does_not_choose_a_different_program(self):
        random.Random(9).shuffle(self.links)
        self.assertEqual(self.d['DimPersona'],etl(self.people,self.links,self.old)['DimPersona'])
    def test_future_membership_cannot_change_current_cut(self):
        self.links.append({**self.links[2],'Programa':'Future','Desde':'2099-01-01'})
        self.assertEqual(self.d['DimPersona'],etl(self.people,self.links,self.old)['DimPersona'])
    def test_duplicate_registered_person_and_orphan_are_rejected(self):
        with self.assertRaises(ValueError):etl(self.people+[self.people[0]],self.links,self.old)
        with self.assertRaises(ValueError):etl(self.people,self.links+[{**self.links[0],'PersonaID':'ORPHAN'}],self.old)
    def test_current_model_matches_materialized_data(self):
        p=Path(__file__).resolve().parents[1]/'datos_recuperacion/modelo.json';saved=json.loads(p.read_text())
        for k,v in self.d.items():self.assertEqual(saved[k],v)
    def test_independent_sql_every_registered_person_once(self):
        db=sqlite3.connect(':memory:');db.execute('create table p (PersonaID text primary key, Zona text, EnCRM int, ConCurso int)');db.executemany('insert into p values (?,?,?,?)',[(x['PersonaID'],x['Zona'],x['EnCRM'],x['ConCurso']) for x in self.d['DimPersona']]);db.execute('create table f (InscripcionID text primary key, PersonaID text, Estado text)');db.executemany('insert into f values (?,?,?)',[(x['InscripcionID'],x['PersonaID'],x['Estado']) for x in self.d['FactInscripcion']])
        for zona in [None,'Sin resolver','Zona ficticia 1','Sin CRM','ABSENT']:
            params=(zona,zona);a=query(self.d,{'Zona':zona})
            row=db.execute('select count(*),coalesce(sum(EnCRM),0),coalesce(sum(ConCurso),0) from p where (? is null or Zona=?)',params).fetchone();self.assertEqual(row,(a['registrados'],a['en_crm'],a['con_curso']))
            # Count enrollments with EXISTS; a person table never multiplies a fact row.
            row=db.execute('select count(*) from f where exists(select 1 from p where p.PersonaID=f.PersonaID and (? is null or Zona=?))',params).fetchone();self.assertEqual(row[0],a['inscripciones'])
        db.close()
    def test_unknown_filter_rejected(self):
        with self.assertRaises(ValueError):query(self.d,{'private_field':'x'})
if __name__=='__main__':unittest.main()
