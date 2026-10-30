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
import math

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

def reverse(astring, akey):
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
    key = int(key_entry.get())
    user_input = input_entry.get()
    output_text.delete("1.0", tk.END)
    if choice == "Reverse":
        result = reverse(user_input, key)
    elif choice == "Caesar":
        if mode == "Encrypt":
            result = caesar(user_input, int(key))
        elif mode == "Decrypt":
            result = caesar(user_input, int(key) - (2 * int(key)))
    elif choice == "Transposition":
        if mode == "Encrypt":
            result = encryptTransposition(key, user_input)
        elif mode == "Decrypt":
            result = decryptTransposition(key, user_input)
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
