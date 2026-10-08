"""Download the pinned public USLCI snapshot, verify its hash, and cache locally."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import urllib.error
import urllib.parse
import urllib.request

ROOT=Path(__file__).resolve().parents[1]
BASE='https://api.nal.usda.gov/FederalLCACommonsapi'

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out',help='Destination ZIP; defaults to manifest path')
    a=p.parse_args()
    m=json.loads((ROOT/'data/source_manifest.json').read_text(encoding='utf-8'))
    dest=Path(a.out) if a.out else ROOT/m['expected_local_path']
    if dest.exists():
        if hashlib.sha256(dest.read_bytes()).hexdigest()==m['sha256']:
            print('Verified cached archive:',dest)
            return
        raise SystemExit('Existing archive hash differs. Preserve it and choose another output path.')
    key=os.environ.get('LCA_COMMONS_API_KEY')
    if not key:
        raise SystemExit('Set LCA_COMMONS_API_KEY using the official LCA Commons API Guide. Do not store it in project files.')
    url=BASE+'/download/json/'+urllib.parse.quote(m['download_descriptor'],safe='@_')+'?'+urllib.parse.urlencode({'api_key':key})
    dest.parent.mkdir(parents=True,exist_ok=True)
    part=dest.with_suffix(dest.suffix+'.part')
    if part.exists():
        raise SystemExit('Partial download already exists; preserve or remove it before retrying.')
    try:
        with urllib.request.urlopen(url,timeout=60) as r, part.open('xb') as f:
            h=hashlib.sha256(); size=0
            while block:=r.read(1024*1024):
                f.write(block); h.update(block); size+=len(block)
        if size!=m['bytes'] or h.hexdigest()!=m['sha256']:
            raise SystemExit('Downloaded bytes do not match pinned snapshot. Partial file retained; no analysis performed.')
        part.rename(dest)
        print('Verified archive:',dest)
        print('SHA-256:',h.hexdigest())
    except urllib.error.HTTPError as e:
        raise SystemExit(f'HTTP {e.code}. For 429, wait for the API quota reset. If the pinned server artifact has expired, obtain the same revision via the official UI; do not substitute a newer release silently.') from None
    except urllib.error.URLError:
        raise SystemExit('Network or TLS failure; any partial file retained. Credentials and request URL are not logged.') from None

if __name__=='__main__':
    main()
