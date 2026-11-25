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
    language=line.get('language','ja')
    if language in ('yue','teochew'):
        return compile_parts(line['text'],[{'text':line['text'],'lang':language,'reading':' '.join(u['reading'] for w in line['words'] for u in w['units'])}],'auto')
    if language=='cmn':
        parts=[];prefix=''
        for word in line['words']:
            text=word['text'];units=word['units']
            if not units:
                if parts:parts[-1]['text']+=text
                else:prefix+=text
                continue
            if re.search('[A-Za-z]',text) and all(u['reading'].isascii() for u in units):
                last=0
                for match in re.finditer(r"[A-Za-z]+(?:['’][A-Za-z]+)*",text):
                    prefix+=text[last:match.start()]
                    surface=match.group()
                    parts.append({'text':prefix+surface,'lang':'en','reading':english_phones(surface)})
                    prefix='';last=match.end()
                parts[-1]['text']+=text[last:]
                continue
            characters=[(index,char) for index,char in enumerate(text) if char.isalnum()]
            if len(characters)!=len(units):
                raise ValueError('Native Chinese PFML requires one source Han character per supplied syllable')
            start=0
            for index,((position,char),unit) in enumerate(zip(characters,units,strict=True)):
                end=characters[index+1][0] if index+1<len(characters) else len(text)
                parts.append({'text':prefix+text[start:end],'lang':'zh','reading':unit['reading']});prefix='';start=end
        return compile_parts(line['text'],parts,'zh')
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
