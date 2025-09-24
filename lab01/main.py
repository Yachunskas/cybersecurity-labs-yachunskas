import re
from datetime import datetime

class PasswordSecurityAnalyzer:
    def __init__(self):
        self.personal_data = {}
        
    def input_personal_data(self):
        print("=== ВВЕДЕННЯ ПЕРСОНАЛЬНИХ ДАНИХ ===")
        self.personal_data['password'] = input("Введіть пароль: ")
        self.personal_data['name'] = input("Введіть ім'я (латиницею): ").lower()
        self.personal_data['birth_date'] = input("Введіть дату народження (ДД.ММ.РРРР): ")
        
        # Витягуємо рік з дати народження
        try:
            self.personal_data['birth_year'] = self.personal_data['birth_date'].split('.')[2]
        except:
            self.personal_data['birth_year'] = ""
    
    def analyze_personal_data_usage(self):
        password = self.personal_data['password'].lower()
        issues = []
        
        # Перевірка на наявність імені
        if self.personal_data['name'] in password:
            issues.append(f"Пароль містить ваше ім'я: {self.personal_data['name']}")
            
        # Перевірка на наявність року народження
        if self.personal_data['birth_year'] in password:
            issues.append(f"Пароль містить рік народження: {self.personal_data['birth_year']}")
            
        # Перевірка на наявність дати народження
        if self.personal_data['birth_date'].replace('.', '') in password.replace('.', ''):
            issues.append(f"Пароль містить дату народження")
            
        return issues
    
    def evaluate_password_complexity(self):
        password = self.personal_data['password']
        score = 0
        criteria = []
        
        # Довжина пароля
        if len(password) >= 12:
            score += 3
            criteria.append("✓ Довжина 12+ символів (3 бали)")
        elif len(password) >= 8:
            score += 2
            criteria.append("✓ Довжина 8+ символів (2 бали)")
        elif len(password) >= 6:
            score += 1
            criteria.append("✓ Довжина 6+ символів (1 бал)")
        else:
            criteria.append("✗ Занадто короткий пароль (0 балів)")
            
        # Різноманітність символів
        if re.search(r'[a-z]', password):
            score += 1
            criteria.append("✓ Містить малі літери (1 бал)")
        else:
            criteria.append("✗ Не містить малі літери (0 балів)")
            
        if re.search(r'[A-Z]', password):
            score += 2
            criteria.append("✓ Містить великі літери (2 бали)")
        else:
            criteria.append("✗ Не містить великі літери (0 балів)")
            
        if re.search(r'\d', password):
            score += 2
            criteria.append("✓ Містить цифри (2 бали)")
        else:
            criteria.append("✗ Не містить цифри (0 балів)")
            
        if re.search(r'[!@#$%^&*()_+\-=\[\]{};:"\\|,.<>\/?]', password):
            score += 2
            criteria.append("✓ Містить спеціальні символи (2 бали)")
        else:
            criteria.append("✗ Не містить спеціальні символи (0 балів)")
            
        # Словникові слова
        common_words = ['password', 'пароль', '123456', 'qwerty', 'admin', 'user', '1234', '12345678', '1234567890']
        for word in common_words:
            if word.lower() in password.lower():
                score -= 2
                criteria.append(f"✗ Містить словникове слово '{word}' (-2 бали)")
                
        return score, criteria
    
    def provide_recommendations(self, score, personal_issues):
        recommendations = []
            
        if score < 5 or personal_issues:
            recommendations.append("🔴 Пароль дуже слабкий! Негайно змініть його!")
        elif score < 6:
            recommendations.append("🟡 Пароль слабкий. Рекомендується покращити.")
        elif score < 8:
            recommendations.append("🟢 Пароль середньої складності. Можна покращити.")
        else:
            recommendations.append("🟢 Пароль сильний! Гарна робота!")
        
        return recommendations
    
    def run_analysis(self):
        print("АНАЛІЗАТОР БЕЗПЕКИ ПАРОЛІВ\n")
        
        # Введення даних
        self.input_personal_data()
        
        print("\n" + "="*50)
        print("РЕЗУЛЬТАТИ АНАЛІЗУ")
        print("="*50)
        
        # Аналіз персональних даних
        personal_issues = self.analyze_personal_data_usage()
        if personal_issues:
            print("\n🔴 ВИЯВЛЕНО ВИКОРИСТАННЯ ПЕРСОНАЛЬНИХ ДАНИХ:")
            for issue in personal_issues:
                print(f"   • {issue}")
        else:
            print("\n🟢 Персональні дані не виявлено в паролі")
            
        # Оцінка складності
        score, criteria = self.evaluate_password_complexity()
        print(f"\nОЦІНКА СКЛАДНОСТІ: {score}/10 балів")
        print("\nДеталізація:")
        for criterion in criteria:
            print(f"   {criterion}")
            
        # Рекомендації
        recommendations = self.provide_recommendations(score, personal_issues)
        print(f"\nРЕКОМЕНДАЦІЇ:")
        for rec in recommendations:
            print(rec)

# Тестування програми
if __name__ == "__main__":
    analyzer = PasswordSecurityAnalyzer()
    analyzer.run_analysis()