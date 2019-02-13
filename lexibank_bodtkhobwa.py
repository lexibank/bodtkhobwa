from __future__ import unicode_literals, print_function
from collections import OrderedDict, defaultdict

import attr
from clldutils.misc import slug
from clldutils.path import Path
from clldutils.text import split_text, strip_brackets
from pylexibank.dataset import Dataset as BaseDataset
from pylexibank.dataset import Concept, Language

from lingpy import *
from tqdm import tqdm



class Dataset(BaseDataset):
    id = 'bodtkhobwa'
    dir = Path(__file__).parent
    concept_class = Concept
    language_class = Language
    

    def split_forms(self, item, value):
        """Override custom behavior: no splitting into multiple values.
        This is done explicitly in the code"""
        value = self.lexemes.get(value, value)
        return [self.clean_form(item, form) for form in [value]]

    def cmd_download(self, **kw):
        pass

    def cmd_install(self, **kw):

        data = Wordlist(self.dir.joinpath('raw',
            'bodt-khobwa-cleaned.tsv').as_posix())
        langs = {} # need for checking later
        concepts = {}

        with self.cldf as ds:

            for concept in self.concepts:
                ds.add_concept(
                        ID=concept['NUMBER'],
                        Name=concept['ENGLISH'],
                        Concepticon_ID=concept['CONCEPTICON_ID'],
                        Concepticon_Gloss=concept['CONCEPTICON_GLOSS']
                        )
                concepts[concept['ENGLISH']] = concept['NUMBER']

            for language in self.languages:
                ds.add_language(
                        ID=language['ID'],
                        Glottocode=language['Glottolog'],
                        Name=language['Name'],
                        )
                langs[language['ID']] = language

            ds.add_sources(*self.raw.read_bib())
            num = 580
            for concept in data.concepts:
                if not concept in concepts:
                    print('"{0}","{1}",,,'.format(num, concept))
                    num += 1

            mapper = {
                    "pʰl": "pʰ l",
                    "aw": "au",
                    "ɛj": "ɛi",
                    "ɔw": "ɔu",
                    "bl": "b l",
                    "aj": "ai",
                    "ɔj": "ɔi",
                    "(ŋ)": "ŋ",
                    "kʰl": "kʰ l",
                    "kl": "k l",
                    "ej": "ei",
                    "uj": "ui",
                    "bɹ": "b ɹ",
                    "ɐʰ": "ɐʰ/ɐ",
                    "hw": "h w",
                    "ɔːʰ": "ɔːʰ/ɔː",
                    "dʑr": "dʑ r",
                    "ow": "ou",
                    "pl": "p l",
                    "lj": "l j",
                    "tʰj": "tʰ j",
                    "aːʰ": "aːʰ/aː",
                    "bj": "b j",
                    "mp": "m p",
                    "pɹ": "p ɹ",
                    "ɐ̃ʰ": "ɐ̃ʰ/ɐ̃",
                    "ɔ̃ʰ": "ɔ̃ʰ/ɔ̃",
                    "aj~e/aj": "aj~e/ai",
                    "aj~ej/ej": "aj~ej/ei",
                    "kl": "k l",
                    "kʰɹ": "kʰ ɹ",
                    "ɛːʰ":"ɛːʰ/ɛː",
                    "ɔʰ": "ɔʰ/ɔ",
                    "tɹ": "t ɹ",
                    "ɐːʰ": "ɐːʰ/ɐ",
                    "br": "b r",
                    "kɹ": "k ɹ",
                    "kʰj": "kʰ j",
                    "kʰr": "kʰ r",
                    "gɹ": "g ɹ",
                    "hj": "h j",
                    "bl~gl/bl": "bl~gl/b l",
                    "dj": "d j",
                    "ej~i/ej": "ej~i/ei",
                    "e~a/ej": "e~a/ei",
                    "fl": "f l",
                    "kʰw": "kʰ w",
                    "mj": "m j",
                    "pr": "p r",
                    "pʰl~bl/pʰl": "pʰl~bl/pʰ l",
                    "pʰr": "pʰ r",
                    "pʰr~pʰl/pʰr": "pʰr~pʰl/pʰ r",
                    "pʰw": "pʰ w",
                    "pʰɹ": "pʰ ɹ",
                    "tr": "t r",
                    "tɕʰɹ": "tɕʰ ɹ",
                    "tʰr": "tʰ r",
                    "tʰw": "tʰ w",
                    "zj": "z j",
                    "ɔj~uj/uj": "ɔj~uj/ui",
                    }

            # add data to cldf
            for idx in tqdm(data, desc='cldf the data'):
                segments = [mapper.get(x, x) for x in data[idx, 'tokens']]
                segments = ' '.join(segments).split()
                concept = concepts.get(data[idx, 'concept'], '')
                ds.add_lexemes(
                    Language_ID=data[idx, 'doculect'].lower(),
                    Parameter_ID=concept,
                    Form=data[idx, 'form'],
                    Value=data[idx, 'value'],
                    Segments=segments,
                    Source=['Bodt2019'],
                    #PhoneticValue=vals['phonetic']
                    )


