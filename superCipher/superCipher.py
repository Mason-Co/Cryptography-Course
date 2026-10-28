# 1) Add code for the Caesar Cipher to "SuperCipher".
# There should be code for both encrypt and decrypt mode. [group submission]
#
# 2) Run the Caesar Cipher functions in "SuperCipher".
# Submit sample runs in both encrypt and decrypt mode. [group submission]
#
# 3) Use the Caesar Hack to conduct a brute-force attack on a fairly long encrypted message.
# Indicate the key number that was needed to hack the message.
# Show a run of this code.  [individual submission]

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
# if number is mod 52 then it should show just the amount of letters, but that means if y + 1 = 122
# then mod 52 = 18. BUT what if I did letter - 65 to give just the starting range at 0. so for example,
# if I did F + 2 - 65 = 72 - 65 = 7 mod 52. Well what happens if t + 15 - 65 = 131 - 65 = 66 mod 52
# that then = 14, which then let me check what that would mean in my system, this is wrong. Maybe have
# a check to see if number goes above 122, if it does then subtract 5 and 6

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
        result = reverse(user_input, key)
    elif choice == "Caesar":
        if mode == "Encrypt":
            result = caesar(user_input, int(key))
        elif mode == "Decrypt":
            result = caesar(user_input, int(key) - (2 * int(key)))
    else:
        result = "Does not work."
    # Display the results
    output_text.insert(
        tk.END,
        f"Mode: {mode}\n"
        f"Selected Option: {choice}\n"
        f"Message:\n{result}"
    )

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
