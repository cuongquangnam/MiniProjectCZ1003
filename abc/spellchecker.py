import re
from collections import Counter

class SpellChecker:
    def __init__(self):
        def words(text): return re.findall(r'\w+', text.lower())
        self.WORDS = Counter(words(open('menu_items.txt').read()))
        self.N=sum(self.WORDS.values())
        #WORDS is a dictionary of all the words in menu_items.txt, which is all the words from menu items in canteen db
         #  keys are the words that appear and values are the times it appear
    def P(self,word):
    # "Probability of `word`."
        return self.WORDS[word] / self.N

    def correction(self,word):
    # "Most probable spelling correction for word." >> return the word based on the highest probability out of WORDS data set
        return max(self.candidates(word), key=self.P)

    def candidates(self,word):
    #"Generate possible spelling corrections for word."  #based on the first non empty set in order of priority,
    #if word is already in known list of WORDS, or words 1 edit distance away is in known list of words, 2 edits, or just word if it is not known.
        return (self.known([word]) or self.known(self.edits1(word)) or self.known(self.edits2(word)) or [word])

    def known(self,words):
   # "The subset of `words` that appear in the dictionary of WORDS."
        return set(w for w in words if w in self.WORDS)

    def edits1(self,word):
    #" return set of All edits that are one edit away from `word`."
        letters    = 'abcdefghijklmnopqrstuvwxyz'
        splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]  #split the words for manipulation
        deletes    = [L + R[1:]               for L, R in splits if R]        #words that have one letter deleted
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]   #words that swap position of one letter
        replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters] #words that replace one letter with another alphabet
        inserts    = [L + c + R               for L, R in splits for c in letters]  #words that insert one letter in between word
        return set(deletes + transposes + replaces + inserts)

    def edits2(self,word):
    #"All edits that are two edits away from `word`."
        return (e2 for e1 in self.edits1(word) for e2 in self.edits1(e1))

    #adapted from http://norvig.com/spell-correct.html

   #### we only need to use this commands
s = SpellChecker()
#INPUT >>
print(s.correction('befe')) #command to return most likely spell corrected word
#OUTPUT>>>> 'chicken'
