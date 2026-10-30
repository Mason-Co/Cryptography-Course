# Detect English module
# https://www.nostarch.com/crackingcodes/ (BSD Licensed)
# (There must be a "dictionary.txt" file in this directory with all
# English words in it, one word per line. You can download this from
# https://www.nostarch.com/crackingcodes/.)
import math
UPPERLETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
LETTERS_AND_SPACE = UPPERLETTERS + UPPERLETTERS.lower() + ' \t\n'

def encryptMessage(key, message):
   # Each string in ciphertext represents a column in the grid:
   ciphertext = [''] * key
   # Loop through each column in ciphertext:
   for column in range(key):
      currentIndex = column
      # Keep looping until currentIndex goes past the message length:
      while currentIndex < len(message):
         # Place the character at currentIndex in message at the
         # end of the current column in the ciphertext list:
         ciphertext[column] += message[currentIndex]
         # Move currentIndex over:
         currentIndex += key
         # Convert the ciphertext list into a single string value and return it:
   return ''.join(ciphertext)

def decryptMessage(key, message):
   # The transposition decrypt function will simulate the "columns" and
   # "rows" of the grid that the plaintext is written on by using a list
   # of strings. First, we need to calculate a few values.
   # The number of "columns" in our transposition grid:
   numOfColumns = int(math.ceil(len(message) / float(key)))
   numOfRows = key
   # The number of "shaded boxes" in the last "column" of the grid:
   numOfShadedBoxes = (numOfColumns * numOfRows) - len(message)
   # Each string in plaintext represents a column in the grid:
   plaintext = [''] * numOfColumns
   column = 0
   row = 0
   for symbol in message:
      plaintext[column] += symbol
      column += 1  # Point to the next column.
      # If there are no more columns OR we're at a shaded box, go back
      # to the first column and the next row:
      if (column == numOfColumns) or (column == numOfColumns - 1 and
                                row >= numOfRows - numOfShadedBoxes):
         column = 0
         row += 1
   return ''.join(plaintext)

def loadDictionary():
   dictionaryFile = open('dictionary.txt')
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

def isEnglish(message, wordPercentage=20, letterPercentage=85):
   # By default, 20% of the words must exist in the dictionary file, and
   # 85% of all the characters in the message must be letters or spaces
   # (not punctuation or numbers).
   wordsMatch = getEnglishCount(message) * 100 >= wordPercentage
   numLetters = len(removeNonLetters(message))
   messageLettersPercentage = float(numLetters) / len(message) * 100
   lettersMatch = messageLettersPercentage >= letterPercentage
   return wordsMatch and lettersMatch

def hackTransposition(message):
   print('Hacking...')
   # Python programs can be stopped at any time by pressing
   # Ctrl-C (on Windows) or Ctrl-D (on macOS and Linux):
   print('(Press Ctrl-C (on Windows) or Ctrl-D (on macOS and Linux) to quit at any time.)')

   # Brute-force by looping through every possible key:
   for key in range(1, len(message)):
      print('Trying key #%s...' % (key))
      decryptedText = decryptMessage(key, message)
      if isEnglish(decryptedText):
         # Ask user if this is the correct decryption:
         print()
         print('Possible encryption hack:')
         print('Key %s: %s' % (key, decryptedText[:100]))
         print()
         print('Enter D if done, anything else to continue hacking:')
         response = input('> ')
         if response.strip().upper().startswith('D'):
            return decryptedText
   return None

#mainline
# You might want to copy & paste this text from the source code at
# https://www.nostarch.com/crackingcodes/:
ENGLISH_WORDS = loadDictionary()
myMessage = input ("Enter Text:")
#This determins whether the message is English text
print("Is this English?")
print(isEnglish(myMessage))
myMessage = encryptMessage(6,myMessage)
print("Cipher Text:" + myMessage)
#This tries transposition hack if message is not English text
hackedMessage = hackTransposition(myMessage)
if hackedMessage == None:
   print('Failed to hack encryption')
else:
      print("Plain Text:", hackedMessage)
