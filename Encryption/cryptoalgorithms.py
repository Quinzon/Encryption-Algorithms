import random
import re
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, PublicFormat, NoEncryption
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key
import base64
import chardet
from Crypto.Util import number


class Crypt:
    def __init__(self, text, key, file, algorithm, action):
        self.text = str(text)
        self.key = key
        self.file = file
        self.file_info = self.handle_file(file, algorithm)
        self.algorithm = algorithm
        self.action = action
        self.result = self.handle_result(text, key, self.file_info, algorithm, action)
        self.text_result = self.handle_text_result(self.result)
        self.file_result = self.handle_file_result(self.file, self.result)

    @staticmethod
    def handle_file(file, algorithm):
        if file:
            if re.search(r'\.[^.\\/:*?"<>|\r\n]+$', str(file))[0] == '.txt' and algorithm not in ["gamming", "RSA"]:
                with open(f'media/result_file/{file}', 'wb+'):
                    result = ''.join([chunk.decode('UTF-8') for chunk in file.chunks()])
                    return result
            else:
                with open(f'media/result_file/{file}', 'wb+'):
                    data = file.read()
                    return data
        else:
            return None

    @staticmethod
    def handle_file_result(file, data):
        if not file:
            file = f'result_{Crypt.generate_file_token()}.txt'
        else:
            file_extension = re.search(r'\.[^.\\/:*?"<>|\r\n]+$', str(file))[0]
            file = f'result_{Crypt.generate_file_token()}{file_extension}'

        if isinstance(data, str):
            with open(f'media/result_file/{file}', 'w') as file:
                for string in data.split('\n'):
                    file.write(string)
                return file
        else:
            with open(f'media/result_file/{file}', 'wb+') as file:
                file.write(data)
                return file

    @staticmethod
    def generate_file_token():
        characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
        return ''.join([random.choice(characters) for _ in range(5)])

    def handle_result(self, data, key, file_info, algorithm, action):
        if file_info:
            data = file_info
        result = self.crypt(data, key, algorithm, action)
        return result

    @staticmethod
    def handle_text_result(result):
        if not isinstance(result, str):
            try:
                result = result.decode(chardet.detect(result)['encoding'])
            except (UnicodeDecodeError, TypeError):
                result = 'Здесь могло быть много битовой информации не имеющей смысла, но её не будет.\n\r'
        return result

    def crypt(self, data, key, algorithm, action):
        if algorithm in ['caesar', 'permutation', 'polybius', 'playfair'] and not isinstance(data, str):
            return 'Только текстовый файл!'
        if algorithm == 'caesar':
            return self._caesar_cipher(data, key, action)
        elif algorithm == 'permutation':
            return self._permutation_cipher(data, key, action)
        elif algorithm == 'polybius':
            return self._polybius_cipher(data, key, action)
        elif algorithm == 'playfair':
            return self._playfair_cipher(data, key, action)
        elif algorithm == 'gamming':
            return self._gamming_cipher(data, key)
        elif algorithm == 'RSA':
            return self._rsa_cipher(data, key, action)

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
        plaintext = ''.join([char for char in plaintext.upper()])
        plaintext = re.sub(r'([A-ZА-Я])\1', r'\1Ъ\1', plaintext)
        plaintext = plaintext + 'Ъ' if len(plaintext) % 2 == 1 else plaintext
        ciphertext = ''
        for i in range(0, len(plaintext), 2):
            if plaintext[i] in table and plaintext[i + 1] in table:
                a, b = plaintext[i], plaintext[i + 1]
                row_a, col_a = divmod(table.index(a), 8)
                row_b, col_b = divmod(table.index(b), 8)
                if row_a == row_b:
                    ciphertext += table[row_a * 8 + (col_a + 1) % 8] + table[row_b * 8 + (col_b + 1) % 8]
                elif col_a == col_b:
                    ciphertext += table[((row_a + 1) % 8) * 8 + col_a] + table[((row_b + 1) % 8) * 8 + col_b]
                else:
                    ciphertext += table[row_a * 8 + col_b] + table[row_b * 8 + col_a]
            else:
                ciphertext += plaintext[i] + plaintext[i + 1]
        return ciphertext

    @staticmethod
    def __playfair_decrypt(ciphertext, table):
        plaintext = ''
        for i in range(0, len(ciphertext), 2):
            if ciphertext[i] in table and ciphertext[i + 1] in table:
                a, b = ciphertext[i], ciphertext[i + 1]
                row_a, col_a = divmod(table.index(a), 8)
                row_b, col_b = divmod(table.index(b), 8)
                if row_a == row_b:
                    plaintext += table[row_a * 8 + (col_a - 1) % 8] + table[row_b * 8 + (col_b - 1) % 8]
                elif col_a == col_b:
                    plaintext += table[((row_a - 1) % 8) * 8 + col_a] + table[((row_b - 1) % 8) * 8 + col_b]
                else:
                    plaintext += table[row_a * 8 + col_b] + table[row_b * 8 + col_a]
            else:
                plaintext += ciphertext[i] + ciphertext[i + 1]
        plaintext = re.sub(r'(?<=[A-ZА-Я])Ъ(?=[A-ZА-Я])', '', plaintext)
        plaintext = re.sub(r'Ъ$', '', plaintext)
        return plaintext

    @staticmethod
    def _gamming_cipher(data, key):
        if isinstance(data, str):
            data = data.encode()
        key = key.encode()
        key_stream = bytes(a ^ b for a, b in zip(data, key * (len(data) // len(key) + 1)))
        return key_stream

    def _rsa_cipher(self, data, key, action):
        if isinstance(data, str):
            data = data.encode('utf-8')
        if action == 'encrypt':
            return self.__rsa_encrypt(data, key)
        else:
            return self.__rsa_decrypt(data, key)

    @staticmethod
    def __rsa_encrypt(plain_data, public_key_pem):
        try:
            public_key = load_pem_public_key(public_key_pem.encode('utf-8'))
        except ValueError:
            return 'Ключ необходимо предоставить в формате PEM'
        max_block_size = (public_key.key_size + 7) // 8 - 11

        plain_blocks = [plain_data[i:i + max_block_size]
                        for i in range(0, len(plain_data), max_block_size)]

        encrypted_blocks = []
        for block in plain_blocks:
            encrypted_block = public_key.encrypt(
                block,
                padding.PKCS1v15()
            )
            encrypted_blocks.append(encrypted_block)

        encrypted_data = b"".join(encrypted_blocks)
        return base64.b64encode(encrypted_data)

    @staticmethod
    def __rsa_decrypt(encrypted_data, private_key_pem):
        try:
            private_key = load_pem_private_key(private_key_pem.encode('utf-8'), password=None)
        except ValueError:
            return 'Ключ необходимо предоставить в формате PEM'
        encrypted_data_bytes = base64.b64decode(encrypted_data)
        block_size = (private_key.key_size + 7) // 8

        encrypted_blocks = [encrypted_data_bytes[i:i + block_size]
                            for i in range(0, len(encrypted_data_bytes), block_size)]

        decrypted_blocks = []
        for block in encrypted_blocks:
            decrypted_block = private_key.decrypt(
                block,
                padding.PKCS1v15()
            )
            decrypted_blocks.append(decrypted_block)

        decrypted_data = b"".join(decrypted_blocks)
        return decrypted_data


class GenerateKey:
    @staticmethod
    def generate_rsa_keys_pem():
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )

        pem_private_key = private_key.private_bytes(
            encoding=Encoding.PEM,
            format=PrivateFormat.PKCS8,
            encryption_algorithm=NoEncryption()
        )

        public_key = private_key.public_key()

        pem_public_key = public_key.public_bytes(
            encoding=Encoding.PEM,
            format=PublicFormat.SubjectPublicKeyInfo
        )

        return {'private': pem_private_key.decode('utf-8'),
                'public': pem_public_key.decode('utf-8')}

    @staticmethod
    def generate_diffie_hellman() -> int:
        bits = 2048
        prime = number.getPrime(bits)
        generator = random.randint(2, prime - 1)

        secret_key_a = random.randint(1, prime - 1)
        secret_key_b = random.randint(1, prime - 1)

        public_key_a = pow(generator, secret_key_a, prime)
        public_key_b = pow(generator, secret_key_b, prime)

        shared_key_a = pow(public_key_b, secret_key_a, prime)
        shared_key_b = pow(public_key_a, secret_key_b, prime)

        return shared_key_a
