import rsa
from cryptography.fernet import Fernet

#create key and store in file
key = Fernet.generate_key()
print ("The key is:", key)
fkey = open("filekey.txt",'wb')
fkey.write(key)
fkey.close()
print ("Key stored in file.")

#read in key
fkey = open("filekey.txt",'rb')
key = fkey.read()
cipher = Fernet(key)
print ("Key read from file.")

#read in file
filename = 'secret.txt'
with open(filename, 'rb') as file1:
    inFile = file1.read()
print ("Data file read in.")

#encrypt file
encryptedFile = cipher.encrypt(inFile)
newfilename = filename + "encrypted"
with open(newfilename, 'wb') as file2:
    file2.write(encryptedFile)
print ("Encrypted data file created.")

#decrypt data
fkey = open("filekey.txt",'rb')
key = fkey.read()
cipher = Fernet(key)
with open(newfilename, 'rb') as file3:
    encryptedData = file3.read()
decryptedFile = cipher.decrypt(encryptedData)
print ("Data decrypted.")

#store decrypted data
with open(filename + "decrypted", 'wb') as file4:
    file4.write(decryptedFile)
print ("Decrypted data file created.")
exit()

