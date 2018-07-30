from lingpy import *
from segments.tokenizer import Tokenizer as Tk
from collections import defaultdict
from lingpy.compare.partial import Partial
from lingpy.sequence.sound_classes import tokens2morphemes
from clldutils.misc import slug

profile = Tk('profile.tsv')

wl = Wordlist('raw-wordlist.tsv')

wl.add_entries('tokens', 'form', lambda x: profile('^'+x+'$',
    column="IPA").split())

concepts = {}
for idx, c in wl.iter_rows('concept'):
    if c[-1] in ['1', '2']:
        concept = c[:-1]
    else:
        concept = c
    concepts[c] = concept
wl.add_entries('_concept', 'concept', lambda x: concepts[x])

D = {0: [
        "doculect",
        "concept",
        "concept_in_source",
        "value",
        "form",
        "tokens",
        "note"
    ]}

for idx, tks in wl.iter_rows('tokens'):
    D[idx] = [wl[idx, h] for h in ["doculect", "_concept", "concept", "value",
        "form", "tokens"]] + ['']
    try:
        for m in tokens2morphemes(tks):
            if ' '.join(m).strip():
                pass
            else:
                print(idx, tks)
    except ValueError:
        print(idx, tks)

part = Partial(D)
part.partial_cluster(method='sca', threshold=0.45, cluster_method='infomap',
        ref='autocogs')
part.add_entries('cogids', 'autocogs', lambda x: x)

M = defaultdict(list)
for idx, tks, cogids, concept in part.iter_rows('tokens', 'cogids', 'concept'):
    
    morphemes = tokens2morphemes(tks)
    if len(morphemes) == 2:
        M['^ '+' '.join(morphemes[0])] += [concept]
        M[' '.join(morphemes[-1])+' $'] += [concept]
        for m in morphemes[1:-1]:
            M[' '.join(m)] += [concept]
    else:
        for m in morphemes:
            M[' '.join(m)] += [concept]

with open('morphemes.tsv', 'w') as f:
    for k, vs in sorted(M.items(), key=lambda x: len(x[1]), reverse=True):
        ms = sorted(set(vs), key=lambda x: vs.count(x), reverse=True)
        if k.startswith('^'):
            pref = '^'
            k = k[2:]
        elif k.endswith('$'):
            pref = '$'
            k = k[:-2]
        else:
            pref = ''

        f.write('{0}\t{1}\t{2}\t{3}\t{4}\n'.format(
            k, pref, len(vs), ms[0], ' / '.join(ms)))

# add alignments
alm = Alignments(part, ref='cogids', segments='tokens')
alm.align()

alm.output('tsv', filename='wordlist-pcogs', subset=True, cols=[h for h in
    D[0]+['cogids', 'autocogs', 'alignment']], ignore='all', prettify=False)
