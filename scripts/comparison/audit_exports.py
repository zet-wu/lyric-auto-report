"""Check ASS event decoding independently, including native negative-hour syntax."""
from common import *
import hashlib, subprocess
import numpy as np
import pysubs2

header = ('[Script Info]\nScriptType: v4.00+\n[Events]\n'
          'Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n')
records = []
for name in ('fa-kara', 'yohane'):
    folder = OUT/name
    names = sorted({p.name.removesuffix('.gz') for p in folder.iterdir()
                    if p.name.endswith(('.json', '.json.gz'))})
    for filename in names:
        data = read(folder/filename)
        if data['status'] != 'ok':
            continue
        raw = [line for line in data['ass'].splitlines() if line.startswith('Dialogue:')]
        document = data['ass'] if '[Events]' in data['ass'] else header+data['ass']
        events = [e for e in pysubs2.SSAFile.from_string(document, format_='ass') if not e.is_comment]
        assert len(events) == len(raw)
        negatives = []
        for index, (event, line) in enumerate(zip(events, raw)):
            fields = line.split(',', 9)
            h, m, s = fields[1].split(':')
            expected = (int(h)*3600+int(m)*60+float(s))*1000
            if fields[1].startswith('-'):
                negatives.append({'line': index, 'encoded': fields[1], 'libass_arithmetic_ms': round(expected)})
            else:
                assert abs(event.start-expected) < .00001
            assert event.text == fields[9]
            assert not re.findall(r'\\k(-\d+)', event.text), 'Negative karaoke duration needs a renderer-specific audit'
        records.append({'file': str(folder/filename), 'events': len(raw),
                        'ass_sha256': hashlib.sha256(data['ass'].encode()).hexdigest(),
                        'negative_headers': negatives, 'negative_durations': []})

# FA-Kara encodes a -40 ms lead as -1:59:59.96. Check libass rendering rather
# than assuming a parser's whole-timestamp minus convention is authoritative.
source = ROOT/'configs/ass-time-probe.ass'
command = ['ffmpeg', '-v', 'error', '-f', 'lavfi', '-i', 'color=c=black:s=320x180:r=5:d=0.4',
           '-vf', 'ass=configs/ass-time-probe.ass', '-frames:v', '2', '-pix_fmt', 'rgb24', '-f', 'rawvideo', '-']
output = subprocess.run(command, check=True, capture_output=True)
frames = np.frombuffer(output.stdout, np.uint8).reshape(2, 180, 320, 3)
colors = []
for index, frame in enumerate(frames):
    red = int(((frame[:,:,0] > 100) & (frame[:,:,2] < 50)).sum())
    blue = int(((frame[:,:,2] > 100) & (frame[:,:,0] < 50)).sum())
    colors.append({'seconds': index/5, 'red_pixels': red, 'blue_pixels': blue})
assert colors[0]['red_pixels'] == 0 and colors[0]['blue_pixels'] > 0
assert colors[1]['red_pixels'] > 0 and colors[1]['blue_pixels'] > 0
dump(OUT/'export-audit.json', {
    'independent_positive_event_origins_and_text': 'pysubs2 1.8.1',
    'negative_time_probe': {'renderer': 'FFmpeg libass', 'source': source.read_text(),
        'command': command, 'header': '-1:59:59.96', 'interpreted_seconds': -.04,
        'empty_lead_karaoke_centiseconds': 20, 'frames': colors,
        'meaning': 'First syllable activates at 0.16 seconds; negative hours use arithmetic component parsing.'},
    'records': records})
print('Audited', sum(r['events'] for r in records), 'ASS events and the libass negative-time probe.')
