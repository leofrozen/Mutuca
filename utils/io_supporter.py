import random, struct,  sys
import hashlib
from Crypto.Cipher import AES


#file_var = ""

password = 'essa eh uma frase muito secreta e por isso se chama password'
defkey = hashlib.sha256(password).digest()


def encrypt_file(in_data, key = defkey,  out_filename=None, chunksize=64*1024):
    """ Encrypts a file using AES (CBC mode) with the
        given key.

        key:
            The encryption key - a string that must be
            either 16, 24 or 32 bytes long. Longer keys
            are more secure.

        in_filename:
            Name of the input file

        out_filename:
            If None, '<in_filename>.enc' will be used.

        chunksize:
            Sets the size of the chunk which the function
            uses to read and encrypt the file. Larger chunk
            sizes can be faster for some files and machines.
            chunksize must be divisible by 16.
    """
    if not out_filename:
        out_filename = in_data + '.mut'

    iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    
    in_data = str(in_data)
    filesize = sys.getsizeof(in_data)
    with open(out_filename, 'wb') as outfile:
        outfile.write(struct.pack('<Q', filesize))
        outfile.write(iv)
        
        while True: 
            chunk = in_data[:chunksize]
            aux = in_data.replace(chunk, "", 1)
            in_data = str(aux)
            
            if len(chunk) == 0:
                break
            elif len(chunk) % 16 != 0:
                chunk += ' ' * (16 - len(chunk) % 16)
            outfile.write(encryptor.encrypt(chunk))



def decrypt_file(in_filename, key = defkey,  chunksize=24*1024):

    file_var = ""
    with open(in_filename, 'rb') as infile:
        struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        while True:
            chunk = infile.read(chunksize)
            if len(chunk) == 0:
                break
            file_var +=  decryptor.decrypt(chunk)
    return file_var

