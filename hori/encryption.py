#############################################
#                                           #
#             Encryption Module             #
#                                           #
#  Author: Shan                             #
#                                           #
#############################################

# Importing necessary library
from cryptography.fernet import Fernet

# Initialize encryption keys
f = Fernet(b'EOgjfZAViNS8Y9cYCk9p-Hz62zx8LScNqtvKmJX_8EY=')

#Function to encrypt string
def encrypt(strs):
    return f._encrypt_from_parts(strs.encode('UTF-8'), 0,b'\xbd\xc0,\x16\x87\xd7G\xb5\xe5\xcc\xdb\xf9\x07\xaf\xa0\xfa').decode()

#Function to decrypt string
def decrypt(strs):
    return f._encrypt_from_parts(strs, 0,b'\xbd\xc0,\x16\x87\xd7G\xb5\xe5\xcc\xdb\xf9\x07\xaf\xa0\xfa').decode('UTF-8').decode()

if __name__=="__main__":
    while 1:
        print(encrypt(input()))