#this accomplished AES for short messages
from cryptography.fernet import Fernet
receiver = input ("Please log into the network >>")
#key generation
if receiver != "Bob":
    print ("Error logging into network")
    exit ()
key = Fernet.generate_key()
print ("Your key has been sent.")

#message generation
sender = input ("Please log into the network >>")
if sender != "Alice":
  print ("Error logging into network")
  exit()
print ("Alice the secret key is :", key)
print ("Make sure no one else knows")
message = input('Secret Message: ').encode('utf-8')

#message encryption
cipher = Fernet(key)
encryptedText = cipher.encrypt(message)
print("The encrypted message is :", encryptedText)
print("Encrypted Message has been sent.")

#message decryption
receiver = input ("Please log into the network >>")
if receiver != "Bob":
  print("Error logging into network")
  exit()
originalText = cipher.decrypt(encryptedText)
print("Plain Text is: ", originalText)
print("Logging Out")