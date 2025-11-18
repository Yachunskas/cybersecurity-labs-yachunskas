import sqlite3
import os

DB_NAME = 'vulnerable_demo.db'

def setup_database():
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    );
    ''')
    
    cursor.execute("INSERT INTO users (username, password, role) VALUES ('admin', 'superS3cret!', 'admin')")
    cursor.execute("INSERT INTO users (username, password, role) VALUES ('bob', 'password123', 'user')")
    cursor.execute("INSERT INTO users (username, password, role) VALUES ('alice', 'alice_pwd', 'user')")
    
    conn.commit()
    conn.close()

def login_vulnerable(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # ВРАЗЛИВИЙ ЗАПИТ: користувацький ввід прямо вставляється в SQL
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    print(f" > Виконується запит: {query}")
    
    try:
        cursor.execute(query)
        user = cursor.fetchone()
    except sqlite3.Error as e:
        print(f"   [!] Помилка SQL: {e}")
        user = None
        
    conn.close()
    return user

def login_secure(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    print(f" > Виконується запит: {query} з параметрами ({username}, {password})")
    
    try:
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
    except sqlite3.Error as e:
        print(f"   [!] Помилка SQL: {e}") # Цей блок не спрацює при ін'єкції
        user = None
        
    conn.close()
    return user

def demonstrate_attack():
    """Виконує демонстрацію атаки та захисту."""
    
    setup_database()
    
    # Це класичний пейлоад для SQL-ін'єкції.
    # ' OR '1'='1' -- 
    # Це змусить частину WHERE виглядати так:
    # WHERE username = '' OR '1'='1' --' AND password = '...'
    # Частина '--' коментує решту запиту (перевірку пароля).
    # '1'='1' завжди правда, тому запит поверне першого користувача (admin).
    
    attack_username = "' OR '1'='1' --"
    attack_password = "password_doesnt_matter"

    print("==============================================")
    print("ДЕМОНСТРАЦІЯ ВРАЗЛИВОЇ ВЕРСІЇ (Атака)")
    print("==============================================")
    print(f"Спроба входу з ім'ям: {attack_username}")
    print(f"Спроба входу з паролем: {attack_password}\n")

    vulnerable_result = login_vulnerable(attack_username, attack_password)
    
    if vulnerable_result:
        print("\n   [!!!] АТАКА УСПІШНА!")
        print(f"   [>] Отримано доступ як: {vulnerable_result[1]} (Роль: {vulnerable_result[3]})")
        print("   [>] Відбувся витік даних першого рядка таблиці.")
    else:
        print("\n   [+] Вхід не вдався.")

    print("\n\n==============================================")
    print("ДЕМОНСТРАЦІЯ ЗАХИЩЕНОЇ ВЕРСІЇ (Захист)")
    print("==============================================")
    print(f"Спроба входу з тим самим ім'ям: {attack_username}")
    print(f"Спроба входу з тим самим паролем: {attack_password}\n")

    secure_result = login_secure(attack_username, attack_password)

    if secure_result:
        print("\n   [!!!] АТАКА УСПІШНА! (Це не повинно було статись)")
        print(f"   [>] Отримано доступ як: {secure_result[1]}")
    else:
        print("\n   [+] АТАКА ЗАБЛОКОВАНА.")
        print("   [>] Запит обробив ввід як звичайний рядок.")
        print("   [>] Користувача з ім'ям \"' OR '1'='1' --\" не знайдено.")

if __name__ == "__main__":
    demonstrate_attack()