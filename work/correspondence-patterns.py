from lingpy import *
from lingrex.util import align_by_structure
from sys import argv
from lingrex.copar import CoPaR

cp = CoPaR(argv[1], ref='crossids')
align_by_structure(cp, segments='tokens', ref='crossids', structure='structure')

cp.add_entries('c_structure', 'tokens', lambda x: ' '.join(['c' if c not in
    '+_'
    else '+' for c in x]))

# make function to extract correspondence patterns
cp.get_sites(pos='c', minrefs=2, structure='c_structure')
cp.sort_patterns()
cp.cluster_patterns()
cp.sites_to_pattern()
cp.refine_sites()
cp.irregular_patterns(debug=True)

cp.add_patterns(irregular_patterns=True)
#cp.write_patterns('patterns-{0}.tsv'.format(s))
print(sum([len(x) for x in cp.clusters.values() if len(x) >= 3]) / sum(
    [len(x) for x in cp.clusters.values()]))

cp.output('tsv', filename='bodth-khobwa-patterns', prettify=False)

preds = cp.predict_words(debug=True)
with open('predictions.tsv', 'w') as f:
    f.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n'.format(
        'NUMBER', 'COGNATESET', 'LANGUAGE', 'CONCEPT', 'MORPHEME', 'WORD'
        ))
    num = 1
    for key, vals in sorted(preds.items(), key=lambda x: x[0]):
        # get the morphemes
        idx = cp.msa['crossids'][key]['ID'][0]
        cidx = cp[idx, 'crossids'].index(key)
        morph = cp[idx, 'morphemes'][cidx]
        for doc in vals:
            f.write('\t'.join([str(num), str(key), doc, cp[idx, 'concept'],
                morph, ' '.join(vals[doc])])+'\n')
            num += 1

