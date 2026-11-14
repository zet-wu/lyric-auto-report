"""Reuse the frozen Terra predictions only for identical inputs/candidates."""
from common import *
import hashlib, shutil

protocol = read(ROOT/'configs/reading.json')
pointer = ROOT/'.cache/reading-reuse.json'
source = ROOT/read(pointer)['source'] if pointer.exists() else OUT
for folder,key in [('inputs','input_sha256'),('predictions/studio','studio_prediction_sha256')]:
    for name,expected in protocol[key].items():
        assert hashlib.sha256((OUT/folder/name).read_bytes()).hexdigest() == expected, (folder,name,'Changed LLM input; reuse is invalid')
for method in ('terra-direct','terra-corrected'):
    for sid in protocol['songs']:
        src = source/'predictions'/method/(sid+'.json')
        dst = OUT/'predictions'/method/(sid+'.json')
        assert src.exists(), f'Missing saved LLM output: {src.relative_to(ROOT)}'
        if src.resolve() != dst.resolve():
            dst.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(src,dst)
print('Reused two frozen Terra conditions; inputs and Studio candidates match protocol hashes.')
