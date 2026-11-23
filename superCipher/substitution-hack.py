# Substitution Hack
# With guidance from Sweigart, Page 209-210

print("Substitution Hack Beginning...")
SYMBOLS = 'abcdefghijklmnopqrstuvwxyz'
FREQ_ORDER = 'etaoinshrdlcumwfgypbvkjxqz'

cipherText = "Sy l nlx sr pyyacao l ylwj eiswi upar lulsxrj isr sxrjsxwjr, ia esmm\n"
cipherText += "rwctjsxsza sj wmpramh, lxo txmarr jia aqsoaxwa sr pqaceiamnsxu, ia esmm caytra\n"
cipherText += "jp famsaqa sj.  Sy, px jia pijac ilxo, ia sr pyyacao rpnajisxu eiswi lyypcor\n"
cipherText += "l calrpx ypc lwjsxu sx lwwpcolxwa jp isr scrjsxwjr, ia esmm lwwabj sj aqax\n"
cipherText += "px jia rmsuijarj aqsoaxwa. Jia pcsusx py nhjir sr agbmlsxao sx jisr elh.\n"
cipherText += "-Facjclxo Ctrramm"

cipherText = cipherText.lower()
print("Cipher Text: \n" + cipherText)

#initialize letterCount List
letterCount = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
print(str(letterCount))

for letter in cipherText:
    if letter in SYMBOLS:
        pos = SYMBOLS.find(letter)
        letterCount[pos] += 1

print("\nLetter Analysis")
print(str(letterCount))

guessKey = ['.'] * 26

for rank in range(26):
    maxIndex = letterCount.index(max(letterCount))
    guessKey[maxIndex] = FREQ_ORDER[rank]
    letterCount[maxIndex] = -1

print("\nPossible key:")
print(''.join(guessKey))

print("Enter the Substitution Key (must be 26 characters long):")
KEY = input()
plainText = ''

for symbol in cipherText:
    if symbol in SYMBOLS:
        symbolIndex = SYMBOLS.find(symbol)
        plainText = plainText + KEY[symbolIndex]
    else:
        plainText = plainText + symbol
print("Plain Text: "+ plainText)
print("Substitution Hack Ending ...")