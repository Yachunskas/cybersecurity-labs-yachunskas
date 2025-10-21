import hashlib
import getpass

# -------------------------------------------------------------------
# --- КРОК 1: РЕАЛІЗАЦІЯ ФУНКЦІЙ ЗГІДНО З ТЗ
# -------------------------------------------------------------------

def generate_keys(name, dob, secret_word):
    print(f"\n[Крок 1] Генерація ключів для: '{name}', '{dob}', '********'...")
    
    # 1. Створюємо рядок для хешування
    combined_string = name + dob + secret_word
    
    # 2. Отримуємо хеш SHA-256 (у вигляді шістнадцяткового рядка)
    private_key_hex = hashlib.sha256(combined_string.encode('utf-8')).hexdigest()
    
    # 3. Перетворюємо "Приватний ключ" в ЧИСЛО для математичних операцій
    #    hash("...") -> "a1b2c3..." -> 123456789...
    private_key_int = int(private_key_hex, 16)
    
    # 4. Визначаємо простий модуль для "Публічного ключа"
    prime_mod = 1000007 # 1,000,007 - просте число
    
    # 5. Створюємо "Публічний ключ" (спрощена математика з ТЗ)
    public_key_int = (private_key_int * 7) % prime_mod
    
    print("  > 'Приватний ключ' (як число): ... (дуже довге число)")
    print(f"  > 'Публічний ключ' (як число): {public_key_int}")
    
    # Повертаємо саме числові версії ключів для подальших операцій
    return private_key_int, public_key_int

def get_document_hash(document_content):
    # 1. Отримуємо хеш (шістнадцятковий рядок)
    doc_hash_hex = hashlib.sha256(document_content.encode('utf-8')).hexdigest()
    
    # 2. Перетворюємо хеш в ЧИСЛО
    doc_hash_int = int(doc_hash_hex, 16)
    
    return doc_hash_int

def create_signature(document_hash_int, private_key_int):
    print("\n[Крок 2] Створення підпису...")
    
    # Виконуємо операцію XOR (^)
    signature = document_hash_int ^ private_key_int
    
    print("  > Хеш документа (число)  XOR  Приватний ключ (число)")
    print("  > Підпис створено (це також дуже довге число).")
    return signature

def verify_signature(signature_int, current_document_content, private_key_int):
    print("\n[Крок 3] Перевірка підпису...")
    
    # 1. Отримуємо хеш ПОТОЧНОГО стану документа
    current_hash_int = get_document_hash(current_document_content)
    
    # 2. "Розшифровуємо" підпис, щоб отримати оригінальний хеш
    #    Використовуємо властивість XOR: (A ^ B) ^ B = A
    decrypted_hash_int = signature_int ^ private_key_int
    
    print(f"  > Хеш з підпису: ...{str(decrypted_hash_int)[-20:]}")
    print(f"  > Хеш поточного файла: ...{str(current_hash_int)[-20:]}")
    
    # 3. Порівнюємо хеші
    if decrypted_hash_int == current_hash_int:
        print("  > РЕЗУЛЬТАТ: Хеші збігаються.")
        return True
    else:
        print("  > РЕЗУЛЬТАТ: Хеші НЕ збігаються.")
        return False

# -------------------------------------------------------------------
# --- КРОК 2: ДЕМОНСТРАЦІЯ РОБОТИ СИСТЕМИ
# -------------------------------------------------------------------

if __name__ == "__main__":
    print("--- ДЕМОНСТРАЦІЯ СПРОЩЕНОГО ЦИФРОВОГО ПІДПИСУ ---")
    
    # --- Етап 1: Введення даних та генерація ключів ---
    # (Використовуємо дані з прикладу в ТЗ)
    user_name = input("Введіть ім'я (напр., Петренко): ")
    user_dob = input("Введіть дату (напр., 15031995): ")
    user_secret = getpass.getpass("Введіть секретне слово (напр., secret_word): ")

    # Генеруємо ключі згідно з ТЗ
    private_key, public_key = generate_keys(user_name, user_dob, user_secret)

    # --- Етап 2: Створення та перевірка ДІЙСНОГО підпису ---
    print("\n--- СЦЕНАРІЙ 1: ПІДПИСАННЯ ТА ПЕРЕВІРКА ОРИГІНАЛУ ---")
    
    # "Створюємо" наш документ
    original_document = f"Це моє резюме. Я, {user_name}, народився {user_dob[:2]}.{user_dob[2:4]}.{user_dob[4:]}."
    print(f"Оригінальний документ: '{original_document}'")
    
    # Отримуємо хеш оригінального документа
    original_hash = get_document_hash(original_document)
    
    # Створюємо підпис за допомогою приватного ключа
    signature = create_signature(original_hash, private_key)
    
    # Перевіряємо підпис на ОРИГІНАЛЬНОМУ документі
    # (Ніби ми відправили комусь 'original_document' і 'signature')
    print("Перевіряємо підпис на оригінальному документі...")
    is_valid = verify_signature(signature, original_document, private_key)
    
    if is_valid:
        print(">>> ВИСНОВОК: Підпис ДІЙСНИЙ 🟢")
    else:
        print(">>> ВИСНОВОК: Підпис ПІДРОБЛЕНИЙ 🔴")
        

    # --- Етап 3: Демонстрація виявлення ПІДРОБКИ (зміна документа) ---
    print("\n--- СЦЕНАРІЙ 2: ПЕРЕВІРКА ПІДПИСУ НА ЗМІНЕНОМУ ФАЙЛІ ---")
    
    # "Зловмисник" змінює документ, хоча б на 1 символ
    modified_document = "Це моє резюме. Я, Зломвисник Зловмисникович, народився 15.03.1995." # <-- Змінена дата
    print(f"Змінений документ:   '{modified_document}'")
    
    # Зловмисник намагається використати СТАРИЙ підпис для НОВОГО документа
    print("Використовуємо СТАРИЙ підпис для ЗМІНЕНОГО документа...")
    is_valid_modified = verify_signature(signature, modified_document, private_key)
    
    if is_valid_modified:
        print(">>> ВИСНОВОК: Підпис ДІЙСНИЙ 🟢")
    else:
        print(">>> ВИСНОВОК: Підпис ПІДРОБЛЕНИЙ 🔴 (Система виявила зміну!)")

    # --- Етап 4: Демонстрація захисту від підробки підпису ---
    print("\n--- СЦЕНАРІЙ 3: СПРОБА ПІДРОБИТИ ПІДПИС ---")
    print("Зловмисник хоче підписати змінений документ від вашого імені.")
    print("Для цього йому потрібно 'створити' новий підпис.")
    print(f"Формула підпису: НОВИЙ_ПІДПИС = (хеш_зміненого_файлу) XOR (ПРИВАТНИЙ_КЛЮЧ)")
    print("Зловмисник НЕ ЗНАЄ ваш 'приватний ключ' (або 'secret_word').")
    print(">>> ВИСНОВОК: Без приватного ключа підробити підпис НЕМОЖЛИВО. 🚫")