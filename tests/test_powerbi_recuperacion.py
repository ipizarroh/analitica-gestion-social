"""Static bindings/geometry only, not an M/DAX execution engine."""
import unittest,json
from pathlib import Path
P=Path(__file__).resolve().parents[1]/'powerbi/recuperacion_formacion'
class StaticModel(unittest.TestCase):
    def test_model_and_report_bindings(self):
        model=json.loads((P/'Formacion.SemanticModel/model.bim').read_text())['model'];tables={t['name']:t for t in model['tables']}
        self.assertEqual(set(tables),{'DimPersona','DimCurso','FactInscripcion'})
        for r in model['relationships']:
            self.assertEqual(r['crossFilteringBehavior'],'oneDirection')
            for side in ['from','to']:self.assertIn(r[side+'Column'],{c['name'] for c in tables[r[side+'Table']]['columns']})
        for f in (P/'Formacion.Report').rglob('visual.json'):
            v=json.loads(f.read_text());b=v['position'];self.assertGreater(b['width'],0);self.assertLessEqual(b['x']+b['width'],1440);self.assertLessEqual(b['y']+b['height'],900)
            for role in v['visual'].get('query',{}).get('queryState',{}).values():
                for pr in role['projections']:
                    kind,field=next(iter(pr['field'].items()));t=tables[field['Expression']['SourceRef']['Entity']];names={x['name'] for x in t['columns' if kind=='Column' else 'measures']};self.assertIn(field['Property'],names)
    def test_no_external_model_sources(self):
        s=(P/'Formacion.SemanticModel/model.bim').read_text()
        for token in ['File.Contents','Web.Contents','Sql.Database','C:\\Users','sharepoint.com','drive.google']:self.assertNotIn(token,s)
        self.assertEqual(len(list((P/'Formacion.Report').rglob('visual.json'))),15)
        self.assertTrue((P/'Formacion.Report/../Formacion.SemanticModel/definition.pbism').is_file())
if __name__=='__main__':unittest.main()
