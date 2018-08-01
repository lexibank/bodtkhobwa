# Manually created the concepts-unmapped.tsv file with VI, then linked it automatically with pyconcepticon

concepticon map_concepts concepts-unmapped.tsv > concepts-mapped.tsv

# then it needs to be refined manually, we'll instruct Tim Bodt how to do this.

# parse the data
python parse.py 

# profile
lingpy profile -i raw-wordlist.tsv -o profile.tsv --column=form --context --clts

# apply the profile
python apply_profile.py

# re-align the data and add cross cognate ids
python re-align.py INFILE

# add the morphemes
python get_morphemes.py INFILE
python add_morphemes.py INFILE MORPHEMES_FILE
