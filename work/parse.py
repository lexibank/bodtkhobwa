from lingpy import *
from clldutils.text import split_text, strip_chars

csv = csv2list('raw-data.tsv')

D1 = {0: [
    'doculect',
    'concept',
    'value',
    'form',
    'variants',
    'note'
    ]}
D2 = {
        0: [
            'doculect',
            'concept',
            'value',
            'form',
            'variants',
            'note'
            ]}

heads = csv[0]
idx = 1
missing = 1
for line in csv[1:]:

    data = {h: e for h, e in zip(heads, line)}
    for doc in heads[1:]:
        val = data[doc]
        form, *variants = split_text(val, '~/')
        print(doc, val, form)
        if form in ["Ø", '-'] or not form.strip():
            missing += 1
            D2[idx] = [doc, data['Gloss'], '', '', '', '']
        else:
            if variants:
                note = 'Variants'
            else:
                note = ''
            try:
                tks = ipa2tokens(form)
            except:
                print(form)
                input()
            D1[idx] = [doc, data['Gloss'], val, form.strip().replace('-',
                '+').replace(' ', '_'), ''.join(variants), note ]
        idx += 1

wl, wl2 = Wordlist(D1), Wordlist(D2)
wl.output('tsv', filename="raw-wordlist")
wl2.output('tsv', filename="missing-words")
print(missing)
