from lingpy import *
from sys import argv
from lingrex.util import add_c_structure, align_by_structure
from lingrex.colex import find_colexified_alignments

alms = Alignments(argv[1], ref='cogids')


add_c_structure(alms)
align_by_structure(alms, segments='tokens', template="imnc")

for idx, concept, tokens, structure in alms.iter_rows('concept', 'tokens',
        'structure'):
    if '?' in structure:
        print(concept, tokens, structure)

find_colexified_alignments(alms, cognates='cogids', segments='tokens')

alms.output('tsv', filename=argv[1][:-4]+'-aligned', prettify=False)
