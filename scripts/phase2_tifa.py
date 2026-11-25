"""TIFA with reference line windows, using native PFML compilation and inference."""
import argparse
import sys
import time
from dataclasses import asdict
from shared import ROOT, read, dump, exists, portable


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--sep', required=True)
    parser.add_argument('--songs', nargs='+', required=True)
    parser.add_argument('--output-dir', type=__import__('pathlib').Path, required=True)
    args = parser.parse_args()
    sys.path[:0] = [str(ROOT / '.deps/comparison/timing'), str(ROOT / 'scripts/comparison')]
    from timing.schema import Line,Unit
    from timing.llm_direct import write_pfml, acoustic_languages, spoken
    from timing import tifa
    from timing_manual import parts_for_line
    import soundfile as sf
    refs = {song['id']: song for song in read(ROOT / 'results/timing/reference.json')}
    for sid in args.songs:
        path = args.output_dir / f'{sid}.json.gz'
        if exists(path) and read(path)['status'] == 'ok':
            continue
        record = {'song': sid, 'separator': args.sep, 'backend': 'tifa', 'mode': 'human', 'status': 'failed'}
        stage = 'frontend_g2p'; started = time.monotonic()
        try:
            source = read(ROOT / 'results/comparison/milikara/inputs/manual' / f'{sid}.json')
            references = refs[sid]['lines']
            lines = [Line(line['text'], start=ref['vocal_start'], end=ref['vocal_end'], language='mixed') for line, ref in zip(source['lines'], references, strict=True)]
            parts = [{'status': 'accepted', 'parts': parts_for_line(line)} for line in source['lines']]
            wave, rate = sf.read(ROOT / '.cache/comparison/stems' / args.sep / f'{sid}.wav', dtype='float32', always_2d=True)
            work = ROOT / '.cache/phase2/tifa-human' / args.sep / sid; work.mkdir(parents=True, exist_ok=True)
            stage = 'alignment_inference'
            import math
            clips=[]
            for index,(line,item) in enumerate(zip(lines,parts)):
                a=max(0,round(math.floor(line.start/.02)*.02*rate));b=min(len(wave),round(math.ceil(line.end/.02)*.02*rate))
                audio=work/f'line_{index+1:03}.wav'
                sf.write(audio,wave[a:b].mean(axis=1),rate,subtype='FLOAT')
                audio.with_suffix('.txt').write_text(spoken(line.text),encoding='utf-8')
                write_pfml(audio,item['parts'])
                clips.append({'id':f'line_{index+1:03}','audio':str(audio),'start':a/rate,'end':b/rate,
                              'target_start':0,'target_end':len(spoken(line.text)),'llm_direct_parts':item['parts'],
                              'source_line':index+1,'languages':acoustic_languages(item['parts'])})
            raw=tifa.run_worker(work,clips,print)
            native_rows={row['id']:row for row in raw['results']};checks=[];aligned=[]
            for line,clip in zip(lines,clips,strict=True):
                try:
                    mapped,detail=tifa.map_clip(line,native_rows[clip['id']],clip,False)
                    aligned.append(mapped);checks.append({'line_id':clip['id'],'status':'ok','start':clip['start'],'end':clip['end']})
                except Exception as exc:
                    line.words=[Unit(line.text,line.text,flags=['tifa_unresolved_unit'])]
                    aligned.append(line);checks.append({'line_id':clip['id'],'status':'failed','error':{'type':type(exc).__name__,'message':portable(exc)[:800]}})
            record.update(status='failed' if any(check['status']=='failed' for check in checks) else 'ok', result={'lines': [asdict(line) for line in aligned]}, checks=checks)

        except Exception as exc:
            record.update(error={'type': type(exc).__name__, 'message': portable(exc)[:800]}, failed_stage=stage)
        record['seconds'] = time.monotonic() - started
        dump(path, record)
        print('TIFA', sid, args.sep, record['status'], flush=True)


if __name__ == '__main__':
    main()
