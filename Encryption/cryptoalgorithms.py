import random
import re


class Crypt:
    def __init__(self, text, key, file, algorithm, action):
        self.text = text
        self.key = key
        self.file = file
        self.file_info = self.handle_file(file)
        self.algorithm = algorithm
        self.action = action
        self.result = self.crypt(text, key, self.file_info, algorithm, action)
        self.file_result = self.handle_file_result(self.file, self.result)

    @staticmethod
    def handle_file(file):
        if file:
            with open(f'media/result_file/{file}', 'wb+'):
                result = ''
                for chunk in file.chunks():
                    result += chunk.decode('UTF-8')
                return result
        else:
            return None

    @staticmethod
    def handle_file_result(file, data):
        if not file:
            file = f'result_{Crypt.generate_file_token()}.txt'
        with open(f'media/result_file/{file}', 'w') as file:
            for string in data.split('\n'):
                file.write(string)
            return file

    @staticmethod
    def generate_file_token():
        characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
        return ''.join([random.choice(characters) for _ in range(5)])

    def crypt(self, text, key, file, algorithm, action):
        if file:
            text = file
        if algorithm == 'caesar':
            return self._caesar_cipher(text, key, action)
        elif algorithm == 'permutation':
            return self._permutation_cipher(text, key, action)
        elif algorithm == 'polybius':
            return self._polybius_cipher(text, key, action)
        elif algorithm == 'playfair':
            return self._playfair_cipher(text, key, action)
        # match algorithm:
        #     case 'caesar':
        #         return self._caesar_cipher(text, key, action)
        #     case 'permutation':
        #         return self._permutation_cipher(text, key, action)
        #     case 'polybius':
        #         return self._polybius_cipher(text, key, action)
        #     case 'playfair':
        #         return self._playfair_cipher(text, key, action)

    def _caesar_cipher(self, text, key, action):
        try:
            key = int(key)
        except ValueError:
            key = 1
        if action == 'encrypt':
            return self.__caesar_cipher(text, key)
        else:
            return self.__caesar_cipher(text, key * (-1))

    @staticmethod
    def __caesar_cipher(text, key):
        alphabet_eng, alphabet_eng_upper = 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        alphabet_rus, alphabet_rus_upper = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя', 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
        cipher_text = ''
        for letter in text:
            if letter in alphabet_eng:
                index = alphabet_eng.index(letter)
                cipher_index = (index + key) % 26
                cipher_text += alphabet_eng[cipher_index]
            elif letter in alphabet_eng_upper:
                index = alphabet_eng_upper.index(letter)
                cipher_index = (index + key) % 26
                cipher_text += alphabet_eng_upper[cipher_index]
            elif letter in alphabet_rus:
                index = alphabet_rus.index(letter)
                cipher_index = (index + key) % 33
                cipher_text += alphabet_rus[cipher_index]
            elif letter in alphabet_rus_upper:
                index = alphabet_rus_upper.index(letter)
                cipher_index = (index + key) % 33
                cipher_text += alphabet_rus_upper[cipher_index]
            else:
                cipher_text += letter
        return cipher_text

    def _permutation_cipher(self, text, key, action):
        alphabet = 'abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        random.seed(key)
        mapping = list(alphabet)
        random.shuffle(mapping)
        if action == 'encrypt':
            return self.__permutation_cipher(text, alphabet, mapping)
        else:
            return self.__permutation_cipher(text, mapping, alphabet)

    @staticmethod
    def __permutation_cipher(text, alphabet, mapping):
        crypto_text = ''
        for char in text:
            if char.lower() in alphabet:
                index = alphabet.index(char.lower())
                if char.isupper():
                    encrypted_char = mapping[index].upper()
                else:
                    encrypted_char = mapping[index]
                crypto_text += encrypted_char
            else:
                crypto_text += char
        return crypto_text

    def _polybius_cipher(self, text, key, action):
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ.,- ?'
        key = key.upper()
        key_letters = []
        for char in key:
            if char not in key_letters and char in alphabet:
                key_letters.append(char)
        for char in alphabet:
            if char not in key_letters:
                key_letters.append(char)

        if action == 'encrypt':
            return self.__polybius_encrypt(text, key_letters, alphabet)
        else:
            return self.__polybius_decrypt(text, key_letters)

    @staticmethod
    def __polybius_encrypt(text, key, alphabet):
        result = ''
        for char in text.upper():
            if char in alphabet:
                index = key.index(char)
                row = index // 8 + 1
                col = index % 8 + 1
                result += str(row) + str(col)
            else:
                result += char
        return result

    @staticmethod
    def __polybius_decrypt(text, key):
        result = ''
        i = 0
        while i < len(text):
            if text[i].isdigit() and i + 1 < len(text) and text[i+1].isdigit():
                row = int(text[i])
                col = int(text[i+1])
                index = (row - 1) * 8 + col - 1
                result += key[index]
                i += 2
            else:
                result += text[i]
                i += 1
        return result

    def _playfair_cipher(self, text, key, action):
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ.,- ?'
        key = ''.join([char for char in key.upper() if char in alphabet])
        key_chars = sorted(set(key), key=key.index)
        table = ''.join(key_chars + [ch for ch in alphabet if ch not in key_chars])

        if action == 'encrypt':
            return self.__playfair_encrypt(text, table)
        else:
            return self.__playfair_decrypt(text, table)

    @staticmethod
    def __playfair_encrypt(plaintext, table):
        plaintext = ''.join([char for char in plaintext.upper() if char in table])
        plaintext = re.sub(r'([A-ZА-Я])\1', r'\1Ъ\1', plaintext)
        plaintext = plaintext + 'Ъ' if len(plaintext) % 2 == 1 else plaintext
        ciphertext = ''
        for i in range(0, len(plaintext), 2):
            a, b = plaintext[i], plaintext[i + 1]
            row_a, col_a = divmod(table.index(a), 8)
            row_b, col_b = divmod(table.index(b), 8)
            if row_a == row_b:
                ciphertext += table[row_a * 8 + (col_a + 1) % 8] + table[row_b * 8 + (col_b + 1) % 8]
            elif col_a == col_b:
                ciphertext += table[((row_a + 1) % 8) * 8 + col_a] + table[((row_b + 1) % 8) * 8 + col_b]
            else:
                ciphertext += table[row_a * 8 + col_b] + table[row_b * 8 + col_a]
        return ciphertext

    @staticmethod
    def __playfair_decrypt(ciphertext, table):
        plaintext = ''
        for i in range(0, len(ciphertext), 2):
            a, b = ciphertext[i], ciphertext[i + 1]
            row_a, col_a = divmod(table.index(a), 8)
            row_b, col_b = divmod(table.index(b), 8)
            if row_a == row_b:
                plaintext += table[row_a * 8 + (col_a - 1) % 8] + table[row_b * 8 + (col_b - 1) % 8]
            elif col_a == col_b:
                plaintext += table[((row_a - 1) % 8) * 8 + col_a] + table[((row_b - 1) % 8) * 8 + col_b]
            else:
                plaintext += table[row_a * 8 + col_b] + table[row_b * 8 + col_a]
        plaintext = re.sub(r'(?<=[A-ZА-Я])Ъ(?=[A-ZА-Я])', '', plaintext)
        plaintext = re.sub(r'Ъ$', '', plaintext)
        return plaintext

# Тест на псевдопростоту числа Миллера Рабина, Ферма, Соловея-Штрассена, на основе символа Якоби
