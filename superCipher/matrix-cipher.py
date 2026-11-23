# Defining Variables/Constants
choice = input("Do you want to encrypt or decrypt? [e or d]:")
if choice == "e":
    M = [[6, 24, 1], [13, 16, 10], [20, 17, 15]]
if choice == "d":
    M = [[8, 5, 10], [21, 8, 21], [21, 12, 8]]
PN = [[0], [0], [0]]
CN = [[0], [0], [0]]
SYMBOLS = "abcdefghijklmnopqrstuvwxyz"
numSym = len(SYMBOLS)

# Getting Plain Text/Number Info
plainText = input("Enter Plain Text :").lower()
lenText = len(plainText)
while (lenText % 3 != 0):
    plainText += ' '
    lenText = len(plainText)

curPos = 0
cipherText = ""
while (curPos < len(plainText)):

    PN[0][0] = SYMBOLS.find(plainText[curPos])
    PN[1][0] = SYMBOLS.find(plainText[curPos + 1])
    PN[2][0] = SYMBOLS.find(plainText[curPos + 2])
    print("Plain Num is :" + str(PN))

    # Matrix Multiplication for Cipher Number
    CN = [[0], [0], [0]]
    for i in range(len(M)):
        for j in range(len(PN[0])):
            for k in range(len(PN)):
                CN[i][j] += M[i][k] * PN[k][j]
            CN[i][j] = CN[i][j] % numSym
    print("Cipher Num is :" + str(CN))

    # Compute Cipher Text
    cipherText += SYMBOLS[CN[0][0]]
    cipherText += SYMBOLS[CN[1][0]]
    cipherText += SYMBOLS[CN[2][0]]
    curPos += 3
print("Cipher Text is :" + cipherText)

exit(0)