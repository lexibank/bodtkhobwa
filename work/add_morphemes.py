from lingpy import *
from lingrex.util import align_by_structure
from sys import argv
from lingrex.copar import CoPaR

morph_ = csv2list(argv[2], strip_lines=False)

# refine morphemes
M = {}
for cogid, morpheme, _a, _b, concepts in morph_:
    M[int(cogid)] = morpheme.replace(' ', '_')

wl = Alignments(argv[1], ref='crossids')
wl.add_entries('morphemes', 'crossids', lambda x: [M.get(y, '?') for y in x])
align_by_structure(wl, segments='tokens')

# write to file
new_name = '-'.join(argv[1].split('-')[:2])+'-morphemes'

wl.output('tsv', filename=new_name)

# make function to extract correspondence patterns
for s in 'imnc':
    cp = CoPaR(wl, ref='crossids')
    cp.get_sites(pos=s, minrefs=2, structure='structure')
    cp.sort_patterns()
    cp.cluster_patterns()
    cp.sites_to_pattern()
    cp.refine_sites()
    cp.write_patterns('patterns-{0}.tsv'.format(s))
    print(s, sum([len(x) for x in cp.clusters.values() if len(x) >= 3]) / sum(
        [len(x) for x in cp.clusters.values()]))
