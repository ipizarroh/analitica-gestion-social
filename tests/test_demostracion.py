import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from demostracion import generar_formacion,indicadores,muestrear

class ControlesGestion(unittest.TestCase):
    def test_personas_no_son_inscripciones(self):
        s=indicadores(generar_formacion())
        self.assertEqual(s['inscripciones'],96);self.assertEqual(s['personas'],53)
        self.assertAlmostEqual(s['tasa_aprobacion'],1/3)
    def test_inscripcion_duplicada_se_rechaza(self):
        f=generar_formacion()
        with self.assertRaises(ValueError):indicadores(f+[f[0]])
    def test_estado_desconocido_se_rechaza(self):
        f=generar_formacion();f[0]['estado']='Desconocido'
        with self.assertRaises(ValueError):indicadores(f)
    def test_tasa_vacia_es_ausente(self):self.assertIsNone(indicadores([])['tasa_aprobacion'])
    def test_muestra_reproducible_sin_reemplazo_y_orden_independiente(self):
        p=[{'programa':str(i%3),'registro_id':str(i)} for i in range(36)]
        a=muestrear(p,4);b=muestrear(list(reversed(p)),4)
        self.assertEqual(a,b);self.assertEqual(len(a),12);self.assertEqual(len({x['registro_id'] for x in a}),12)
        self.assertTrue(all(sum(x['programa']==g for x in a)==4 for g in ['0','1','2']))
    def test_poblacion_insuficiente_y_duplicada(self):
        p=[{'programa':'A','registro_id':'1'}]
        with self.assertRaises(ValueError):muestrear(p,2)
        with self.assertRaises(ValueError):muestrear(p+p,1)
    def test_tamano_invalido(self):
        with self.assertRaises(ValueError):muestrear([],0)

if __name__=='__main__':unittest.main()
