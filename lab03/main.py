from PIL import Image
import numpy as np


def text_to_binary(text):
    binary = ''.join(format(ord(char), '08b') for char in text)
    return binary


def binary_to_text(binary):
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    text = ''.join(chr(int(char, 2)) for char in chars)
    return text


def hide_message(image_path, message, output_path):
    # Відкриваємо зображення
    img = Image.open(image_path)
    img_array = np.array(img)
    
    # Додаємо маркери для визначення меж повідомлення
    START_MARKER = "<<<START>>>"
    END_MARKER = "<<<END>>>"
    full_message = START_MARKER + message + END_MARKER
    
    # Конвертуємо повідомлення в бінарний формат
    binary_message = text_to_binary(full_message)
    message_length = len(binary_message)
    
    # Перевіряємо, чи достатньо місця в зображенні
    total_pixels = img_array.shape[0] * img_array.shape[1] * img_array.shape[2]
    if message_length > total_pixels:
        raise ValueError(f"Повідомлення занадто довге! Максимум {total_pixels} біт, потрібно {message_length}")
    
    print(f"Довжина повідомлення: {len(message)} символів")
    print(f"Розмір повідомлення в бітах: {message_length} біт")
    print(f"Доступно пікселів: {total_pixels}")
    
    # Перетворюємо зображення в одновимірний масив
    flat_array = img_array.flatten()
    
    # Приховуємо біти повідомлення в молодших бітах пікселів
    for i in range(message_length):
        # Отримуємо біт повідомлення
        bit = int(binary_message[i])
        
        # Замінюємо молодший біт пікселя
        # Спочатку обнуляємо молодший біт (побітове І з 254 = 11111110)
        # Потім встановлюємо потрібний біт (побітове АБО)
        flat_array[i] = (flat_array[i] & 254) | bit
    
    # Повертаємо форму масиву та зберігаємо зображення
    modified_array = flat_array.reshape(img_array.shape)
    modified_img = Image.fromarray(modified_array.astype('uint8'))
    modified_img.save(output_path)
    
    print(f"Повідомлення успішно приховано в {output_path}")


def extract_message(image_path):
    # Відкриваємо зображення
    img = Image.open(image_path)
    img_array = np.array(img)
    
    # Перетворюємо в одновимірний масив
    flat_array = img_array.flatten()
    
    # Витягуємо молодші біти з пікселів
    binary_message = ''
    for pixel in flat_array:
        # Отримуємо молодший біт (побітове І з 1)
        binary_message += str(pixel & 1)
    
    # Конвертуємо бінарний рядок у текст порціями по 8 біт
    extracted_text = ''
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        if len(byte) == 8:
            try:
                char = chr(int(byte, 2))
                extracted_text += char
            except:
                break
    
    # Шукаємо маркери початку та кінця
    START_MARKER = "<<<START>>>"
    END_MARKER = "<<<END>>>"
    
    start_index = extracted_text.find(START_MARKER)
    end_index = extracted_text.find(END_MARKER)
    
    if start_index != -1 and end_index != -1:
        message = extracted_text[start_index + len(START_MARKER):end_index]
        print("Повідомлення успішно витягнуто")
        return message
    else:
        print("Не знайдено маркерів повідомлення")
        return None


def analyze_image_changes(original_path, modified_path):
    # Відкриваємо обидва зображення
    original = np.array(Image.open(original_path))
    modified = np.array(Image.open(modified_path))
    
    # Обчислюємо різницю
    diff = np.abs(original.astype(int) - modified.astype(int))
    
    # Статистика змін
    total_pixels = original.size
    changed_pixels = np.count_nonzero(diff)
    max_change = np.max(diff)
    avg_change = np.mean(diff)
    
    print("\n--- Аналіз змін в зображенні ---")
    print(f"Загальна кількість пікселів: {total_pixels}")
    print(f"Змінених пікселів: {changed_pixels} ({changed_pixels/total_pixels*100:.4f}%)")
    print(f"Максимальна зміна значення пікселя: {max_change}")
    print(f"Середня зміна значення пікселя: {avg_change:.6f}")
    print(f"Зміни непомітні для людського ока: {'Так' if max_change <= 1 else 'Ні'}")
    
    return {
        'total_pixels': total_pixels,
        'changed_pixels': changed_pixels,
        'max_change': max_change,
        'avg_change': avg_change
    }


def main():
    print("=" * 60)
    print("Стеганографія: приховування тексту в зображеннях (LSB)")
    print("=" * 60)
    
    # Шляхи до файлів
    original_image = "photos/original.png"
    modified_image = "photos/hidden.png"
    
    # Повідомлення для приховування
    secret_message = input("Введіть повідомлення для приховування: ")
    
    print(f"\nПовідомлення: {secret_message}")
    
    try:
        # Приховуємо повідомлення
        print("\n1. Приховування повідомлення...")
        hide_message(original_image, secret_message, modified_image)
        
        # Витягуємо повідомлення
        print("\n2. Витягування повідомлення...")
        extracted = extract_message(modified_image)
        print(f"Витягнуте повідомлення: {extracted}")
        
        # Перевіряємо коректність
        if extracted == secret_message:
            print("\nПеревірка: Повідомлення витягнуто правильно")
        else:
            print("\nПеревірка: Помилка при витягуванні")
        
        # Аналізуємо зміни
        print("\n3. Аналіз змін в зображенні...")
        analyze_image_changes(original_image, modified_image)
        
    except FileNotFoundError:
        print(f"\nПомилка: Файл {original_image} не знайдено")
        print("Створіть тестове зображення або змініть шлях до файлу")
    except Exception as e:
        print(f"\nПомилка: {e}")

if __name__ == "__main__":
    main()