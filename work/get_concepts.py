from lingpy import *

wl = Wordlist('bodth-khobwa-patterns.tsv')

concepts = []
vis = []
num = 1
for idx, concept in wl.iter_rows('concept'):
    if concept in vis:
        pass
    else:
        concepts += [(num, concept)]
        num += 1
        vis += [concept]

with open('concepts.tsv', 'w') as f:
    f.write('NUMBER\tENGLISH\n')
    for n, c in concepts:
        f.write('{0}\t{1}\n'.format(n, c))
        
