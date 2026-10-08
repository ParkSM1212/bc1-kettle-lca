import csv
import sys
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from audit import read_bom,purchase_mass,build_producer_index,resolve_provider,references,walk_roots

def exchange(fid, incoming=False, reference=False, provider=None, kind='PRODUCT_FLOW'):
    e={'flow':{'@id':fid,'name':fid,'flowType':kind},'amount':1,'isInput':incoming,'isQuantitativeReference':reference,'internalId':1}
    if provider:
        e['defaultProvider']={'@id':provider}
    return e

class InventoryTests(unittest.TestCase):
    def test_independent_mass_controls(self):
        bom=read_bom(Path(__file__).resolve().parents[1]/'inputs/bom.csv')
        self.assertEqual(sum(r['mass'] for r in bom if r['scope']=='Kettle'),Decimal('723'))
        self.assertEqual(sum(r['mass'] for r in bom if r['scope']=='Packaging'),Decimal('137.8'))
        self.assertEqual(len(bom),12)

    def test_missing_yield_is_not_zero(self):
        self.assertIsNone(purchase_mass(Decimal('723'),None))

    def test_purchase_mass_and_scrap(self):
        self.assertEqual(purchase_mass(Decimal('950'),Decimal('.95')),Decimal('1'))
        self.assertEqual(purchase_mass(Decimal('860.8'),Decimal('1')),Decimal('.8608'))

    def test_invalid_yields(self):
        for y in (0,-1,1.1,'NaN','Infinity'):
            with self.subTest(y=y),self.assertRaises(ValueError):
                purchase_mass(Decimal('10'),y)

    def test_bad_bom_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'bad.csv'
            for content in ('material,finished_mass_g,scope\na,1,Kettle\na,2,Kettle\n','material,finished_mass_g,scope\na,NaN,Kettle\n','material,finished_mass_g,scope\na,1,Use\n'):
                p.write_text(content)
                with self.assertRaises(ValueError):read_bom(p)

class GraphTests(unittest.TestCase):
    def test_v2_reference_schema(self):
        self.assertEqual(len(references({'exchanges':[exchange('x',reference=True)]})),1)

    def test_explicit_missing_not_replaced_by_candidate(self):
        ps={'p':{'exchanges':[exchange('x',reference=True)]}}
        e=exchange('x',incoming=True,provider='outside')
        status,uid,_=resolve_provider(e,ps,{},build_producer_index(ps,{}))
        self.assertEqual((status,uid),('explicit_provider_outside_archive','outside'))

    def test_ambiguous_provider_not_arbitrarily_selected(self):
        ps={p:{'exchanges':[exchange('x',reference=True)]} for p in ('p1','p2')}
        result=resolve_provider(exchange('x',incoming=True),ps,{},build_producer_index(ps,{}))
        self.assertEqual(result[0],'ambiguous_provider')
        self.assertIsNone(result[1])

    def test_waste_direction(self):
        ps={'t':{'exchanges':[exchange('w',incoming=True,reference=True,kind='WASTE_FLOW')]}}
        idx=build_producer_index(ps,{})
        self.assertEqual(resolve_provider(exchange('w',kind='WASTE_FLOW'),ps,{},idx)[:2],('unique_reference_flow_candidate','t'))

    def test_coproduct_is_review_not_invalid_provider(self):
        ps={'p':{'exchanges':[exchange('main',reference=True),exchange('byproduct')]}}
        s=resolve_provider(exchange('byproduct',incoming=True,provider='p'),ps,{},build_producer_index(ps,{}))
        self.assertEqual(s[0],'explicit_coproduct_allocation_required')

    def test_avoided_output_is_not_ignored(self):
        e=exchange('x');e['isAvoidedProduct']=True
        self.assertEqual(resolve_provider(e,{}, {},{})[0],'avoided_product_requires_model_choice')

    def test_cycle_terminates_and_missing_emissions_remain_pending(self):
        ps={'a':{'name':'a','exchanges':[exchange('a',reference=True),exchange('b',incoming=True,provider='b'),exchange('co2',kind='ELEMENTARY_FLOW')]},'b':{'name':'b','exchanges':[exchange('b',reference=True),exchange('a',incoming=True,provider='a')]}}
        links,summary,elementary,flags,reached=walk_roots(['a'],ps,{'co2':{'flowType':'ELEMENTARY_FLOW'}})
        self.assertEqual(reached,{'a','b'})
        self.assertEqual(summary[0]['unresolved_provider_edges'],0)
        self.assertEqual(elementary['co2'],1)
        self.assertEqual(summary[0]['closure_status'],'structural_candidates_only')

if __name__=='__main__':unittest.main()
