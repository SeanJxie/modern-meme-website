"""
[_NOUN] represents a noun
[_ADJ] represents an adjective
[_PNOUN] represents an plural noun
[_VERB] represents an verb

"""

text = [
    {"top": "Top Text",
     "bot": "Bottom Text"},

    {"top": "Don't care",
     "bot": "Didn't ask"},

    {"top": "Society",
     "bot": "Bottom Text"},

    {"top": "When the [_NOUN]",
     "bot": "is [_ADJ]"},

    {"top": "My [_PNOUN] are",
     "bot": "are [_VERB]"},

    {"top": "This pic goes hard",
     "bot": "feel free to screenshot"},

    {"top": "",
    "bot": "what"},

    {"top": "I have committed several",
    "bot": "war crimes"},

    {"top": "",
    "bot": "war crimes"},

    {"top": "",
    "bot": "[_NOUN] moment"}
]


nouns = ["contribution","sister","inspector","editor","secretary","addition","member","distribution","mud","conclusion","policy","phone","series","comparison","revolution","manufacturer","requirement","skill","student","depth","income","flight","coffee","cell","education","obligation","math","person","gate","girlfriend","software","queen","recording","weakness","employee","variation","transportation","suggestion","virus","currency","fact","hotel","photo","relationship","song","arrival","singer","extent","bread","response"]
plural_nouns = list(map(lambda s: s + "s", nouns)) # lazy pluralization (makes it funnier i think)
adjectives = ["resonant","ill-informed","sneaky","womanly","tidy","entertaining","half","similar","suitable","gray","impolite","subdued","chubby","silent","testy","third","frail","awesome","possible","available","descriptive","gentle","hard-to-find","bouncy","soft","tense","languid","plastic","actually","pretty","uttermost","murky","petite","sudden","mysterious","decisive","feigned","yielding","busy","green","tangy","aboriginal","eager","fair","absorbing","literate","discreet","unbiased","smooth","heavenly"]
verbs = ["substitute","attack","reply","sleep","concede","increase","bounce","accumulate","access","colour","celebrate","slow","wave","enclose","negotiate","object","define","undergo","subject","lay","function","tremble","withdraw","trade","impose","hurt","shop","operate","leap","remain","place","urge","clean","arrange","rely","assert","produce","protect","going","vanish","prove","convince","blossom","oppose","disagree","load","enable","use","educate","presume"]