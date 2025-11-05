import hashlib
import base64
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.backends import default_backend

AES_BLOCK_SIZE = algorithms.AES.block_size // 8

def generate_key_from_data(personal_data: str) -> bytes:
    # SHA-256 створює 32-байтний хеш
    key = hashlib.sha256(personal_data.encode('utf-8')).digest()
    return key

def encrypt_message(message: str, key: bytes) -> str:
    # 1. Генерація випадкового вектору ініціалізації (IV)
    # IV гарантує, що однаковий текст, зашифрований тим самим ключем, 
    # щоразу даватиме різний результат.
    iv = os.urandom(AES_BLOCK_SIZE)
    
    # 2. Налаштування шифру
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # 3. Доповнення повідомлення (Padding) до розміру, кратного блоку
    padder = PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(message.encode('utf-8')) + padder.finalize()
    
    # 4. Шифрування
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    
    # 5. Об'єднання IV та шифротексту
    # Отримувач повинен знати IV для розшифрування. 
    # Його безпечно передавати відкрито разом із шифротекстом.
    encrypted_data = iv + ciphertext
    
    # 6. Кодування в Base64 для безпечної передачі у вигляді тексту
    return base64.b64encode(encrypted_data).decode('utf-8')

def decrypt_message(encrypted_data_b64: str, key: bytes) -> str:
    try:
        # 1. Декодування з Base64
        encrypted_data = base64.b64decode(encrypted_data_b64)
    except (base64.binascii.Error, ValueError):
        return "Помилка: Невірні Base64 дані"

    # 2. Розділення IV та шифротексту
    iv = encrypted_data[:AES_BLOCK_SIZE]
    ciphertext = encrypted_data[AES_BLOCK_SIZE:]

    if len(iv) != AES_BLOCK_SIZE:
        return "Помилка: Невірний формат (IV відсутній або має невірну довжину)"

    # 3. Налаштування дешифратора
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    try:
        # 4. Розшифрування
        padded_decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
    except ValueError:
        return "Помилка: Невірні зашифровані дані (можливо, невірний ключ)"

    try:
        # 5. Видалення доповнення (Unpadding)
        unpadder = PKCS7(algorithms.AES.block_size).unpadder()
        decrypted_data = unpadder.update(padded_decrypted_data) + unpadder.finalize()
    except ValueError:
        # Ця помилка найчастіше виникає, якщо ключ невірний
        return "Помилка: Невірний ключ або пошкоджені дані (помилка відступу)"

    return decrypted_data.decode('utf-8')

def demonstration_process():
    # 1. Вхідні дані (за прикладом з ТЗ)
    email = "ivan.petrenko@gmail.com"
    personal_info = "IvanPetrenko1995"
    message_to_send = "Зустрічаємося завтра о 15:00"

    print(f"--- Демонстрація безпечного обміну ---")
    print(f"Користувач: {email}")
    print(f"Секретна фраза (основа ключа): {personal_info}")
    print(f"Вихідне повідомлення: \"{message_to_send}\"\n")

    # 2. Генерація ключа
    # Обидві сторони (відправник і отримувач) 
    # повинні згенерувати однаковий ключ з однакових даних.
    shared_key = generate_key_from_data(personal_info)
    print(f"Згенерований ключ (SHA-256): {shared_key.hex()}\n")

    # 3. Процес відправника (Шифрування)
    print("--- Процес відправника (Шифрування) ---")
    encrypted_message = encrypt_message(message_to_send, shared_key)
    print(f"Зашифровані дані (Base64 для email): {encrypted_message}\n")
    
    # 4. Процес отримувача (Розшифрування)
    print("--- Процес отримувача (Розшифрування) ---")
    print(f"Отримані дані: {encrypted_message}")
    
    # Отримувач використовує той самий ключ, згенерований з 'personal_info'
    decrypted_message = decrypt_message(encrypted_message, shared_key)
    print(f"Розшифроване повідомлення: \"{decrypted_message}\"\n")

    # 5. Демонстрація збою (невірний ключ)
    print("--- Демонстрація з невірним ключем ---")
    wrong_personal_info = "IvanPetrenko1996" # Змінені дані
    wrong_key = generate_key_from_data(wrong_personal_info)
    print(f"Спроба розшифрувати з невірним ключем (від '{wrong_personal_info}')...")
    
    failed_decryption = decrypt_message(encrypted_message, wrong_key)
    print(f"Результат: {failed_decryption}")

if __name__ == "__main__":
    demonstration_process()