"""Reproducible BOM validation and openLCA JSON-LD provider-readiness audit.

This program does not calculate LCIA and never converts absent impacts to zero.
Only the Python standard library is required.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import platform
import sys
import zipfile
from collections import Counter, defaultdict, deque
from decimal import Decimal, InvalidOperation
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO_URL = 'https://www.lcacommons.gov/lca-collaboration/National_Renewable_Energy_Laboratory/USLCI_Database_Public'

def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))

def write_json(path, obj):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False)+'\n', encoding='utf-8')

def write_csv(path, rows, fields=None):
    rows = list(rows)
    fields = fields or (list(rows[0]) if rows else ['status'])
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with Path(path).open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

def sha256(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        while block := f.read(1024*1024):
            h.update(block)
    return h.hexdigest()

def read_bom(path):
    with Path(path).open(encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != ['material', 'finished_mass_g', 'scope']:
            raise ValueError('BOM must have material,finished_mass_g,scope columns in that order')
        rows = list(reader)
    if not rows:
        raise ValueError('Empty BOM')
    seen = set()
    for row in rows:
        if not row['material'] or row['material'] in seen:
            raise ValueError('Missing or duplicate material')
        seen.add(row['material'])
        if row['scope'] not in ('Kettle', 'Packaging'):
            raise ValueError('Unsupported scope')
        try:
            mass = Decimal(row['finished_mass_g'])
        except InvalidOperation as e:
            raise ValueError('Invalid finished mass') from e
        if not mass.is_finite() or mass <= 0:
            raise ValueError('Finished mass must be finite and positive')
        row['mass'] = mass
    return rows

def purchase_mass(mass_g, yield_fraction):
    if yield_fraction is None:
        return None
    y = Decimal(str(yield_fraction))
    if not y.is_finite() or not Decimal(0) < y <= Decimal(1):
        raise ValueError('Yield must be in (0, 1]')
    return mass_g / Decimal(1000) / y

def load_archive(path):
    objects = defaultdict(dict)
    entries = {}
    with zipfile.ZipFile(path) as z:
        corrupt = z.testzip()
        if corrupt:
            raise ValueError('ZIP CRC failure: '+corrupt)
        for name in z.namelist():
            if not name.endswith('.json') or '/' not in name:
                continue
            kind = name.split('/')[0]
            data = z.read(name)
            obj = json.loads(data)
            uid = obj.get('@id')
            if not uid:
                continue
            if uid in objects[kind]:
                raise ValueError('Duplicate entity UUID: '+uid)
            objects[kind][uid] = obj
            entries[(kind,uid)] = {'archive_member':name,'sha256':hashlib.sha256(data).hexdigest()}
    return objects, entries

def references(process):
    return [e for e in process.get('exchanges',[]) if e.get('isQuantitativeReference',e.get('quantitativeReference',False))]

def is_reference(ex):
    return ex.get('isQuantitativeReference',ex.get('quantitativeReference',False))

def refid(obj):
    return (obj or {}).get('@id','')

def input_exchange(ex):
    return ex.get('isInput', ex.get('input',False))

def build_producer_index(processes, flows, reference_only=True):
    by_flow = defaultdict(list)
    for uid,p in processes.items():
        for e in references(p) if reference_only else p.get('exchanges',[]):
            fid=refid(e.get('flow'))
            kind=flows.get(fid,e.get('flow',{})).get('flowType')
            if (kind=='PRODUCT_FLOW' and not input_exchange(e)) or (kind=='WASTE_FLOW' and input_exchange(e)):
                if not e.get('isAvoidedProduct',False) and uid not in by_flow[fid]:
                    by_flow[fid].append(uid)
    return by_flow

def resolve_provider(ex, processes, flows, by_flow, all_by_flow=None):
    fid=refid(ex.get('flow'))
    ft=flows.get(fid,ex.get('flow',{})).get('flowType')
    if ft == 'ELEMENTARY_FLOW':
        return 'elementary', None, []
    if not ft:
        return 'unknown_flow_type',None,[]
    if ex.get('isAvoidedProduct',ex.get('avoidedProduct',False)):
        return 'avoided_product_requires_model_choice',None,[]
    requires = (ft=='PRODUCT_FLOW' and input_exchange(ex)) or (ft=='WASTE_FLOW' and not input_exchange(ex))
    if not requires:
        return 'no_provider_required',None,[]
    supplied=refid(ex.get('defaultProvider'))
    if supplied:
        if supplied not in processes:
            return 'explicit_provider_outside_archive',supplied,[]
        if supplied not in by_flow.get(fid,[]):
            offered=[e for e in processes[supplied].get('exchanges',[]) if refid(e.get('flow'))==fid and input_exchange(e)!=(ft=='PRODUCT_FLOW')]
            if offered:
                return 'explicit_coproduct_allocation_required',supplied,[supplied]
            return 'explicit_provider_reference_mismatch',supplied,by_flow.get(fid,[])
        return 'explicit_provider',supplied,[supplied]
    candidates=by_flow.get(fid,[])
    if len(candidates)==1:
        return 'unique_reference_flow_candidate',candidates[0],candidates
    if not candidates and all_by_flow and all_by_flow.get(fid):
        alternatives=all_by_flow[fid]
        if len(alternatives)==1:
            return 'unique_coproduct_allocation_required',alternatives[0],alternatives
        return 'ambiguous_coproduct_providers',None,alternatives
    return ('ambiguous_provider' if candidates else 'missing_provider'),None,candidates

def walk_roots(root_ids, processes, flows):
    """Graph diagnostics; unique-flow links are candidates, not an accepted LCA model."""
    idx=build_producer_index(processes,flows)
    all_idx=build_producer_index(processes,flows,reference_only=False)
    links=[]; summaries=[]; elementary=Counter(); flags=[]; all_reached=set()
    for root in sorted(set(root_ids)):
        queue=deque([root]); visited=set(); issues=0; link_count=0
        while queue:
            uid=queue.popleft()
            if uid in visited:
                continue
            visited.add(uid)
            p=processes[uid]
            if len(references(p))!=1:
                flags.append({'root_uuid':root,'process_uuid':uid,'issue':'reference_count','detail':len(references(p))})
            nonref_products=[e for e in p.get('exchanges',[]) if not is_reference(e) and not input_exchange(e) and flows.get(refid(e.get('flow')),e.get('flow',{})).get('flowType')=='PRODUCT_FLOW' and (e.get('amount',0)!=0 or e.get('amountFormula'))]
            if nonref_products:
                flags.append({'root_uuid':root,'process_uuid':uid,'issue':'coproduct_allocation_review','detail':len(nonref_products)})
            for e in p.get('exchanges',[]):
                if e.get('amountFormula'):
                    flags.append({'root_uuid':root,'process_uuid':uid,'issue':'formula_not_evaluated','detail':str(e['amountFormula'])})
                # A literal zero without a formula has no activity. A formula may be nonzero.
                if e.get('amount')==0 and not e.get('amountFormula'):
                    continue
                status,provider,candidates=resolve_provider(e,processes,flows,idx,all_idx)
                if status=='elementary':
                    if uid not in all_reached:
                        elementary[refid(e.get('flow'))]+=1
                    continue
                if is_reference(e) or status=='no_provider_required':
                    continue
                links.append({'root_uuid':root,'process_uuid':uid,'process_name':p.get('name'),'exchange_id':e.get('internalId'),'flow_uuid':refid(e.get('flow')),'flow_name':e.get('flow',{}).get('name'),'amount':e.get('amount'),'unit':e.get('unit',{}).get('name'),'amount_formula':e.get('amountFormula',''),'status':status,'provider_uuid':provider or '','candidates':'|'.join(sorted(candidates))})
                link_count+=1
                if status in ('explicit_provider','unique_reference_flow_candidate','explicit_coproduct_allocation_required','unique_coproduct_allocation_required'):
                    queue.append(provider)
                if status not in ('explicit_provider','unique_reference_flow_candidate'):
                    issues+=1
        all_reached.update(visited)
        summaries.append({'root_uuid':root,'reachable_process_count':len(visited),'provider_edge_count':link_count,'unresolved_provider_edges':issues,'closure_status':'failed' if issues else 'structural_candidates_only'})
    return links,summaries,elementary,flags,all_reached

def process_metadata(uid, objects, entries, manifest):
    p=objects['processes'][uid]; refs=references(p)
    e=refs[0] if len(refs)==1 else {}
    loc=p.get('location',{})
    location=objects.get('locations',{}).get(refid(loc),loc)
    doc=p.get('processDocumentation',{})
    return {
        'dataset_name':p.get('name','unknown'),'uuid':uid,'version':p.get('version','unknown'),
        'process_type':p.get('processType','unknown'),'database':'USLCI',
        'database_release':manifest['release'],'geography':location.get('name','unknown'),
        'valid_from':doc.get('validFrom','unknown'),'valid_until':doc.get('validUntil','unknown'),
        'reference_flow_name':e.get('flow',{}).get('name','unknown'),
        'reference_flow_uuid':refid(e.get('flow')) or 'unknown',
        'reference_amount':e.get('amount','unknown'),'reference_unit':e.get('unit',{}).get('name','unknown'),
        'reference_is_input':input_exchange(e),'reference_count':len(refs),
        'allocation_method':p.get('defaultAllocationMethod','unknown'),
        'source_url':'https://api.nal.usda.gov/FederalLCACommonsapi/browse/National_Renewable_Energy_Laboratory/USLCI_Database_Public/PROCESS/'+uid,
        'retrieval_date':manifest['retrieved_date'],**entries[('processes',uid)]
    }

def boundary_evidence(objects, entries, manifest, output):
    processes=objects['processes']
    bridges=[]
    for uid in ('6373ec73-ca57-47bd-8284-2f3cc25b8637','a2174501-418e-4b2e-9dbd-fa81f5f0bcc7','052c051b-b37f-4f00-9fe8-f5b2764b69c1','531f7547-3175-4114-842a-cf358fb4a10b'):
        p=processes[uid]
        meta=process_metadata(uid,objects,entries,manifest)
        for e in p.get('exchanges',[]):
            if input_exchange(e) and e.get('unit',{}).get('name')=='USD':
                bridges.append({'process_uuid':uid,'name':p['name'],'reference_amount':meta['reference_amount'],'reference_unit':meta['reference_unit'],'sector_flow':e['flow']['name'],'sector_flow_uuid':refid(e['flow']),'price_per_reference_amount':e['amount'],'currency':'USD','price_year':2012 if '2012 producer price' in p.get('description','') else 'unknown','price_basis':'producer price (dataset wording); purchaser/basic-price equivalence not verified','quantity_for_kettle':'unknown: purchase quantity/yield unresolved','status':'not_used_in_GWP','source_url':meta['source_url'],'process_sha256':meta['sha256']})
    write_csv(output/'monetary_bridge_review.csv',bridges)
    evidence=[]
    filters={
        '89a2b59a-1ca2-34f5-acc8-a8eaaa6fa870':['Polypropylene, PP; virgin resin; at plant','Electricity, AC, 120 V','Corrugated product; at mill'],
        '26f39b7c-389c-4903-8f09-6ef5e95876cc':['Material extrusion, at plant','Linear low-density polyethylene, LLDPE; virgin resin; at plant']
    }
    for uid,names in filters.items():
        p=processes[uid]; meta=process_metadata(uid,objects,entries,manifest)
        for e in p['exchanges']:
            if input_exchange(e) and e['flow']['name'] in names:
                evidence.append({'process_uuid':uid,'process_name':p['name'],'reference_amount':meta['reference_amount'],'reference_unit':meta['reference_unit'],'included_input':e['flow']['name'],'input_amount':e['amount'],'input_unit':e['unit']['name'],'provider_uuid':refid(e.get('defaultProvider')) or 'unknown','status':'boundary_evidence_only_not_baseline','source_url':meta['source_url'],'process_sha256':meta['sha256']})
    write_csv(output/'boundary_evidence.csv',evidence)

def generate(args):
    output=Path(args.out); output.mkdir(parents=True,exist_ok=True)
    study=read_json(ROOT/'inputs/study.json')
    bom=read_bom(ROOT/'inputs/bom.csv')
    total=sum((x['mass'] for x in bom),Decimal(0))
    scopes={s:sum((x['mass'] for x in bom if x['scope']==s),Decimal(0)) for s in ('Kettle','Packaging')}
    checks=[]
    for scope,value in scopes.items():
        ok=value==Decimal(str(study['expected_mass_g'][scope]))
        checks.append({'check':'mass_'+scope,'status':'pass' if ok else 'fail','detail':f'{value} g; expected {study["expected_mass_g"][scope]} g'})
    if any(c['status']=='fail' for c in checks):
        raise ValueError('BOM mass does not match study controls')
    inventory=[{'material':x['material'],'scope':x['scope'],'finished_mass_g':str(x['mass']),'finished_mass_kg':str(x['mass']/1000),'share_of_packaged_mass_pct':float(x['mass']/total*100),'purchase_mass_kg':None,'purchase_status':'unknown_yield'} for x in bom]
    write_csv(output/'inventory.csv',inventory)
    sensitivity=[]
    for y in ('1.00','0.98','0.95'):
        for s,m in {**scopes,'Packaged kettle':total}.items():
            pm=purchase_mass(m,y)
            sensitivity.append({'scope':s,'assumed_uniform_yield':y,'purchased_mass_g':float(pm*1000),'scrap_mass_g':float(pm*1000-m),'status':'mass_illustration_only_not_baseline'})
    write_csv(output/'mass_sensitivity.csv',sensitivity)
    contributions=[{'input':r['material'],'stage':r['scope'],'gwp100_kg_CO2eq':None,'status':'not_calculated'} for r in inventory]
    contributions += [{'input':s,'stage':'Manufacturing','gwp100_kg_CO2eq':None,'status':'not_calculated'} for s in ('Conversion services','Assembly electricity','Inbound transport','Scrap treatment')]
    write_csv(output/'contributions.csv',contributions)
    summary={'run_id':study['run_id'],'study_date':study['study_date'],'calculation_status':'not_calculated_incomplete_inventory','gwp100_kg_CO2eq_per_packaged_kettle':None,'gwp_top_three':None,'mass_g':{**{k:float(v) for k,v in scopes.items()},'Total':float(total)},'mass_top_three':[r['material'] for r in sorted(inventory,key=lambda r:float(r['finished_mass_g']),reverse=True)[:3]],'uncertainty_calculated':False,'mean':None,'median':None,'p05':None,'p95':None,'python_version':platform.python_version(),'runtime_os':platform.system(),'input_bom_sha256':sha256(ROOT/'inputs/bom.csv')}
    if args.archive:
        manifest=read_json(ROOT/'data/source_manifest.json')
        actual=sha256(args.archive)
        if actual!=manifest['sha256']:
            raise ValueError('Archive SHA-256 differs from pinned source manifest')
        objects,entries=load_archive(args.archive)
        processes=objects['processes']; flows=objects['flows']
        boundary_evidence(objects,entries,manifest,output)
        queries=read_json(ROOT/'inputs/search_queries.json')
        candidates=[]; query_log=[]
        for material,terms in queries.items():
            for term in terms:
                hits=[uid for uid,p in processes.items() if term.casefold() in p.get('name','').casefold()]
                query_log.append({'input':material,'query':term,'search_field':'process.name','match_mode':'case-insensitive substring','hits':len(hits),'catalog_process_count':len(processes),'status':'complete_local_scan'})
                for uid in sorted(hits):
                    candidates.append({'input':material,'query':term,**process_metadata(uid,objects,entries,manifest)})
        write_csv(output/'search_log.csv',query_log)
        write_csv(output/'search_candidates.csv',candidates)
        decisions=read_json(ROOT/'inputs/matching_decisions.json')
        mapped=[]; root_ids=[]
        for row in bom:
            d=decisions[row['material']]
            uid=d.get('candidate_uuid')
            base={'input':row['material'],'finished_mass_g':str(row['mass']),'decision':d['decision'],'rationale':d['rationale'],'alternatives':d.get('alternatives',''),'gwp_status':'not_calculated'}
            if uid:
                if uid not in processes:
                    raise ValueError('Selected UUID absent from pinned archive: '+uid)
                root_ids.append(uid)
                base.update(process_metadata(uid,objects,entries,manifest))
            mapped.append(base)
        fields=list(dict.fromkeys(k for r in mapped for k in r))
        write_csv(output/'mapping.csv',({k:r.get(k,'unknown') for k in fields} for r in mapped),fields)
        links,closure,elementary,flags,reached=walk_roots(root_ids,processes,flows)
        write_csv(output/'supplier_links.csv',links)
        write_csv(output/'supplier_closure.csv',closure)
        write_csv(output/'model_flags.csv',flags)
        write_csv(output/'elementary_flows_pending.csv',({'flow_uuid':uid,'name':flows.get(uid,{}).get('name','unknown'),'category':flows.get(uid,{}).get('category','unknown'),'exchange_occurrences':n,'characterization_status':'not_assessed_method_not_selected'} for uid,n in sorted(elementary.items())))
        write_csv(output/'reachable_process_manifest.csv',(process_metadata(uid,objects,entries,manifest) for uid in sorted(reached)))
        unique_links={(r['process_uuid'],r['exchange_id'],r['flow_uuid']):r for r in links}
        statuses=Counter(r['status'] for r in unique_links.values())
        summary.update({'archive_sha256':actual,'database_release':manifest['release'],'archive_entities':{k:len(v) for k,v in objects.items()},'candidate_roots':len(set(root_ids)),'unique_reachable_processes':len(reached),'unique_provider_edge_statuses':dict(statuses),'elementary_flow_count_in_candidate_graph':len(elementary),'uncharacterized_flow_count':None,'characterization_note':'Method not selected; count of uncharacterized flows cannot yet be evaluated.','mapping_status_counts':dict(Counter(d['decision'] for d in decisions.values()))})
        checks.extend([{'check':'archive_integrity','status':'pass','detail':'SHA-256 matches source manifest; ZIP CRC verified'}, {'check':'supplier_closure','status':'fail' if any(r['unresolved_provider_edges'] for r in closure) else 'review','detail':'See supplier_closure.csv; unique-flow links are diagnostic candidates'}, {'check':'reference_flow_metadata','status':'pass' if all(references(processes[uid]) and len(references(processes[uid]))==1 for uid in root_ids) else 'fail','detail':'One quantitative reference per candidate root; normalization not applied to LCIA'}])
    else:
        summary['background_status']='not_audited_no_archive'
        checks.append({'check':'supplier_closure','status':'not_checked','detail':'Supply --archive to audit pinned USLCI snapshot'})
    checks.extend([{'check':'g_to_kg_units','status':'pass','detail':'Decimal conversion divides every mass by 1000'}, {'check':'purchase_mass_balance','status':'not_calculated','detail':'Baseline yields are unknown; illustrative scenarios are separate'}, {'check':'contribution_sum','status':'not_calculated','detail':'Missing GWP values remain null/blank, not zero'}, {'check':'double_counting','status':'unresolved','detail':'Resin/conversion boundaries and supplier allocation must be resolved before impact calculation'}, {'check':'characterization','status':'not_calculated','detail':'No LCIA method or factors selected'}])
    write_json(output/'summary.json',summary)
    write_csv(output/'checks.csv',checks)
    from report import render_report
    render_report(output,summary,inventory,checks)
    print(json.dumps(summary,ensure_ascii=False,indent=2))

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive',help='Pinned public USLCI JSON-LD ZIP')
    parser.add_argument('--out',default=str(ROOT/'results/reproduced'))
    args=parser.parse_args()
    out=Path(args.out).resolve()
    if out.exists() and any(out.iterdir()):
        parser.error('Output directory must be new or empty; preserve previous runs')
    generate(args)

if __name__=='__main__':
    main()
