#! /usr/bin/env python3
# coding: utf-8

"Arithmetic coding of texts."

from __future__ import print_function
import random
import collections


def count_symbols(string):
    counter = collections.Counter(string)
    return dict(counter)


def shuffle_symbols(text):
    "Shuffle the symbols of the text."
    return "".join(random.sample(text, len(text)))


class ArithmeticCode:

    def __init__(self, intervals_or_sample):
        if isinstance(intervals_or_sample, str):
            self.intervals = self.get_intervals(intervals_or_sample)
            self.text = intervals_or_sample
        elif isinstance(intervals_or_sample, list):
            self.intervals = intervals_or_sample
            self.text = None
        else:
            raise ValueError("The arguments must be string or list.")

    @staticmethod
    def get_intervals(sample):
        number_of_symbols = count_symbols(sample)
        lower_limit = 0
        intervals = collections.OrderedDict()
        for symbol in sorted(number_of_symbols.keys()):
            probablity = number_of_symbols[symbol] / len(sample)
            upper_limit = lower_limit + probablity
            intervals[symbol] = (lower_limit, upper_limit)
            lower_limit = upper_limit
        return intervals

    def coder_intervals(self, text=None):
        if text is None:
            text = self.text
        code_intervals = []
        lower0, upper0 = 0., 1.
        for i, symbol in enumerate(text, 1):
            length = upper0 - lower0
            lower, upper = self.intervals[symbol]
            lower0, upper0 = lower0 + length*lower, lower0 + length*upper
            code_intervals.append((text[:i], lower0, upper0))
        return code_intervals

    def coder(self, text):
        text, lower_limit, upper_limit = self.coder_intervals(text)[-1]
        return (lower_limit + upper_limit) / 2

    def decoder_steps(self, code, length=10, verbose=False):
        """Visszafejti a kódolt szöveget az intervallumok ismeretében."""
        steps = []

        t = code
        message = ""
        for i in range(length):
            for k in self.intervals.keys():
                a, f = self.intervals[k]
                if a < t < f:
                    message += k
                    break
            steps.append((message, t))
            if verbose:
                print("{0:<12.10} {1}.".format(
                    t, k)
                )
            diff = t - a
            t = diff / (f - a)
        return steps

    def decoder(self, code, length=10, verbose=False):
        decoder_steps = self.decoder_steps(code, length, verbose)
        return decoder_steps[-1][0]

    def code_of_words(self, word_list, file_=None):
        if isinstance(word_list, str):
            word_list = word_list.split()
        codes = []
        for word in word_list:
            code = self.coder(word)
            codes.append((word, code))
        return codes


def save_codes_of_words(word_list, file_):
    if isinstance(file_, str):
        file_ = open(file_, "w")
    for word in word_list:
        code = ArithmeticCode(word)
        code_value = code.coder(word)
        print("% {:3} {:10} {:7}".format(len(word), code_value, word),
              file=file_)

"""
def print_it(text, latex=False, verbose=True):
    szovegresz = text
    if verbose:
        if latex:
            print("{:>10}& $\\rightarrow [$ {:<12.10g}&; "
                    "{:<12.10g} &[\\\\".format(szovegresz, lower0, upper0))
        else:
            print("{:>10} --> [{:<12.10g}; {:<12.10g}[".format(
                szovegresz, lower0, upper0))
"""

intervallumok = \
    (
        {
            "A": (0,   0.2),
            "B": (0.2, 0.3),
            "E": (0.3, 0.6),
            "L": (0.6, 0.7),
            "K": (0.7, 0.8),
            "R": (0.8, 0.9),
            "T": (0.9, 1.0),
        },
    )


word_parts_hu = {
    "CASABLANCA": (
        "ALBA",
        "BASA",
        "ANCSA",
        "CSALA",
        "CSABA",
        "NACSA",
        "ABBA",
        "ABBAN",
        "BALLA",
        "ANNA",
        "CASA",
    ),
    'AKROBATIKA': (
        "ABBA",
        "ABBOT",
        "ABRAK",
        "AKAR",
        "AKART",
        "AKIK",
        "AKIT",
        "AKKOR",
        "AKTA",
        "AKTOT",
        "ARAB",
        "ARAK",
        "ARAT",
        "ARBOR",
        "ARRA",
        "ATKA",
        "BABA",
        "BAKA",
        "BAKI",
        "BAKOT",
        "BAKTA",
        "BARI",
        "BARIT",
        "BARKA",
        "BIBI",
        "BIBIT",
        "BIKA",
        "BIRKA",
        "BOBA",
        "BOKA",
        "BOKOR",
        "BOROK",
        "BORT",
        "BRIT",
        "IKRA",
        "IKTAT",
        "IRAT",
        "IRKA",
        "ITAT",
        "KABA",
        "KARBA",
        "KARIB",
        "KATA",
        "KIIRT",
        "KIRAK",
        "KITTI",
        "KOBAK",
        "KOBRA",
        "KORA",
        "KORAI",
        "KORI",
        "KOROK",
        "KORT",
        "KOTOR",
        "KOTTA",
        "KROKI",
        "OKOK",
        "OKOT",
        "OKTAT",
        "ORRA",
        "ORRBA",
        "ORROT",
        "RABBI",
        "RAKAT",
        "RITA",
        "RITKA",
        "ROBOT",
        "ROBI",
        "ROOT",
        "TABOR",
        "TAKAR",
        "TARKA",
        "TART",
        "TATA",
        "TIARA",
        "TIBA",
        "TIBOR",
        "TITOK",
        "TOKA",
        "TOKBA",
        "TORKA",
        "TOROK",
        "TORTA",
    ),
    "MIKKAMAKKA": (
        "MIKI",
        "MAKI",
        "AKIK",
        "AMIM",
        "KAKA",
        "MAKK",
        "MAMA",
        "MAMI",
    ),
    "TOPCSILLAG": (
        "ALAP",
        "ALAP",
        "ALAP",
        "ALATT",
        "ALGA",
        "ALIG",
        "APAI",
        "APAIT",
        "ATOLL",
        "CICA",
        "CSAL",
        "CSALI",
        "CSAP",
        "CSAP",
        "CSAPA",
        "CSAPI",
        "CSAT",
        "CSATA",
        "CSIGA",
        "CSILLAG",
        "CSILLOG",
        "CSIPA",
        "CSITT",
        "GALL",
        "GICCS",
        "GITT",
        "IGAL",
        "ILLAT",
        "ITAL",
        "ITALT",
        "ITAT",
        "LALA",
        "LAPOS",
        "LAPOT",
        "LICIT",
        "LIGA",
        "LIGA",
        "LILI",
        "LILLA",
        "LIPPA",
        "LISTA",
        "LOLA",
        "OLGA",
        "PACA",
        "PACAL",
        "PACI",
        "PACSA",
        "PALA",
        "PALI",
        "PAPA",
        "PAPI",
        "PAPOL",
        "PAPOS",
        "PASAS",
        "PASI",
        "PATA",
        "PATT",
        "PIAC",
        "PIAC",
        "PIACI",
        "PICI",
        "PICIT",
        "PILIS",
        "PIPA",
        "PIPI",
        "POCI",
        "POLC",
        "POLIP",
        "POLLI",
        "POPSI",
        "POSTA",
        "SICC",
        "SITT",
        "SLAG",
        "SOLT",
        "TACCS",
        "TAGOL",
        "TALP",
        "TALPA",
        "TAPOS",
        "TAPS",
        "TASS",
        "TATA",
        "TILLA",
        "TILOS",
        "TILT",
        "TIPP",
        "TOLAT",
        "TOLL",
        "TOLL",
        "TOLLA",
        "TOPIS",
        "TOPOG",
    ),
    "SZACDEREGI": (
        "ADAG",
        "ARCA",
        "ARCRA",
        "ADDIG",
        "CICA",
        "CSER",
        "CSIGA",
        "CSERE",
        "DADA",
        "DAGI",
        "DAGAD",
        "DARA",
        "DERCE",
        "DERES",
        "EDDIG",
        "ERESZ",
        "EGRES",
        "ERDEI",
        "ERED",
        "ERES",
        "ERESZ",
        "ERRE",
        "ESZE",
        "ESZED",
        "ESZES",
        "ESZI",
        "EZER",
        "EZRED",
        "GARAS",
        "GAZDA",
        "GICCS",
        "GIDA",
        "IDEG",
        "IDEGI",
        "IDEI",
        "IDEIG",
        "IGAZ",
        "IGAZA",
        "IGAZI",
        "IGEI",
        "ISSZA",
        "IZGI",
        "IZZAD",
        "RADAR",
        "RAGAD",
        "RECCS",
        "REGE",
        "REZEG",
        "REZES",
        "REZEZ",
        "REZSI",
        "RIAD",
        "RIDEG",
        "RIZS",
        "RIZSA",
        "SARC",
        "SEREG",
        "SICC",
        "SIESD",
        "SIESS",
        "SZAG",
        "SZAGA",
        "SZED",
        "SZEDD",
        "SZEDI",
        "SZEG",
        "SZEGI",
        "SZER",
        "SZESZ",
        "SZIA",
        "SZID",
        "ZACC",
        "ZERGE",
        "ZIZEG",
        "AIDA",
        "EDDA",
        "GERDA",
        "GIDA",
        "ADDIG",
        "ADSZ",
        "ARRA",
        "AZAZ",
        "EDDIG",
        "ERRE",
        "EZER",
        "IGAZ",
        "IGAZA",
        "IGAZI",
        "ISZA",
        "READ",
        "REGI",
        "RESZ",
        "SEREG",
        "SZED",
        "ERCSI",
        "ZIRC",
        "ARAD",
        "EGRES",
        "GECSE",
        "GIDA",
        "GERI",
        "IREG",
        "RECCS",
        "REGE",
        "SZERDA",
        "SEREG",
        "SZEG",
        "SZER",
        "ZSIGER",
    ),
    "FELELETTEL": (
        "ELLET",
        "ELTE",
        "ETEL",
        "ETELE",
        "ETET",
        "ETTE",
        "FELE",
        "FELEL",
        "FETT",
        "LELET",
        "LELLE",
        "LELT",
        "LELTE",
        "LETT",
        "TELE",
        "TELEL",
        "TELT",
        "TETT",
        "TETTE",

    ),
    "LEHELETTEL": (
        "EHET",
        "ELLET",
        "ELTE",
        "ETEL",
        "ETELE",
        "ETET",
        "ETTE",
        "HETE",
        "LEHEL",
        "LELET",
        "LELLE",
        "LELT",
        "LELTE",
        "LETT",
        "TEHET",
        "TELE",
        "TELEL",
        "TELT",
        "TETT",
        "TETTE",

    ),
    "TEREMTETTE": (
        "ERET",
        "ERRE",
        "ETET",
        "ETTE",
        "ETTEM",
        "MERRE",
        "TEMET",
        "TERE",
        "TERET",
        "TETEM",
        "TETT",
        "TETTE",

    ),
    "ALKALOMMAL": (
        "AKOL",
        "ALAK",
        "ALMA",
        "ALOM",
        "KOALA",
        "KOMA",
        "LAKK",
        "LAKOL",
        "LOLA",
        "MAKK",
        "MALOM",
        "MAMA",
        "MOLL",
        "MOLLA",
        "OKOK",
        "OKOL",
        "OKOM",

    ),
    "BOROSSEBES": (
        "BESE",
        "BOROS",
        "BORS",
        "BROSS",
        "EBBE",
        "ERES",
        "ERRE",
        "SEBES",
        "SOROS",
        "SORS",
        "SOSE",

    ),
    "CINCINNATI": (
        "ANITA",
        "ANNA",
        "CICA",
        "INNI",
        "ITAT",
        "NINA",
        "NINI",
        "TANA",
        "TATA",
        "TINA",
        "TINI",
        "TINTA",

    ),
    "CSEPPECSKE": (
        "CSEKE",
        "CSEKK",
        "CSEPP",
        "KEKEC",
        "PECEK",
    ),
    "UGYANANNYI": (
        "AGYA",
        "AGYAG",
        "AGYI",
        "ANNA",
        "ANNYI",
        "ANYA",
        "ANYAG",
        "ANYAI",
        "ANYU",
        "GANNA",
        "GINA",
        "GYUGY",
        "INGA",
        "INNI",
        "NAGY",
        "NAGYI",
        "NINA",
        "NINI",
        "NYUGI",
    ),
    "OLDALBORDA": (
        "ABBA",
        "ABDA",
        "ADOD",
        "ALBA",
        "ARAB",
        "ARAD",
        "ARRA",
        "BABA",
        "BADAR",
        "BALLA",
        "BALRA",
        "BOBA",
        "BODOR",
        "BORDA",
        "DADA",
        "DALOL",
        "DARA",
        "DARAB",
        "DOBOL",
        "LABDA",
        "LABOR",
        "LOLA",
        "LORD",
        "ODAAD",
        "OLDAL",
        "ORRA",
        "ORRAL",
        "ORRBA",
        "ORROD",
        "RABOL",
        "RADAR",
    ),
    "SZAVAZATOT": (
        "AVAS",
        "AVAT",
        "AZAZ",
        "OSZT",
        "SAVAS",
        "SAVAZ",
        "SZAVA",
        "SZTOA",
        "TASS",
        "TATA",
        "VASA",
        "VASAS",
        "VASAT",
        "VATTA",

    ),
    "TORZONBORZ": (
        "BONT",
        "BORT",
        "BORZ",
        "BRONZ",
        "NONO",
        "OROZ",
        "ORRON",
        "ORROT",
        "ROBOT",
        "RONT",
        "TOBOZ",
        "TORZ",
        "ZOBOR",
    ),
    "HALDARABKA": (
        "ABBA",
        "ABDA",
        "ABLAK",
        "ABRAK",
        "AKAD",
        "AKAR",
        "AKARD",
        "ALAK",
        "ALBA",
        "ALKAR",
        "ARAB",
        "ARAD",
        "ARRA",
        "BABA",
        "BADAR",
        "BAKA",
        "BALLA",
        "BALRA",
        "BARKA",
        "DADA",
        "DARA",
        "DARAB",
        "HADAD",
        "HADAR",
        "HADBA",
        "HADD",
        "HADRA",
        "HALA",
        "HALAD",
        "HALAK",
        "HALK",
        "HALL",
        "KABA",
        "KARBA",
        "KARD",
        "LABDA",
        "LAKK",
        "RADAR",
    ),
    "DALLAMOSAN": (
        "ADOD",
        "ADOM",
        "ADOMA",
        "ALMA",
        "ALOM",
        "ANNA",
        "DADA",
        "DALMA",
        "DALOL",
        "DALOS",
        "LOLA",
        "MALOM",
        "MAMA",
        "MANDA",
        "MANNA",
        "MASA",
        "MOLLA",
        "MOND",
        "MONDA",
        "MONDD",
        "MOSOM",
        "MOSSA",
        "NONO",
        "ODAAD",
        "OLDAL",
        "ONNAN",
        "OSON",
        "SAMOA",
        "SANDA",
        "SOMA",
    ),
    "CERUZARAJZ": (
        "ARCA",
        "ARCRA",
        "ARRA",
        "AURA",
        "AZAZ",
        "CUCC",
        "CUCCA",
        "EREJE",
        "ERRE",
        "EZER",
        "JURA",
        "RAJZ",
        "REZEZ",
        "RUCA",
        "UCCU",
        "UJJA",
        "ZACC",
        "ZAJA",

    ),
    "BIKAVIADAL": (
        "ABBA",
        "ABDA",
        "ABLAK",
        "AIDA",
        "AKAD",
        "AKIK",
        "ALAK",
        "ALAKI",
        "ALBA",
        "ALIBI",
        "ALIDA",
        "ALVA",
        "AVVAL",
        "BABA",
        "BAKA",
        "BAKI",
        "BALLA",
        "BIALA",
        "BIBI",
        "BIKA",
        "BIKAL",
        "BILI",
        "DADA",
        "DILI",
        "IDILL",
        "IKLAD",
        "ILKA",
        "ILLIK",
        "KABA",
        "KADA",
        "KAKA",
        "KIAD",
        "KLIKK",
        "LABDA",
        "LADIK",
        "LAKIK",
        "LAKK",
        "LAKLI",
        "LIBA",
        "LILI",
        "LILLA",
        "VALL",
        "VIDA",
        "VILLA",
    ),
}
