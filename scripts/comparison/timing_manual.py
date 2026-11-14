"""Represent supplied kana in native explicit PFML, with no timestamp input."""
import re,jaconv
from timing.schema import Unit
from timing.singing import english_parts
from timing.llm_direct import compile_parts

def english_phones(surface):
    try:return english_parts(Unit(surface,surface),False)[0][1]
    except ValueError:
        # TIFA's native dictionary-backed LSTM fallback for Latin lyrics.
        from timing.config import MODELS
        import sys
        sys.path.insert(0,str(MODELS/'tifa/deps'))
        from g2pflow.converters.lstm import LSTMConverter
        converter=LSTMConverter(dict_path=str(MODELS/'tifa/dictionaries/ds_cmudict-07b.txt'),model_path=str(MODELS/'tifa/assets/LstmG2p-Eng'),beam_size=16)
        return [p for w in converter.convert(surface.lower()) for g in w.readings[0].paths[0] for p in g.phonemes]

def parts_for_line(line):
    words=line['words'];parts=[];prefix='';i=0
    def attach(text):
        nonlocal prefix
        if parts:parts[-1]['text']+=text
        else:prefix+=text
    while i<len(words):
        w=words[i];reading=''.join(u['reading'] for u in w['units'])
        if reading and reading.isascii():
            text=w['text'];i+=1
            while i<len(words) and words[i]['text'].isascii():text+=words[i]['text'];i+=1
            last=0
            for m in re.finditer(r"[A-Za-z]+(?:['’][A-Za-z]+)*",text):
                attach(text[last:m.start()]);surface=m.group();phones=english_phones(surface)
                parts.append({'text':prefix+surface,'lang':'en','reading':phones});prefix='';last=m.end()
            attach(text[last:]);continue
        i+=1
        if not reading:attach(w['text']);continue
        reading=jaconv.hira2kata(reading)
        # Standalone small vowels are equivalent elongated vowels; contracted
        # kana and long marks need the preceding kana in the converter input.
        if reading in 'ァィゥェォ':reading=reading.translate(str.maketrans('ァィゥェォ','アイウエオ'))
        if reading[0] in 'ャュョヮー' and parts and parts[-1]['lang']=='ja':
            parts[-1]['text']+=w['text'];parts[-1]['reading']+=reading
        else:parts.append({'text':prefix+w['text'],'lang':'ja','reading':reading});prefix=''
    assert not prefix
    return compile_parts(line['text'],parts,'mixed')
