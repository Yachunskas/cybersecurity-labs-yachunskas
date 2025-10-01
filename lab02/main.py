from collections import Counter


class CaesarCipher:
    def __init__(self, shift):
        self.shift = shift % 26
    
    def encrypt(self, text):
        result = []
        for char in text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                shifted = (ord(char) - base + self.shift) % 26
                result.append(chr(base + shifted))
            else:
                result.append(char)
        return ''.join(result)
    
    def decrypt(self, text):
        self.shift = -self.shift
        decrypted = self.encrypt(text)
        self.shift = -self.shift
        return decrypted


class VigenereCipher:
    def __init__(self, key):
        self.key = key.upper()
    
    def encrypt(self, text):
        result = []
        key_index = 0
        
        for char in text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                shift = ord(self.key[key_index % len(self.key)]) - ord('A')
                shifted = (ord(char) - base + shift) % 26
                result.append(chr(base + shifted))
                key_index += 1
            else:
                result.append(char)
        
        return ''.join(result)
    
    def decrypt(self, text):
        result = []
        key_index = 0
        
        for char in text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                shift = ord(self.key[key_index % len(self.key)]) - ord('A')
                shifted = (ord(char) - base - shift) % 26
                result.append(chr(base + shifted))
                key_index += 1
            else:
                result.append(char)
        
        return ''.join(result)


def analyze_results(original, caesar_encrypted, vigenere_encrypted, caesar_key, vigenere_key):
    print("\n" + "="*70)
    print("ПОРІВНЯЛЬНИЙ АНАЛІЗ РЕЗУЛЬТАТІВ ШИФРУВАННЯ")
    print("="*70)
    
    print(f"\nОригінальний текст:\n   {original}")
    print(f"\nШифр Цезаря (зсув {caesar_key}):\n   {caesar_encrypted}")
    print(f"\nШифр Віженера (ключ '{vigenere_key}'):\n   {vigenere_encrypted}")
    
    # Довжина текстів
    print(f"\nСТАТИСТИКА:")
    print(f"   Довжина оригіналу: {len(original)} символів")
    print(f"   Літер в оригіналі: {sum(c.isalpha() for c in original)}")
    
    # Частотний аналіз для Цезаря
    caesar_letters = [c.upper() for c in caesar_encrypted if c.isalpha()]
    if caesar_letters:
        caesar_freq = Counter(caesar_letters).most_common(3)
        print(f"\n   Шифр Цезаря - найчастіші літери:")
        for letter, count in caesar_freq:
            print(f"      {letter}: {count} разів ({count/len(caesar_letters)*100:.1f}%)")
    
    # Частотний аналіз для Віженера
    vigenere_letters = [c.upper() for c in vigenere_encrypted if c.isalpha()]
    if vigenere_letters:
        vigenere_freq = Counter(vigenere_letters).most_common(3)
        print(f"\n   Шифр Віженера - найчастіші літери:")
        for letter, count in vigenere_freq:
            print(f"      {letter}: {count} разів ({count/len(vigenere_letters)*100:.1f}%)")
    
    # Порівняння стійкості
    print(f"\nОЦІНКА СТІЙКОСТІ:")
    print(f"   Шифр Цезаря:")
    print(f"      - Можливих ключів: 25")
    print(f"      - Легко зламати методом перебору")
    print(f"      - Зберігає частотність літер")
    
    print(f"\n   Шифр Віженера:")
    print(f"      - Довжина ключа: {len(vigenere_key)}")
    print(f"      - Можливих комбінацій: 26^{len(vigenere_key)}")
    print(f"      - Складніший для криптоаналізу")
    print(f"      - Розмиває частотність літер")
    
    print("\n" + "="*70)


def print_menu():
    print("\n" + "="*70)
    print("                   ПРОГРАМА ШИФРУВАННЯ")
    print("="*70)
    print("\n1. Шифрування методом Цезаря")
    print("2. Розшифрування методом Цезаря")
    print("3. Шифрування методом Віженера")
    print("4. Розшифрування методом Віженера")
    print("5. Порівняльний аналіз обох методів")
    print("0. Вихід")
    print("\n" + "-"*70)


def main():
    while True:
        print_menu()
        choice = input("\nВиберіть опцію (0-5): ").strip()
        
        if choice == '0':
            break
        
        elif choice == '1':
            text = input("\nВведіть текст для шифрування: ")
            try:
                shift = int(input("Введіть ключ (зсув, число): "))
                cipher = CaesarCipher(shift)
                encrypted = cipher.encrypt(text)
                print(f"\nЗашифрований текст: {encrypted}")
            except ValueError:
                print("❌ Помилка! Ключ повинен бути числом.")
        
        elif choice == '2':
            text = input("\nВведіть текст для розшифрування: ")
            try:
                shift = int(input("Введіть ключ (зсув, число): "))
                cipher = CaesarCipher(shift)
                decrypted = cipher.decrypt(text)
                print(f"\nРозшифрований текст: {decrypted}")
            except ValueError:
                print("❌ Помилка! Ключ повинен бути числом.")
        
        elif choice == '3':
            text = input("\nВведіть текст для шифрування: ")
            key = input("Введіть ключове слово: ")
            if key.isalpha():
                cipher = VigenereCipher(key)
                encrypted = cipher.encrypt(text)
                print(f"\nашифрований текст: {encrypted}")
            else:
                print("❌ Помилка! Ключ повинен містити тільки літери.")
        
        elif choice == '4':
            text = input("\nВведіть текст для розшифрування: ")
            key = input("Введіть ключове слово: ")
            if key.isalpha():
                cipher = VigenereCipher(key)
                decrypted = cipher.decrypt(text)
                print(f"\nРозшифрований текст: {decrypted}")
            else:
                print("❌ Помилка! Ключ повинен містити тільки літери.")
        
        elif choice == '5':
            text = input("\nВведіть текст для аналізу: ")
            
            try:
                caesar_shift = int(input("Введіть зсув для шифру Цезаря: "))
                vigenere_key = input("Введіть ключ для шифру Віженера: ")
                
                if not vigenere_key.isalpha():
                    print("❌ Помилка! Ключ Віженера повинен містити тільки літери.")
                    continue
                
                # Шифрування обома методами
                caesar = CaesarCipher(caesar_shift)
                vigenere = VigenereCipher(vigenere_key)
                
                caesar_enc = caesar.encrypt(text)
                vigenere_enc = vigenere.encrypt(text)
                
                # Порівняльний аналіз
                analyze_results(text, caesar_enc, vigenere_enc, 
                              caesar_shift, vigenere_key)
                
            except ValueError:
                print("❌ Помилка! Зсув Цезаря повинен бути числом.")
        
        else:
            print("❌ Невірний вибір! Спробуйте ще раз.")
        
        input("\nНатисніть Enter для продовження...")


if __name__ == "__main__":
    main()