# day8.py# day8.py

direction = input("type encode to encrypt, type decode to decrypt: \n").lower()
text = input("Type your message: \n").lower()
shift = int(input("Type the shift number: \n"))


def encrypt(orginal_text, shift_amount):
    cipher_text = ""
    for char in orginal_text:
        if char.isalpha():
            shifted = ord(char) + shift_amount
            if char.islower():
                if shifted > ord("z"):
                    shifted -= 26
            elif char.isupper():
                if shifted > ord("Z"):
                    shifted -= 26
            cipher_text += chr(shifted)
        else:
            cipher_text += char
    return cipher_text


def decrypt(cipher_text, shift_amount):
    original_text = ""
    for char in cipher_text:
        if char.isalpha():
            shifted = ord(char) - shift_amount
            if char.islower():
                if shifted < ord("a"):
                    shifted += 26
            elif char.isupper():
                if shifted < ord("A"):
                    shifted += 26
            original_text += chr(shifted)
        else:
            original_text += char
    return original_text


if direction == "encode":
    result = encrypt(text, shift)
    print(f"The encoded text is: {result}")
elif direction == "decode":
    result = decrypt(text, shift)
    print(f"The decoded text is: {result}")
# This script provides a simple encryption and decryption mechanism using a Caesar cipher.

cont = input("type yes if you want to go again, type no if you want to exit\n").lower()
while cont == "yes":
    direction = input("type encode to encrypt, type decode to decrypt: \n").lower()
    text = input("Type your message: \n").lower()
    shift = int(input("Type the shift number: \n"))

    if direction == "encode":
        result = encrypt(text, shift)
        print(f"The encoded text is: {result}")
    elif direction == "decode":
        result = decrypt(text, shift)
        print(f"The decoded text is: {result}")

    cont = input(
        "type yes if you want to go again, type no if you want to exit\n"
    ).lower()
