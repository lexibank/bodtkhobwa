from lingpy import *
from sys import argv
from collections import defaultdict
from clldutils.misc import slug

wl = Wordlist(argv[1])

for idx, cids in wl.iter_rows('crossids'):
    wl[idx, 'crossids'] = [int(x) for x in cids.split()]

# get the morphemes now
M = wl.get_etymdict(ref='crossids')

clist = []
for cogid in M:
    vals = []
    for x in M[cogid]:
        if x:
            vals += x
    concepts = [wl[x, 'concept'] for x in vals]
    best_concept = sorted(concepts, key=lambda x: concepts.count(x),
            reverse=True)[0]
    clist += [[
        str(cogid), 
        slug(best_concept),
        str(len(set(concepts))),
        str(len(concepts)),
        ' / '.join(sorted(set(concepts), key=lambda x: concepts.count(x)))
        ]]

with open('morphemes.tsv', 'w') as f:
    for line in sorted(clist, key=lambda x: int(x[3]), reverse=True):
        f.write('\t'.join(line)+'\n')


