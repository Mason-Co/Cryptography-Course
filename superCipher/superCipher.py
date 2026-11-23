# ##################################################
# Programmer: Jonathan Zderad with some iterative
#    help from ChatGPT
# Date: June 22, 2026
# Program : Crypto
# Creates a GUI window that allows the user to either
# encrypt or decrypt a message, using one of a
# selection of ciphers.
# ##################################################
import tkinter as tk
import random
import secrets
import math

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
SYMBOLS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()-=[];,._+{}|:<>? "
ALPH_NUM = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"
ALPH_LOWER = "abcdefghijklmnopqrstuvwxyz"
symLen = len(SYMBOLS)

def reverse(astring):
    return astring[::-1]

def caesar(astring, akey):
    nstring = ""
    for char in astring:
        if char not in ALPHABET:
            nstring += char
            continue
        index = ALPHABET.index(char)
        nstring += ALPHABET[(index + akey) % 52]
    return nstring

def encryptTransposition(key, message):
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

def decryptTransposition(key, message):
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

def encryptAffine(key, message):
    keyList = key.split(' ')
    s = len(message)
    cipherText = ""

    for i in range(s):
        posPlain = SYMBOLS.find(message[i])
        posCipher = (posPlain * int(keyList[0]) + int(keyList[1])) % symLen
        if message[i] == ' ':
            cipherText += ' '
        else:
            cipherText += SYMBOLS[posCipher]

    c = 0
    d = 0
    for i in range(symLen):
        if (i * int(keyList[0])) % symLen == 1:
            c = i
    d = (-1) * c * int(keyList[1]) % symLen
    decKeys = [c, d]
    return cipherText, decKeys

def decryptAffine(key, cipherText):
    plainText = ""
    c, d = key.split(' ')
    for i in range(len(cipherText)):
        if cipherText[i] == ' ':
            plainText += ' '
        else:
            posCipher = SYMBOLS.find(cipherText[i])
            posPlain = (posCipher * int(c) + int(d)) % symLen
            plainText += SYMBOLS[posPlain]
    return plainText

def encryptSubstitution(key, message):
    cipherText = ""
    key = f"{key.upper()}{key}"
    for char in message:
        if char in ALPHABET:
            symbolIndex = ALPHABET.find(char)
            cipherText = cipherText + key[symbolIndex]
        else:
            cipherText = cipherText + char
    return cipherText

def decryptSubstitution(key, cipherText):
    plainText = ""
    key = f"{key.upper()}{key}"
    for char in cipherText:
        if char in ALPHABET:
            keyIndex = key.find(char)
            plainText = plainText + ALPHABET[keyIndex]
        else:
            plainText = plainText + char
    return plainText

def isInvertible(M):
    # A matrix can be decrypted only if its determinant has no factor in common with 26
    det = sum(M[0][j] * cofactor(M, 0, j) for j in range(3)) % 26
    return det % 2 != 0 and det % 13 != 0

def matrixKeyToMatrix(key):
    # Turns ANY key into a 3x3 matrix that can be encrypted AND decrypted
    if key.strip() == "":
        raise ValueError("Please enter a key")

    # If the key is exactly 9 letters and works as a matrix, use it directly
    cleaned = key.lower().replace(" ", "")
    if len(cleaned) == 9 and cleaned.isalpha():
        nums = [ALPH_LOWER.find(c) for c in cleaned]
        M = [nums[0:3], nums[3:6], nums[6:9]]
        if isInvertible(M):
            return M

    # Otherwise, build a matrix from the key text. Seeding with the key means
    # the same key always gives the same matrix.
    rng = random.Random(key)
    while True:
        M = [[rng.randrange(26) for _ in range(3)] for _ in range(3)]
        if isInvertible(M):
            return M

def cofactor(M, r, c):
    rows = [x for x in range(3) if x != r]
    cols = [x for x in range(3) if x != c]
    minor = (M[rows[0]][cols[0]] * M[rows[1]][cols[1]]
             - M[rows[0]][cols[1]] * M[rows[1]][cols[0]])
    return ((-1) ** (r + c)) * minor

def invertMatrix(M):
    # Inverse of a 3x3 matrix mod 26 (this is what gives you the decryption matrix)
    numSym = len(ALPH_LOWER)
    det = sum(M[0][j] * cofactor(M, 0, j) for j in range(3)) % numSym
    detInv = None
    for i in range(numSym):
        if (det * i) % numSym == 1:
            detInv = i
    if detInv is None:
        raise ValueError("That key can't be decrypted (try a different 9 letter key)")
    return [[(detInv * cofactor(M, j, i)) % numSym for j in range(3)] for i in range(3)]

def matrixCipher(key, message, mode):
    M = matrixKeyToMatrix(key)
    if mode == "Decrypt":
        M = invertMatrix(M)

    numSym = len(ALPH_LOWER)
    # Keep only letters, lowercase
    text = "".join(c for c in message.lower() if c in ALPH_LOWER)

    if mode == "Encrypt":
        while len(text) % 3 != 0:
            text += 'x'          # pad with x (a space isn't in SYMBOLS)
    elif len(text) % 3 != 0:
        raise ValueError("Encrypted text must be a multiple of 3 letters")

    PN = [[0], [0], [0]]
    curPos = 0
    cipherText = ""
    while curPos < len(text):
        PN[0][0] = ALPH_LOWER.find(text[curPos])
        PN[1][0] = ALPH_LOWER.find(text[curPos + 1])
        PN[2][0] = ALPH_LOWER.find(text[curPos + 2])

        # Matrix Multiplication for Cipher Number
        CN = [[0], [0], [0]]
        for i in range(len(M)):
            for j in range(len(PN[0])):
                for k in range(len(PN)):
                    CN[i][j] += M[i][k] * PN[k][j]
                CN[i][j] = CN[i][j] % numSym

        # Compute Cipher Text
        cipherText += ALPH_LOWER[CN[0][0]]
        cipherText += ALPH_LOWER[CN[1][0]]
        cipherText += ALPH_LOWER[CN[2][0]]
        curPos += 3
    return cipherText


# noinspection DuplicatedCode
def OTP(key = '', message= '', mode= ''):
    keyPos = 0
    numKey = len(key)
    numSym = len(SYMBOLS)
    numMessage = len(message)
    plainText = ''
    cipherText = ''

    if mode == "Decrypt":
        for symbol in message:
            if symbol in SYMBOLS:
                symbolIndex = SYMBOLS.find(symbol)  # where is the current plain text character?
                keyIndex = SYMBOLS.find(key[keyPos])  # where is the current key character?
                plainIndex = symbolIndex - keyIndex  # compute cipher Index
                plainIndex = plainIndex % numSym
                plainText = plainText + SYMBOLS[plainIndex]
            else:
                plainText = plainText + symbol  # no change if not in symbols
            keyPos += 1  # increment key
            keyPos = keyPos % numKey
        return plainText
    elif mode == "Encrypt":
        plainText = message
        key = ''
        for i in range(numMessage):
            key += secrets.choice(ALPH_NUM)
        numKey = len(key)

        for symbol in plainText:
            if symbol in SYMBOLS:
                symbolIndex = SYMBOLS.find(symbol)  # where is the current plain text character?
                keyIndex = SYMBOLS.find(key[keyPos])  # where is the current key character?
                cipherIndex = symbolIndex + keyIndex  # compute cipher Index
                cipherIndex = cipherIndex % numSym
                cipherText = cipherText + SYMBOLS[cipherIndex]
            else:
                cipherText = cipherText + symbol  # no change if not in symbols
            keyPos += 1  # increment key
            keyPos = keyPos % numKey
        return cipherText, key
    return "Error."

def wild(key = '', message = '', mode = ''):
    keyPos = 0
    numSym = len(SYMBOLS)
    plainText = ''
    cipherText = ''
    if mode == "Decrypt":
        half = len(key) // 2
        bundle = OTP(key[half:], key[:half], "Decrypt")
        tranKey, subKey, OTPKey = bundle.split(' ')
        numKey = len(OTPKey)
        #OTP Decryption Section
        for symbol in message:
            if symbol in SYMBOLS:
                symbolIndex = SYMBOLS.find(symbol)  # where is the current plain text character?
                keyIndex = SYMBOLS.find(OTPKey[keyPos])  # where is the current key character?
                plainIndex = symbolIndex - keyIndex  # compute cipher Index
                plainIndex = plainIndex % numSym
                plainText = plainText + SYMBOLS[plainIndex]
            else:
                plainText = plainText + symbol  # no change if not in symbols
            keyPos += 1  # increment key
            keyPos = keyPos % numKey
        #Caesar Decryption Section
        plainText = caesar(plainText, -12)

        #Substitution Decryption Section
        plainText = decryptSubstitution(subKey, plainText)

        #Reverse Decryption Section
        plainText = plainText[::-1]

        #Transposition Decryption Section
        plainText = decryptTransposition(int(tranKey), plainText)

        return plainText
    if mode == "Encrypt":
        #Transposition Encryption Section
        cipherText = encryptTransposition(int(key), message)

        #Reverse Encryption Section
        cipherText = reverse(cipherText)

        #Substitution Encryption Section
        subKeyList = list(ALPH_LOWER)
        random.shuffle(subKeyList)
        subKey = "".join(subKeyList)

        cipherText = encryptSubstitution(subKey, cipherText)

        #Caesar Encryption Section
        caesarKey = 12

        cipherText = caesar(cipherText, caesarKey)

        #OTP Encryption Section
        numMessage = len(cipherText)
        finalCipher = ""
        OTPKey = ''

        for i in range(numMessage):
            OTPKey += secrets.choice(ALPH_NUM)
        numKey = len(OTPKey)

        for symbol in cipherText:
            if symbol in SYMBOLS:
                symbolIndex = SYMBOLS.find(symbol)  # where is the current plain text character?
                keyIndex = SYMBOLS.find(OTPKey[keyPos])  # where is the current key character?
                cipherIndex = symbolIndex + keyIndex  # compute cipher Index
                cipherIndex = cipherIndex % numSym
                finalCipher = finalCipher + SYMBOLS[cipherIndex]
            else:
                finalCipher = finalCipher + symbol  # no change if not in symbols
            keyPos += 1  # increment key
            keyPos = keyPos % numKey

        bundle = f"{key} {subKey} {OTPKey}"  # "transKey subKey otpKey"
        keyCipher, keyPad = OTP('', bundle, "Encrypt")
        keyOTP = keyCipher + keyPad

        return finalCipher, keyOTP

    return "Error."

def make_options():
    # Radio button options
    options = [
        "Affine",
        "Caesar",
        "Matrix",
        "One-Time Pad",
        "Reverse",
        "Substitution",
        "Transposition",
        "Wild"
    ]

    # Create radio buttons
    for option in options:
        rb = tk.Radiobutton(
            root,
            text=option,
            variable=selected_option,
            value=option
        )
        rb.pack(anchor="w", padx=10)

def make_mode():
    # Create mode option
    # Encrypt / Decrypt selection

    for mode in ["Encrypt", "Decrypt"]:
        rb = tk.Radiobutton(
            root,
            text=mode,
            variable=selected_mode,
            value=mode
        )
        rb.pack(anchor="w", padx=20)

def process_input():
    # Get the buttons and boxes
    choice = selected_option.get()
    mode = selected_mode.get()
    key = key_entry.get()
    user_input = input_entry.get()
    output_text.delete("1.0", tk.END)
    if choice == "Reverse":
        result = reverse(user_input)
    elif choice == "Caesar":
        if mode == "Encrypt":
            result = caesar(user_input, int(key))
        elif mode == "Decrypt":
            result = caesar(user_input, int(key) - (2 * int(key)))
    elif choice == "Transposition":
        if mode == "Encrypt":
            result = encryptTransposition(int(key), user_input)
        elif mode == "Decrypt":
            result = decryptTransposition(int(key), user_input)
    elif choice == "Affine":
        if mode == "Encrypt":
            message, keys = encryptAffine(key, user_input)
            result = f"{message}\nThe Decryption Keys are: {keys[0]} & {keys[1]}"
        elif mode == "Decrypt":
            result = decryptAffine(key, user_input)
    elif choice == "Substitution":
        if mode == "Encrypt":
            result = encryptSubstitution(key, user_input)
        elif mode == "Decrypt":
            result = decryptSubstitution(key, user_input)
    elif choice == "Matrix":
        result = matrixCipher(key, user_input, mode)
    elif choice == "One-Time Pad":
        if mode == "Encrypt":
            message, key = OTP(key, user_input, mode)
            result = f"{message}\nRandom Key:\n{key}"
        if mode == "Decrypt":
            result = OTP(key, user_input, mode)
    elif choice == "Wild":
        if mode == "Encrypt":
            message, key = wild(key, user_input, mode)
            result = f"{message}\nRandom Key:\n{key}"
        if mode == "Decrypt":
            result = wild(key, user_input, mode)
    else:
        result = "Does not work."
    # Display the results
    output_text.insert(
        tk.END,
        f"Mode: {mode}\n"
        f"Selected Option: {choice}\n"
        f"Message:\n{result}"
    )

if __name__ == "__main__":
    #Mainline of Program
    #make root for window
    root = tk.Tk()
    root.title("Cipher Tester")

    #make option subwindow
    selected_option = tk.StringVar(value="Reverse")
    tk.Label(root, text="Cipher:").pack(anchor="w", padx=10, pady=(10, 0))
    make_options()

    #make mode subwindow
    selected_mode = tk.StringVar(value="Encrypt")
    tk.Label(root, text="Mode:").pack(anchor="w", padx=10, pady=(10, 0))
    make_mode()

    #Get Input Ready
    tk.Label(root, text="Input:").pack(anchor="w", padx=10, pady=(10, 0))
    input_entry = tk.Entry(root, width=40)
    input_entry.pack(padx=10, pady=5)

    #Get Key Box Ready
    tk.Label(root, text="Key:").pack(anchor="w", padx=10, pady=(10, 0))
    key_entry = tk.Entry(root, width=40)
    key_entry.pack(padx=10, pady=5)

    # Process Submit Button
    tk.Button(
        root,
        text="Submit",
        command=process_input
    ).pack(pady=10)

    # Make Output Box
    tk.Label(root, text="Output:").pack(anchor="w", padx=10)
    output_text = tk.Text(root, width=50, height=5)
    output_text.pack(padx=10, pady=5)
    root.mainloop()
