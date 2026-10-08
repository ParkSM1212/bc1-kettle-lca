"""Verify the preserved independent outputs without modifying files."""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/'data/independent_output_manifest.json').read_text(encoding='utf-8'))
failures=[]
for entry in manifest['files']:
    p=ROOT/entry['path']
    if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=entry['sha256']:
        failures.append(entry['path'])
if failures:
    raise SystemExit('Missing or changed outputs: '+', '.join(failures))
print('PASS:',len(manifest['files']),'independent output files match their recorded SHA-256 hashes.')
