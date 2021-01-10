from spellchecker import SpellChecker
spell = SpellChecker()

class SpellCChecker:
    def __init__(self):
        pass

    def expand_query(self, word):

        list_spell = []
        most_close = spell.correction(word)
        list_spell.append(most_close)
        return list_spell

