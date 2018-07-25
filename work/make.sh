# Manually created the concepts-unmapped.tsv file with VI, then linked it automatically with pyconcepticon

concepticon map_concepts concepts-unmapped.tsv > concepts-mapped.tsv

# then it needs to be refined manually, we'll instruct Tim Bodt how to do this.

# profile
lingpy profile -i raw-wordlist.tsv -o profile.tsv --column=form --context --clts
