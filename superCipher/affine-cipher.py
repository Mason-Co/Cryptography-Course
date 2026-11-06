# Affine Cipher Encrypt/Decrypt
# Makes sure to use a prime number symbol set
# The formula is cipherText = a*plainText + b (mod 89)
# Get alphabet and Inputs from User
SYMBOLS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()-=[];,._+{}|:<>? "
n = len(SYMBOLS)
a = int(input("Enter the first number of the key(a):"))
b = int(input("Enter the second number of the key(b):"))
plainText = input ("Enter Plain Text:")
s = len(plainText)
cipherText = ""

#Encrypt Message Symbol by Symbol
for i in range(s):
    posPlain = SYMBOLS.find(plainText[i])
    posCipher = (posPlain * a + b) % n
    if plainText[i] == ' ':
        cipherText += ' '
    else:
        cipherText += SYMBOLS[posCipher]
print ("The Cipher Text: " + cipherText)

#Compute the Decryption Key
#The formula is plainText = c * cipherText + d (mod 89)
c = 0
d = 0
for i in range(n):
    if (i*a) % n == 1:
        c = i
d = (-1) * c * b % n
print ("The Decryption Keys are: ", str(c), " & ", str(d))


# ---- affine(): missing page, reconstructed. Decrypt one char at a time. ----
def affine (cipherText, c, d):
    plainText = ""
    for i in range(len(cipherText)):
        if cipherText[i] == ' ':
            plainText += ' '
        else:
            posCipher = SYMBOLS.find(cipherText[i])
            posPlain = (posCipher * c + d) % n
            plainText += SYMBOLS[posPlain]
    return plainText

# ---- testEnglish(): top of function was cut off by the OCR, reconstructed. ----
def testEnglish (cipherText):
    letPerMatch = 0
    numWords = 0
    words = cipherText.split(' ')
    t = len(words)
    for testword in words:
        if testword in englishWords:
            numWords += 1

    #letter percent match: how much of the text is alphabetic (English) vs. symbols
    letCount = 0
    for i in range(len(cipherText)):
        if cipherText[i].isalpha() or cipherText[i] == ' ':
            letCount += 1
    if (len(cipherText) > 0):
        letPerMatch = float(letCount/len(cipherText))*100

    numPerMatch = 0
    if (t>0):
        numPerMatch = float(numWords/t)*100

    if (letPerMatch > 75) and (numPerMatch > 25):
        print("\nWe have a possible match!")
        print("Letter Percent Match: " + str(int(letPerMatch)) + "%")
        print("Word Percent Match: " + str(int(numPerMatch)) + "%")
        return("Match")
    else:
        return("No Match")
# end TestEnglish Function

#Decrypting the message
def hack (cipherText):
    keysTested = 0
    startTime = time.time()
    for i in range(1,89):
        for j in range(0,89):
            plainText = affine(cipherText,i,j)
            #print ("i = ", i, "j = ", j)
            #print ("PlainText: ", plainText)
            test = testEnglish(plainText)
            keysTested += 1
            if (keysTested % 1000 == 0):
                print ("Keys Tested: ", keysTested)
            if test == "Match":
                print("Key " + str(i) + ", " + str(j) + " found!")
                print("Plain Text Guess:", plainText)
    endTime = time.time()
    totTime = endTime - startTime
    print("This took " + str(totTime) + " seconds.")
#end hack

#mainline
import time
print ("Welcome to the Affine Cipher...")

#load dictionary
dictionaryFile = open('../dictionary.txt')
englishWords = []
for word in dictionaryFile.read().split('\n'):
    englishWords.append(word)
dictionaryFile.close()
print ("Dictionary Loaded...")

#calling hack
cT = input ("Enter the Cipher Text:")
#cT = "L%A1 A1 | ]>1] xU ]%> Phm0 >D>dr>aoM Rdx|@o|1] 1M1]>D"
hack(cT)
print("Program Ending ... ")
exit(0)
