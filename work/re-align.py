from lingpy import *
from sys import argv
from lingrex.util import add_c_structure, align_by_structure

alms = Alignments(argv[1], ref='cogids')


add_c_structure(alms)
align_by_structure(alms, segments='tokens', template="imncimnc")

for idx, concept, tokens, structure in alms.iter_rows('concept', 'tokens',
        'structure'):
    if '?' in structure:
        print(concept, tokens, structure)

alms.output('tsv', filename=argv[1][:-4]+'-aligned', prettify=False)
