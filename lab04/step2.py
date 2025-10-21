import hashlib
import getpass

print("--- Демонстрація 'Кроку 2': Створення навчальної пари ключів ---")

# --- Крок 2.1: Отримання персональних даних ---
name = input("Введіть ваше ім'я: ")
dob = input("Введіть вашу дату народження (напр., 01.01.2000): ")
secret_word = getpass.getpass("Введіть ваше секретне слово (введення буде приховано): ")

# --- Крок 2.2: Створення "Приватного ключа" ---
# 1. Об'єднуємо всі дані в один рядок
data_to_hash = name + dob + secret_word

# 2. Кодуємо рядок в байти, оскільки хеш-функції працюють з байтами
data_bytes = data_to_hash.encode('utf-8')

# 3. Створюємо хеш SHA-256
private_key_hash = hashlib.sha256(data_bytes).hexdigest()

print("\n------------------------------------------------------")
print(f"[Крок 2.2] Створено 'Приватний ключ' (хеш від '{data_to_hash}')")
print(f"Приватний ключ: {private_key_hash}")

# --- Крок 2.3: Створення "Публічного ключа" ---
public_key_hash = hashlib.sha256(private_key_hash.encode('utf-8')).hexdigest()

print(f"\n[Крок 2.3] Створено 'Публічний ключ' (хеш від приватного ключа)")
print(f"Публічний ключ: {public_key_hash}")

# --- Крок 2.4: Збереження ключів у файлах ---
try:
    with open("private_key.txt", "w") as f:
        f.write(private_key_hash)
    
    with open("public_key.txt", "w") as f:
        f.write(public_key_hash)
    
    print("\n------------------------------------------------------")
    print("[Крок 2.4] Ключі успішно збережено в окремих файлах:")
    print("- private_key.txt")
    print("- public_key.txt")
    print("------------------------------------------------------")

except IOError as e:
    print(f"\nПомилка: Не вдалося зберегти файли. {e}")