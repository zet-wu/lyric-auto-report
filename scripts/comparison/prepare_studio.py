from common import *
product_imports()
from server.reading import SudachiReadingProposer
from dataclasses import asdict
p=SudachiReadingProposer();assert p.available,p.unavailable_reason
for s in songs():
 lines=[{'id':l['id'],'text':l['text']} for l in s['lines']]
 dump(CACHE/'inputs'/f"{s['id']}-reading.json",{'lines':lines,'proposals':[asdict(x) for x in p.propose(lines)]})
