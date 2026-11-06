# Detect English module
# https://www.nostarch.com/crackingcodes/ (BSD Licensed)
# To use, type this code:
#   import detectEnglish
#   detectEnglish.isEnglish(someString) # Returns True or False
# (There must be a "dictionary.txt" file in this directory with all
# English words in it, one word per line. You can download this from
# https://www.nostarch.com/crackingcodes/.)
UPPERLETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
LETTERS_AND_SPACE = UPPERLETTERS + UPPERLETTERS.lower() + ' \t\n'
def loadDictionary():
   dictionaryFile = open('../dictionary.txt')
   englishWords = {}
   for word in dictionaryFile.read().split('\n'):
      englishWords[word] = None
      dictionaryFile.close()
   return englishWords

def getEnglishCount(message):
   message = message.upper()
   message = removeNonLetters(message)
   possibleWords = message.split()
   if possibleWords == []:
      return 0.0 # No words at all, so return 0.0
   matches = 0
   for word in possibleWords:
      if word in ENGLISH_WORDS:
        matches += 1
   return float(matches) / len(possibleWords)

def removeNonLetters(message):
   lettersOnly = []
   for symbol in message:
      if symbol in LETTERS_AND_SPACE:
             lettersOnly.append(symbol)
   return ''.join(lettersOnly)

def getEnglishCharacter(message):
   message = message.upper()
   charCount = 0
   for char in message:
       if char in LETTERS_AND_SPACE:
           charCount += 1
   return charCount / len(message)

def isEnglish(message, wordPercentage=40, letterPercentage=90):
   # By default, 20% of the words must exist in the dictionary file, and
   # 85% of all the characters in the message must be letters or spaces
   # (not punctuation or numbers).
   print(f"Constants are Word% and Letter%: {wordPercentage}% and {letterPercentage}%\n")
   wordsMatch = getEnglishCount(message) * 100 >= wordPercentage
   numLetters = len(removeNonLetters(message))
   messageLettersPercentage = float(numLetters) / len(message) * 100
   lettersMatch = messageLettersPercentage >= letterPercentage
   return wordsMatch and lettersMatch

#mainline
ENGLISH_WORDS = loadDictionary()
plaintext = input ("Plaintext:\n")
print(f"English Character Percentage:\t{getEnglishCharacter(plaintext.replace(' ', ''))*100:.1f}%")
print(f"English Word Percentage:\t\t{getEnglishCount(plaintext)*100:.1f}%")
if isEnglish(plaintext):
   print("This is English.")
else:
   print("This does not show enough signs to be English.")