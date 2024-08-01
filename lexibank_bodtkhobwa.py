from pathlib import Path

import attr
import lingpy
import pylexibank
from clldutils.misc import slug


@attr.s
class CustomCognate(pylexibank.Cognate):
    Morpheme_Index = attr.ib(default=None)


@attr.s
class CustomLexeme(pylexibank.Lexeme):
    Partial_Cognacy = attr.ib(default=None)


@attr.s
class CustomLanguage(pylexibank.Language):
    Latitude = attr.ib(default=None)
    Longitude = attr.ib(default=None)
    SubGroup = attr.ib(default=None)
    Family = attr.ib(default=None)


class Dataset(pylexibank.Dataset):
    id = "bodtkhobwa"
    dir = Path(__file__).parent
    cognate_class = CustomCognate
    language_class = CustomLanguage
    cross_concept_cognates = True
    lexeme_class = CustomLexeme
    writer_options = dict(keep_languages=False, keep_parameters=False)

    def cmd_makecldf(self, args):

        wl = lingpy.Wordlist(
            self.raw_dir.joinpath("bodt-khobwa-cleaned.tsv").as_posix(),
            conf=self.raw_dir.joinpath("wordlist.rc").as_posix(),
        )
        args.writer.add_sources()

        concept_lookup = {}
        for concept in self.conceptlists[0].concepts.values():
            idx = concept.id.split("-")[-1] + "_" + slug(concept.english)
            args.writer.add_concept(
                ID=idx,
                Name=concept.english,
                Concepticon_ID=concept.concepticon_id,
                Concepticon_Gloss=concept.concepticon_gloss,
            )
            concept_lookup[concept.english] = idx

        args.writer.add_languages(lookup_factory="Name")

        mapper = {
            "pʰl": "pʰ l",
            "pɕ": "p ɕ",
            "pɕ~ɕ/pɕ": "p ɕ",
            "aw": "au",
            "ɛj": "ɛi",
            "ɔw": "ɔu",
            "bl": "b l",
            "aj": "ai",
            "ɔj": "ɔi",
            "(ŋ)": "ŋ",
            "kʰl": "kʰ l",
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
            "ɛːʰ": "ɛːʰ/ɛː",
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
            "dɾ": "d ɾ",
            "tɾ": "t ɾ",
            "zj": "z j",
            "ɔj~uj/uj": "ɔj~uj/ui",
        }

        for idx in pylexibank.progressbar(wl, desc="cldfify"):
            segments = " ".join([mapper.get(x, x) for x in wl[idx, "tokens"]])
            concept = concept_lookup.get(wl[idx, "concept"], "")
            lex = args.writer.add_form_with_segments(
                Language_ID=wl[idx, "doculect"],
                Parameter_ID=concept,
                Value=wl[idx, "form"],
                Form=wl[idx, "form"],
                Segments=segments.split(),
                Partial_Cognacy=" ".join([str(x) for x in wl[idx, "crossids"]]),
                Source=["Bodt2019"],
            )
            for morpheme_index, cogid in enumerate(wl[idx, "crossids"]):
                alignment = wl[idx, "alignment"].split(" + ")[morpheme_index].split()
                alignment = " ".join([mapper.get(x, x) for x in alignment]).split()
                if int(cogid):
                    args.writer.add_cognate(
                        lexeme=lex,
                        Cognateset_ID=cogid,
                        Morpheme_Index=morpheme_index + 1,
                        Alignment=alignment,
                    )
