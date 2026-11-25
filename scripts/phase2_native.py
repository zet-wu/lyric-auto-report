"""Run current Studio public alignment APIs with shared source-axis acoustics."""
import argparse
import sys
import time
import xml.etree.ElementTree as ET
from dataclasses import asdict
from shared import ROOT, read, dump, exists, portable


def snapshot_for(sid, condition):
    if condition != 'dictionary':
        folder = ROOT / '.cache/comparison/inputs'
        path = folder / f'{sid}-studio-{condition}.json'
        if condition == 'manual' and not path.exists():
            path = ROOT / '.cache/timing/inputs' / f'{sid}-studio.json'
        return read(path)
    data = read(ROOT / 'results/M2/dictionary/inputs' / f'{sid}.json')
    T = '{http://www.w3.org/ns/ttml}'; S = '{http://www.w3.org/ns/ttml#styling}'
    D = '{urn:lazulite:studio:draft}'
    root = ET.Element(T + 'tt'); body = ET.SubElement(root, T + 'body'); div = ET.SubElement(body, T + 'div')
    for line in data['lines']:
        p = ET.SubElement(div, T + 'p', {D + 'id': line['id']})
        for index, proposal in enumerate(item for item in data['proposals'] if item['line_id'] == line['id']):
            attrs = {D + 'id': f"{line['id']}-dict-{index}"}
            word = ET.SubElement(p, T + 'span', attrs)
            if proposal['units']:
                word.set(S + 'ruby', 'container')
                ET.SubElement(word, T + 'span', {S + 'ruby': 'base'}).text = proposal['base']
                container = ET.SubElement(word, T + 'span', {S + 'ruby': 'textContainer'})
                for j, value in enumerate(proposal['units']):
                    ET.SubElement(container, T + 'span', {S + 'ruby': 'text', D + 'id': attrs[D + 'id'] + f'-u{j}'}).text = value
            else:
                word.text = proposal['base']
    return {'lyrics': {'draftTtml': ET.tostring(root, encoding='unicode')},
            'lineOrder': [line['id'] for line in data['lines']], 'editing': {'skippedAlignmentLineIds': []}}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--separator', required=True)
    parser.add_argument('--backend', choices=['nextfire', 'mms-fa'], required=True)
    parser.add_argument('--condition', choices=['manual', 'auto', 'dictionary'], default='manual')
    parser.add_argument('--mode', choices=['core', 'global', 'human'], default='core')
    parser.add_argument('--audio-format', choices=['float', 'aac'], default='float')
    parser.add_argument('--smart', action='store_true')
    parser.add_argument('--songs', nargs='+', required=True)
    parser.add_argument('--output-dir', type=__import__('pathlib').Path, required=True)
    args = parser.parse_args()
    sys.path[:0] = [str(ROOT / '.deps/comparison/studio'), str(ROOT / '.deps/comparison/lazulite/src')]
    import numpy as np
    import soundfile as sf
    import torch
    from lazulite.audio.io import decode_audio, resample_audio
    from lazulite.audio.preparation import prepare_existing_vocals
    from lazulite.audio.concat import ConcatMap, Piece
    from lazulite.models.audio import AudioBuffer
    from lazulite.models.japanese import JapaneseAlignmentRequest
    from lazulite.alignment.japanese.backend import open_backend
    from lazulite.alignment.japanese.run import align_japanese, compute_acoustics, JapaneseConfig
    from lazulite.alignment.japanese.stages import AcousticResult, FrameMap
    from server.alignment_projection import project_alignment
    from server.alignment_postprocessing import object_timings
    from server.vocal_audio import encode_vocals
    if not torch.cuda.is_available():
        raise RuntimeError('CUDA is required; no CPU alignment fallback')
    torch.set_num_threads(8)
    refs = {song['id']: song for song in read(ROOT / 'results/timing/reference.json')}
    backend = open_backend(ROOT / '.models' / args.backend, 'cuda')
    try:
        for sid in args.songs:
            target = args.output_dir / f'{sid}.json.gz'
            if exists(target) and read(target)['status'] == 'ok':
                continue
            started = time.monotonic(); stage = 'input'
            record = {'song': sid, 'separator': args.separator, 'backend': args.backend, 'condition': args.condition,
                      'mode': args.mode, 'audio_format': args.audio_format, 'smart': args.smart, 'status': 'failed'}
            try:
                song = refs[sid]
                source = ROOT / '.cache/comparison/stems' / args.separator / f'{sid}.wav'
                samples, rate = sf.read(source, dtype='float32', always_2d=True)
                vocals = AudioBuffer(samples.T.copy(), rate, sid)
                original = decode_audio(ROOT / song['audio'], sample_rate=rate, channels=2)
                difference = vocals.samples.shape[1] - original.samples.shape[1]
                if abs(difference) == 1:
                    # Independent decoders round the final sample differently.
                    # Preserve the source axis; adjust only its final sample.
                    adjusted = vocals.samples[:, :original.samples.shape[1]] if difference > 0 else np.pad(vocals.samples, ((0, 0), (0, 1)))
                    record['decoder_endpoint_adjustment'] = {'input_frames': vocals.samples.shape[1], 'original_frames': original.samples.shape[1], 'end_trimmed': max(difference, 0), 'end_padded': max(-difference, 0), 'stretched': False}
                    vocals = AudioBuffer(adjusted.copy(), rate, sid)
                if args.audio_format == 'aac':
                    stage = 'aac_encoding'
                    path = ROOT / '.cache/phase2/aac' / args.separator / f'{sid}.m4a'; path.parent.mkdir(parents=True, exist_ok=True)
                    peak=float(np.max(np.abs(vocals.samples),initial=0))
                    gain=min(1.0,(1-2**-15)/peak) if peak else 1.0
                    record.update(encoding={'implementation':'server.vocal_audio.encode_vocals','gain':gain,'peak_before_gain':peak,'decoded_sample_format':'float32','valid_frames':vocals.samples.shape[1]})
                    if not path.exists():
                        encode_vocals(path,vocals.samples,rate,gain)
                    decoded = decode_audio(path, sample_rate=rate, channels=2)
                    if decoded.samples.shape[1] < vocals.samples.shape[1]:
                        raise ValueError('AAC decode is shorter than the valid native sample interval')
                    vocals = AudioBuffer(decoded.samples[:, :vocals.samples.shape[1]].copy(), rate, sid)
                stage = 'vocal_analysis'
                prepared = prepare_existing_vocals(vocals, reference=original, original_duration=original.duration)
                record.update(analysis=asdict(prepared.analysis),core_segments=[asdict(segment) for segment in prepared.segments],duration=original.duration)
                stage = 'frontend_g2p'
                cached_projection=ROOT/'.cache/phase2/projections'/f'{sid}-{args.condition}-{args.backend}.json.gz'
                if cached_projection.exists():
                    cached=read(cached_projection)
                    if cached['status']!='ok':
                        record.update(error=cached['error'],failed_stage='frontend_g2p',seconds=time.monotonic()-started)
                        dump(target,record);continue
                    projection=cached['projection']
                else:
                    projection=project_alignment(snapshot_for(sid,args.condition),False,model={'vocabulary':backend.vocab,'blank':backend.blank},strip_tone_digits=sid in ('y01','y02','jy01'))
                record.update(projection=projection,input_tokens=projection['summary']['inputs'])
                request = JapaneseAlignmentRequest.from_dict(projection['request'])
                outputs = []; all_units = []; times = {}; stage = 'alignment_inference'
                cases = [(None, request, 0., vocals.duration)]
                if args.mode == 'human':
                    by_id = {line['id']: line for line in song['lines']}
                    cases = [(line.line_id, JapaneseAlignmentRequest((line,)), np.floor(by_id[line.line_id]['vocal_start']/.02)*.02 if by_id[line.line_id]['vocal_start'] is not None else None, np.ceil(by_id[line.line_id]['vocal_end']/.02)*.02 if by_id[line.line_id]['vocal_end'] is not None else None) for line in request.lines]
                for line_id, req, start, end in cases:
                    if start is None or end is None or end <= start:
                        raise ValueError('Human line window has no positive reference interval')
                    prefix = ROOT / '.cache/phase2/emissions' / f'{sid}-{args.separator}-{args.backend}-{args.audio_format}-{args.mode}-{line_id or "all"}'
                    prefix.parent.mkdir(parents=True, exist_ok=True)
                    if prefix.with_suffix('.npy').exists() and prefix.with_suffix('.json').exists():
                        metadata = read(prefix.with_suffix('.json'))
                        mapping = ConcatMap(metadata['mapping']['sample_rate'], metadata['mapping']['sample_count'], tuple(Piece(**piece) for piece in metadata['mapping']['pieces']))
                        acoustic = AcousticResult(np.load(prefix.with_suffix('.npy')), backend.vocab, backend.blank, FrameMap(**metadata['frames']), mapping, original.duration, special_tokens=backend.special_tokens)
                    else:
                        if args.mode == 'core':
                            acoustic = compute_acoustics(prepared, backend=backend)
                        else:
                            audio = resample_audio(vocals, sample_rate=backend.frames.sample_rate, channels=1)
                            a, b = max(0, int(start * audio.sample_rate)), min(audio.samples.shape[1], int(np.ceil(end * audio.sample_rate)))
                            clip = AudioBuffer(audio.samples[:, a:b].copy(), audio.sample_rate, sid)
                            mapping = ConcatMap(audio.sample_rate, b-a, (Piece(a, b, 0, b-a),))
                            acoustic = AcousticResult(backend.emissions(clip), backend.vocab, backend.blank, backend.frames, mapping, original.duration, special_tokens=backend.special_tokens)
                        np.save(prefix.with_suffix('.npy'), acoustic.log_probabilities)
                        dump(prefix.with_suffix('.json'), {'mapping': asdict(acoustic.mapping), 'frames': asdict(acoustic.frames)})
                    result = align_japanese(None, req, acoustic=acoustic, config=JapaneseConfig(hint_mode='off', strip_tone_digits=sid in ('y01', 'y02', 'jy01')))
                    outputs.append({'line_id': line_id, 'status': result.status}); all_units.extend(result.units)
                    selected = [item for item in projection['mapping'] if line_id is None or item['line_id'] == line_id]
                    times.update(object_timings(result, selected, vocals, args.smart, segments=prepared.segments))
                record.update(status='failed' if outputs and all(case['status']=='unresolved' for case in outputs) else 'ok', projection=projection, object_timings=times, units=[asdict(unit) for unit in all_units],
                              analysis=asdict(prepared.analysis), core_segments=[asdict(segment) for segment in prepared.segments], cases=outputs,
                              input_tokens=projection['summary']['inputs'], duration=original.duration)
            except Exception as exc:
                record.update(error={'type': type(exc).__name__, 'message': portable(exc)[:800]}, failed_stage=stage)
            record['seconds'] = time.monotonic() - started
            dump(target, record)
            print(sid, args.separator, args.backend, args.condition, args.mode, record['status'], flush=True)
    finally:
        backend.close()


if __name__ == '__main__':
    main()
