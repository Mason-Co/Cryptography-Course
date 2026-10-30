from superCipher import encryptTransposition, decryptTransposition
import random
import sys

def tester():
   random.seed(42) # Set the random "seed" to a static value.
   fails = 0
   for i in range(1000): # Run 20 tests.
      # Generate random messages to test.
      # The message will have a random length:
      message = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ    ' * random.randint(4, 40)
      # Convert the message string to a list to shuffle it:
      message = list(message)
      random.shuffle(message)
      message = ''.join(message) # Convert the list back to a string.
      # Check all possible keys for each message:
      for key in range(1, int(len(message)/2)):
          encrypted = encryptTransposition(key, message)
          decrypted = decryptTransposition(key, encrypted)

          # If the decryption doesn't match the original message, display
          # an error message and quit:
          if message != decrypted:
             print('Mismatch with key %s and message %s.' % (key, message))
             print('Decrypted as: ' + decrypted)
             fails += 1
             sys.exit()
      if i % 100 == 0 and i != 0:
         print(i, "encryptions completed.")
   completions = 1000 - fails
   comp_percent = completions / completions * 100
   print(f'Transposition cipher test completed.\n{comp_percent:.2f}% of test messages passed.')

if __name__ == "__main__":
   tester()