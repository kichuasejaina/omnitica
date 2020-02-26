from cryptography.fernet import Fernet


def encoder():
    key = Fernet.generate_key()
    encrypter = Fernet(key)
    length_of_key = len(key)
    user_input1 = input("Please enter the string to encode: ")
    if user_input1.strip('\n').strip('\r') == '':
        print("Need to provide string to encode. Exiting!!!!!!")
    else:
        user_input2 = input("Please confirm the string to encode: ")
        if (user_input1.strip('\n').strip('\r') != user_input2.strip('\n').strip('\r')):
            print("String mismatch... Exiting!!")
        else:
            user_input = user_input1.strip('\n').strip('\r')
            encrypted_data = encrypter.encrypt(user_input.encode()).decode()
            print("{}#{}{}".format(length_of_key, key.decode(), encrypted_data))


def decoder(encoded_string):
    keylength = int(encoded_string.split('#')[0])
    data = "#".join(encoded_string.split('#')[1:])
    key = data[:keylength].encode()
    encrypted_data = data[keylength:].encode()
    decrypter = Fernet(key)
    decrypted_data = decrypter.decrypt(encrypted_data).decode().strip('\n').strip('\r')
    return decrypted_data

##
