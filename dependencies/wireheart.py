from secrets import SystemRandom
from string import ascii_letters
from collections import deque
from copy import deepcopy

ALPHABET_ASCII = [char for char in ascii_letters]
ALPHABET_ASCII.extend([" ", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"])
ALPHABET_ASCII = deque(ALPHABET_ASCII)
ALPHABET_WIREHEART = deque(["ˤ", "‽", "ӻ", "ȣ", "฿", "΅", "ē", "Ⴤ", "ϫ", "ȵ", "α", "β", "δ", "ɲ", "ʬ",
                            "Ք", "ʩ", "ಸ", "æ", "ɨ", "ъ", "מ", "ཪ", "λ", "ֆ", "ͼ", "˥",
                            "ȿ", "ɏ", "ɂ", "Ѷ", "ԙ", "ҽ", "ϻ", "ˢ", "ϗ", "ǝ", "ץ", "҂", "ी", "৬", "౫",
                            "໑", "༅", "໒", "æ", "༒", "༬", "࿐", "ᄋ", "ኦ", "ᇫ", "᎙", "Ꭿ",
                            "Ω", "θ", "σ", "ρ", "τ", "χ", "ι", "π", "ς", "ʨ"])
RANDOM_OBJ = SystemRandom()


def encrypt(message: str):
    encrypted_message_raw = []
    wire = (f"{RANDOM_OBJ.randint(0, 9)}{RANDOM_OBJ.randint(0, 9)}", str(RANDOM_OBJ.randint(1, 9)))
    wire_str = f"{wire[0]}{wire[1]}"
    encrypted_wire_str = [ALPHABET_WIREHEART[ALPHABET_ASCII.index(l)] for l in wire_str]
    encrypted_message_raw.append(encrypted_wire_str)

    shift_value = int(wire[0]) * int(wire[1])
    temp = deepcopy(ALPHABET_WIREHEART)
    temp.rotate(shift_value)
    shifted_alphabet = temp

    for letter in message:
        try:
            encrypted_message_raw.append(shifted_alphabet[ALPHABET_ASCII.index(letter)])
        except ValueError:
            encrypted_message_raw.append(letter)

    encrypted_message_raw = [item for sublist in encrypted_message_raw for item in sublist]
    encrypted_message = "".join(encrypted_message_raw)
    return encrypted_message


def decrypt(message: str):
    encrypted_wire_str = message[:3]
    wire_str = ""
    for letter in encrypted_wire_str:
        wire_str += ALPHABET_ASCII[ALPHABET_WIREHEART.index(letter)]
    wire = (wire_str[:2], wire_str[2])

    shift_value = int(wire[0]) * int(wire[1])
    temp = deepcopy(ALPHABET_WIREHEART)
    temp.rotate(shift_value)
    shifted_alphabet = temp

    decrypted_message_raw = []
    for letter in message[3:]:
        try:
            decrypted_message_raw.append(ALPHABET_ASCII[shifted_alphabet.index(letter)])
        except ValueError:
            decrypted_message_raw.append(letter)

    decrypted_message = "".join(decrypted_message_raw)
    return decrypted_message


if __name__ == "__main__":
    while True:
        enc = encrypt(input())
        print(enc)
        print(decrypt(enc))
