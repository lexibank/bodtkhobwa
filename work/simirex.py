from collections import OrderedDict
from lingrex.semirex import *
from lingrex.util import *
from lingrex.copar import *
from lingpy import *

wl = Alignments('bodth-khobwa-patterns.tsv', ref='crossids')
align_by_structure(wl, structure='structure', ref='crossids', segments='tokens')

patterns = read_patterns('patterns-2018-08-02.tsv', wl.cols,
        structure='structure', proto='PWK', cognates='cognates', note='notes')


protos = reconstruct(
        wl, 'Proto-Khobwa', patterns, ref='crossids')
counts = []
num = 1
with open('reconstructions.tsv', 'w') as f:
    f.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n'.format(
        'NUMBER', 'COGNATESET', 'CONCEPT', 'MORPHEME', 'PROTOFORM', 'SCORE'
        ))
    for key, vals in sorted(protos.items(), key=lambda x: x[0]):
        score = 1 - vals.count('⁰?') / len(vals)
        # get the morphemes
        idx = wl.msa['crossids'][key]['ID'][0]
        cidx = wl[idx, 'crossids'].index(key)
        morph = wl[idx, 'morphemes'][cidx]
        f.write('\t'.join([str(num), str(key), wl[idx, 'concept'], morph,
            '{0:.2f}'.format(score), ' '.join(vals)])+'\n')
        counts += [score]
print('{0:.2f}'.format(sum(counts) / len(counts)))



