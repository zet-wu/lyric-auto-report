from common import *
product_imports()
from server.reading import SudachiReadingProposer
from dataclasses import asdict
import argparse
parser=argparse.ArgumentParser();parser.add_argument("--song");args=parser.parse_args()
p=SudachiReadingProposer();assert p.available,p.unavailable_reason
for s in songs():
 if args.song and s["id"]!=args.song:continue
 lines=[{'id':l['id'],'text':plain_line(l['text'])} for l in s['lines']]
 dump(CACHE/'inputs'/f"{s['id']}-reading.json",{'lines':lines,'proposals':[asdict(x) for x in sorted(p.propose(lines),key=lambda x:(x.line_id,x.base_start))]})
